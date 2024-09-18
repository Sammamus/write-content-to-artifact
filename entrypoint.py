#!/usr/bin/env python

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("artifactor")

import os
import re
import json
import uuid

# Globals
workspace_path = "/github/workspace/"
artifact_folder = "artifacts/"
file_prefix = "artifact"
file_uuid = str(uuid.uuid4().hex)
file_suffix = ".json"
file_name = f"{file_prefix}_{file_uuid}{file_suffix}"
file_path = f"{workspace_path}{artifact_folder}{file_name}"
output = f"{artifact_folder}{file_name}"
content = ""

def get_content_filler():
    return {
        "dummy_data01": str(uuid.uuid4()),
        "dummy_data02": str(uuid.uuid4()),
        "dummy_data03": str(uuid.uuid4()),
        "dummy_data04": str(uuid.uuid4()),
        "dummy_data05": str(uuid.uuid4()),
        "dummy_data06": str(uuid.uuid4()),
        "content": content
    }


def create_file_content():

    file_content = {
        "metadata": []
    }

    filler_ammount = 10
    count = 0

    while count <= filler_ammount:
        file_content['metadata'].append(get_content_filler())
        count += 1

    return file_content


def write_file():
    file_content = create_file_content

    with open(file_path, 'w') as f:
        f.write(json.dumps(file_content, indent=2))

    f.close()


def get_env_variables():
    output = {}

    pattern = r'^INPUT_\w*'
    for key, val in os.environ.items():
        if re.match(pattern, key):
            output.update({key: val})

    return output


def set_globals():
    global content

    variables = get_env_variables()

    content = variables.get("INPUT_CONTENT", None)

    if content == "" or content is None:
        raise Exception("Missing content input")
    

def set_output(name, value):
    github_output_file = "GITHUB_OUTPUT"
    if github_output_file in os.environ:
        with open(os.environ[github_output_file], 'a') as f:
            print(f"{name}={value}", file=f)

    else:
        print(f"::set-output name={name}::{value}")


def main():
    try:
        set_globals()
        write_file()
        set_output("filepath", output)

        exit(0)

    except Exception as e:
        logger.exception(e)
        exit(1)


if __name__ == "__main__":
    main()