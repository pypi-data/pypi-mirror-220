import typing
import yaml
import pydantic
import pathlib
import logging


logger = logging.getLogger(__name__)


class Stage(pydantic.BaseModel):
    
    script: str
    script_md5: str
    parameters: typing.Dict[str, typing.Any]


Condition = typing.Union[str, typing.List[str]]

class Transition(pydantic.BaseModel):

    trigger: typing.Optional[str]
    source: str
    dest: str
    conditions: typing.Optional[Condition] = None
    unless: typing.Optional[Condition] = None


class Regimen(pydantic.BaseModel):
    
    name: str
    stages: typing.Dict[str, Stage]
    transitions: typing.List[Transition]
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> "Regimen":
        # regimen_dict = yaml.load(
        #     pathlib.Path(yaml_str).read_text(),
        #     Loader=yaml.FullLoader,
        # )
        with open(yaml_str, "r") as f:
            regimen_dict = yaml.safe_load(f.read())
        
        return cls.from_dict(regimen_dict)
    
    @classmethod
    def from_dict(cls, regimen_dict: dict[str, typing.Any]) -> "Regimen":
        logger.setLevel(logging.DEBUG)
        logger.debug("regimen_dict: %s" % regimen_dict)
        return cls(
            name=regimen_dict["name"],
            transitions=[
                Transition(**transition_dict)
                for transition_dict in regimen_dict["transitions"]
            ],
            stages={
                stage_id: Stage(**stage_dict)
                for stage_id, stage_dict in regimen_dict["stages"].items()
            }
        )
    

class RegimenUpdate(pydantic.BaseModel):

    name: list[str]
    value: typing.Any

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     if isinstance(self.name, str):
    #         self.name = data["name"].split(".")
    #     self.value = data["value"]


class RegimenUpdateConditionalParam(pydantic.BaseModel):
    
    name: list[str]
    value: typing.Optional[typing.Any] = None
    is_property: typing.Optional[bool] = False


class RegimenUpdateConditional(pydantic.BaseModel):
    
    name: list[str]
    op: str
    params: list[RegimenUpdateConditionalParam]
    prop_name: list[str]


class RegimenUpdateAlias(pydantic.BaseModel):
    
    name: str
    value: list[str]


class RegimenUpdateRecipie(pydantic.BaseModel):

    name: str
    aliases: list[RegimenUpdateAlias]
    conditionals: list[RegimenUpdateConditional]
    api_base: str
    username: str
    password: str
    access_token: str
    github_repo_name: str

    @classmethod
    def from_dict(cls, d: dict) -> "RegimenUpdateRecipie":
        return cls(
            name=d["name"],
            api_base=d["api_base"],
            username=d["username"],
            password=d["password"],
            access_token=d["access_token"],
            github_repo_name=d["github_repo_name"],
            aliases=[
                RegimenUpdateAlias(**alias)
                for alias in d["aliases"]
            ],
            conditionals=[
                RegimenUpdateConditional(
                    name=conditional["name"],
                    op=conditional["op"],
                    params=[
                        RegimenUpdateConditionalParam(
                            **regimen_update_conditional_param,
                        )
                        for regimen_update_conditional_param in conditional.get("params", [])
                    ],
                    prop_name=conditional["prop_name"],
                )
                for conditional in d["conditionals"]
            ],
        )
