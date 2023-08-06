import re
import os
import json
import yaml
import shutil
import pickle
import random
import typing
import tempfile
import requests
import enum
import logging
import hashlib
import pathlib

from . import exceptions


logger = logging.getLogger(__name__)


def _generate_random_labtracks_id() -> int:
    # helper function
    # must be a 6 digit integer, cant be 999999 due special api handling for 999999
    return random.randint(100000, 999998)


# cant type hint client due to awkward import order...
def autogenerate_labtracks_id(client, max_tries=100) -> int:
    """Utility function for autogenerating a labtracks_id that doesn't already exist.
    """
    for n in range(max_tries):
        labtracks_id = _generate_random_labtracks_id()
        try:
            client.get(
                entity_name="subjects",
                filter_property_name="LabTracks_ID",
                filter_operator="eq",
                filter_property_value=labtracks_id,
            )
        except exceptions.NotFoundError:
            return labtracks_id

    else:
        raise Exception(
            "Failed to autogenerate a labtracks_id after %s tries." % n)


def generate_mtrain_lims_upload_bundle(api_base: str, username: str, password: str, foraging_id: str, session_filepath: str) -> typing.Tuple[str, str, str, typing.Callable]:
    temp_dir = tempfile.TemporaryDirectory()

    input_json_path = os.path.join(temp_dir.name, "input.json")
    with open(input_json_path, "w") as f:
        json.dump({
            "inc": {
                "API_BASE": api_base,
                "foraging_id": foraging_id,
                "foraging_file_name": session_filepath,
            }
        }, f)

    # generate secrets file required by mtrain_lims
    mtrain_secrets_path = os.path.join(temp_dir.name, "mtrain_secrets.yml")
    with open(mtrain_secrets_path, "w") as f:
        yaml.dump({
            "username": username,
            "password": password,
        }, f)

    return input_json_path, os.path.join(temp_dir.name, "output.json"), temp_dir.name, lambda: temp_dir.cleanup()


def replace_behavior_session_metadata_dynamic_routing(path: str, labtracks_id: int) -> str:
    """Replace dynamic routing metadata required for an mtrain v2 session upload
    """
    upload_filename = os.path.basename(path)
    # subject id must be serialized in upload filepath
    renamed_upload_filepath = re.sub(
        # this regex isnt great but this is just test code okay...
        r"DynamicRouting1_(\d{6})",
        f"DynamicRouting1_{labtracks_id}",
        upload_filename,
    )
    assert not os.path.isfile(
        renamed_upload_filepath), "Renamed upload shouldnt exist yet."
    shutil.copy(path, renamed_upload_filepath)
    assert os.path.isfile(
        renamed_upload_filepath), "Renamed upload should exist."
    return renamed_upload_filepath


def replace_behavior_session_metadata_doc(path: str, labtracks_id: int, foraging_id: str) -> str:
    """Replace doc metadata required for an mtrain v1 session upload
    """
    upload_filename = os.path.basename(path)
    # subject id must be serialized in upload filepath
    deserialized = os.path.splitext(upload_filename)[0].split("_")
    renamed_upload_filepath = f"{deserialized[0]}_{labtracks_id}_{foraging_id}.pkl"
    assert not os.path.isfile(
        renamed_upload_filepath), "Renamed upload shouldnt exist yet."
    shutil.copy(path, renamed_upload_filepath)
    assert os.path.isfile(
        renamed_upload_filepath), "Renamed upload should exist."

    with open(renamed_upload_filepath, "rb") as f:
        data = pickle.load(f, encoding="latin1")

    data["session_uuid"] = foraging_id
    # overwrite mouse_id everywhere vba looks
    data["items"]["behavior"]["params"]["mouse_id"] = labtracks_id
    data["items"]["behavior"]["cl_params"]["mouse_id"] = labtracks_id
    data["items"]["behavior"]["config"]["behavior"]["mouse_id"] = labtracks_id

    with open(renamed_upload_filepath, "wb") as f:
        pickle.dump(data, f, protocol=0)

    return renamed_upload_filepath


def replace_behavior_session_metadata_passive(path: str, output_filepath: str, labtracks_id: int, session_id: str) -> str:
    with open(path, "rb") as f:
        data = pickle.load(path, encoding="latin1")

    data["mouse_id"] = labtracks_id
    data["session_uuid"] = session_id

    with open(output_filepath, "wb") as f:
        pickle.dump(data, f, protocol=0)

    return output_filepath


def get_regimen_from_github(tag_name: str, github_uri_template="https://raw.githubusercontent.com/AllenInstitute/mtrain_regimens/%s/regimen.yml") -> typing.Dict:
    result = requests.get(github_uri_template % tag_name)
    result.raise_for_status()
    return yaml.load(
        result.content,
        Loader=yaml.FullLoader,
    )


class UpdateType(enum.Enum):
    patch = "patch"
    minor = "minor"
    major = "major"

def generate_regimen_version(current_version: str, update_type: UpdateType = UpdateType.patch) -> str:
    deserialized = current_version.split("_")
    version = deserialized[-1]
    logger.debug("Inferred version: %s" % version)
    major_version, minor_version, patch_version = \
    list(map(
        lambda version_str: int(version_str),
        version.lstrip("v").split("."),
    ))
    logger.debug("Parsed versions: major=%s minor=%s patch=%s" % (major_version, minor_version, patch_version))
    if update_type == UpdateType.patch:
        patch_version += 1
    elif update_type == UpdateType.minor:
        minor_version += 1
        patch_version = 0
    elif update_type == UpdateType.major:
        major_version += 1
        patch_version = 0
        minor_version = 0
    else:
        raise ValueError("Unexpected update_type: %s" % update_type)
    deserialized[-1] = f"v{major_version}.{minor_version}.{patch_version}"
    updated_version = "_".join(deserialized)
    return updated_version

def resolve_stage_name(regimen_record: typing.Dict, state_id: str) -> str:
    source_states = list(filter(
        lambda state: state["id"] == state_id,
        regimen_record["states"],
    ))
    if not len(source_states) == 1:
        raise Exception("Only one stage should be returned. source_states=%s" % source_states)
    source_stages = list(filter(
        lambda stage: stage["id"] == source_states[0]["stage_id"],
        regimen_record["stages"],
    ))
    if not len(source_stages) == 1:
        raise Exception("Only one stage should be returned. source_stages=%s" % source_stages)
    return source_stages[0]["name"]


def generate_script_checksum(script_uri: str) -> str:
    response = requests.get(script_uri)
    if response.status_code not in (200, ):
        response.raise_for_status()
    return hashlib.md5(response.content).hexdigest()


def resolve_update_name(serialized: str) -> list[str]:
    """Splits update name into its constituent parts.
    """
    return serialized.split(".")