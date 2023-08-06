import sys
import copy
import typing
import logging
from github import Github, Repository, ContentFile
import yaml
import ruamel.yaml

from . import models, utils


"""Interface for storing regimens on github?
"""

logger = logging.getLogger(__name__)

ruamel_yaml = ruamel.yaml.YAML(typ=['rt', 'string'])  # for anchor preservation

GithubRegimen = typing.Tuple[models.Regimen, dict]


def get_head_commit_content(repo: Repository, regimen_branch_name: str, filename: str = "regimen.yml") -> ContentFile:
    branch = repo.get_branch(regimen_branch_name)
    head_commit = branch.commit
    logger.debug("Head commit: %s" % head_commit)
    return repo.get_contents(filename, ref=head_commit.sha)


def get(client: Github, github_repo_name: str, regimen_branch_name: str) -> GithubRegimen:
    repo = client.get_repo(github_repo_name)
    content_file = get_head_commit_content(repo, regimen_branch_name)
    decoded = content_file.decoded_content
    return models.Regimen.from_yaml(decoded), ruamel_yaml.load(decoded)


def put(client: Github, regimen: GithubRegimen, github_repo_name: str, regimen_branch_name: str, update_message: str = "mtrain-superclient update regimen default commit message.") -> str:
    repo = client.get_repo(github_repo_name)
    content_file = get_head_commit_content(repo, regimen_branch_name)
    repo.update_file(
        content_file.path,
        message=update_message,
        content=ruamel_yaml.dump_to_string(regimen[1]),
        sha=content_file.sha,
        branch=regimen_branch_name,
    )
    return regimen[0].name

RegimenUpdate = typing.Tuple[str, typing.Any]
def update_regimen(regimen: GithubRegimen, updates: typing.List[RegimenUpdate]) -> GithubRegimen:
    """Updates the regimen dict then generates a new regimen from that dict?
    """
    _, regimen_dict = regimen
    updated_regimen_dict = copy.deepcopy(regimen_dict)
    for update in updates:
        field_name, value = update
        logger.setLevel(logging.DEBUG)
        # logger.debug("field_name: %s" % field_name[0])
        # logger.debug("value: %s" % value)
        target = updated_regimen_dict
        logger.debug("Field name: %s" % str(field_name))
        for key in field_name[:-1]:  # get nested key values
            target = target[key]
        target[field_name[-1]] = value
        logger.debug("Target value: %s" % target)

    dumped = ruamel_yaml.dump_to_string(
        updated_regimen_dict
    )
    # logger.debug("bur")
    updated_regimen = models.Regimen.from_dict(yaml.safe_load(dumped))
    # logger.debug("bur")
    return updated_regimen, updated_regimen_dict


def resolve_builtin_callable(name: str) -> typing.Callable:
    return getattr(utils, name, None)


def resolve_conditional(updates: list[RegimenUpdate], conditional: models.RegimenUpdateConditional) -> models.RegimenUpdate:
    """Resolves a builtin callable value from a list of updates and a conditional.
    """
    params = []
    for param in conditional.params:
        if param.is_property:
            for update_name, update_value in updates:
                if update_name == param.name:
                    params.append(update_value)
                    break
        else:
            params.append(param.value)
    
    resolved_builtin = resolve_builtin_callable(conditional.op)
    if resolved_builtin is None:
        raise Exception("Could not resolve builtin callable: %s" % conditional.op)

    # return models.RegimenUpdate(
    #     name=conditional.prop_name,
    #     value=resolved_builtin(
    #         conditional.op,
    #     )(*params),
    # )
    return (
        conditional.prop_name,
        resolved_builtin(*params),
    )


def resolve_updates(updates: list[RegimenUpdate], recipie: models.RegimenUpdateRecipie) -> list[RegimenUpdate]:
    """Resolves user input updates against recipie.
    """
    resolved = []
    for update_name, update_value in updates:
        # if name is serialized, then it wont have aliases or conditionals?
        # deserialized = update.name.split(".")
        # if len(deserialized) > 1:
        #     resolved.append(models.RegimenUpdate(
        #         name=deserialized,
        #         value=update.value,
        #     ))
        #     continue

        # resolves aliases
        for alias in recipie.aliases:
            if update_name == alias.name:
                resolved.append(
                    (alias.value, update_value, ),
                    # models.RegimenUpdate(
                    #     name=alias.value,
                    #     value=update_value,
                    # )
                )
    for update_name, update_value in resolved:
        # resolves conditionals
        for conditional in recipie.conditionals:
            if update_name == conditional.name:
                resolved.append(
                    resolve_conditional(
                        resolved,
                        conditional,
                    )
                )
    return resolved