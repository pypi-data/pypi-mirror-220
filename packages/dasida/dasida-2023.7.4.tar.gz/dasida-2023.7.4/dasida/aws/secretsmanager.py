import ast
import base64
import fnmatch
import json
import logging
from typing import Union, List

import boto3
from botocore.exceptions import ClientError
from rich import print

from .common import session_maker

logger = logging.getLogger(__file__)


################################################################
# HELPERS
################################################################
# _get_secrets
def _get_secrets(client, secret_name):
    # get secrets
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        description = ERROR_DESCRIPTIONS.get(code, "unknown").replace("\n", " ")
        if code == "ResourceNotFoundException":
            logger.info(f"{code}: secret '{secret_name}' not found! return None.")
            return None
        logger.error(f"{code}: {description}")
        raise e
    else:
        if "SecretString" in get_secret_value_response:
            secrets = get_secret_value_response["SecretString"]
            try:
                secrets = json.loads(secrets)
            except json.JSONDecodeError:
                try:
                    secrets = ast.literal_eval(secrets)
                except SyntaxError as ex:
                    pass
            except Exception as ex:
                logger.error(f"[DASIDA] Cannot Decode JSON, {secrets}")
        else:
            secrets = base64.b64decode(get_secret_value_response["SecretBinary"])

    return secrets


################################################################
# FUNCTIONS
################################################################
# list secrets
def list_secrets(
    patterns: Union[str, list] = "*",
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """
    (TODO)
      - filter tags
    """
    # correct args
    if patterns:
        patterns = patterns if isinstance(patterns, (tuple, list)) else [patterns]

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    # get secrets
    opts = {"MaxResults": 100}
    secrets = []
    while True:
        response = client.list_secrets(**opts)
        secrets += response.get("SecretList", [])
        next_token = response.get("NextToken")
        if next_token is None:
            break
        opts.update({"NextToken": next_token})

    for secret in secrets:
        secret_name = secret["Name"]
        if not any([fnmatch.fnmatch(secret_name, f"*{pat.strip('*')}*") for pat in patterns]):
            continue
        try:
            body = _get_secrets(client, secret_name)
        except Exception as ex:
            print(f"[FAIL] {secret_name}")
        print(f"[[bold]{secret['Name']}[/bold]]")
        if secret.get("Description"):
            print(f" DESCRIPTION: {secret['Description']}")
        print(" VALUES:")
        if isinstance(body, dict):
            for k, v in body.items():
                print(f"  - {k}: {v}")
        else:
            print(f"  - {body}")


# get secrets
def get_secrets(
    secret_name: str,
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """Get secrets from AWS SecretsManager.

    Example
    -------
    >>> conf = get_secrets("some/secrets")
    """

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    return _get_secrets(client, secret_name)


# create secrets
def create_secrets(
    secret_name: str,
    secrets: Union[str, dict],
    description: str = None,
    tags: List[dict] = None,
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """Create secrets from AWS SecretsManager.

    Example
    -------
    >>> create_secrets("some/secrets")
    """

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    if isinstance(secrets, dict):
        secrets = json.dumps(secrets)

    opts = {"Name": secret_name, "SecretString": secrets}
    if description:
        opts.update({"Description": description})
    if tags:
        opts.update({"Tags": tags})

    response = client.create_secret(**opts)

    return response


# update secrets
def update_secrets(
    secret_name: str,
    secrets: Union[str, dict] = None,
    description: str = None,
    tags: List[dict] = None,
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """Update secrets from AWS SecretsManager.

    Example
    -------
    >>> update_secrets("some/secrets")
    """

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    opts = {"SecretId": secret_name}
    new_opts = dict()
    if secrets:
        if isinstance(secrets, dict):
            secrets = json.dumps(secrets)
        new_opts.update({"SecretString": secrets})
    if description:
        new_opts.update({"Description": description})
    if tags:
        new_opts.update({"Tags": tags})

    if not new_opts:
        logger.warning("Nothing to update. Exit!")

    opts.update(new_opts)
    response = client.update_secret(**opts)

    return response


# put secrets
def put_secrets(
    secret_name: str,
    secrets: Union[str, dict] = None,
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """Update secrets from AWS SecretsManager.

    Example
    -------
    >>> put_secrets("some/secrets")
    """

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    if isinstance(secrets, dict):
        current_secrets = get_secrets(secret_name, session=session)
        current_secrets.update(secrets)
        secrets = json.dumps(current_secrets)

    opts = {"SecretId": secret_name, "SecretString": secrets}
    response = client.put_secret_value(**opts)

    return response


# delete secrets
def delete_secrets(
    secret_name: str,
    recovery_window_in_days: int = None,
    force_delete_without_recovery: bool = None,
    profile_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str = "ap-northeast-2",
    load_docker_secret: bool = True,
    session: boto3.Session = None,
):
    """Create secrets from AWS SecretsManager.

    Example
    -------
    >>> create_secrets("some/secrets")
    """

    # get client
    session = session or session_maker(
        profile_name=profile_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        load_docker_secret=load_docker_secret,
    )
    client = session.client("secretsmanager")

    opts = {"SecretId": secret_name}
    if recovery_window_in_days:
        opts.update({"RecoveryWindowInDasy": recovery_window_in_days})
    if force_delete_without_recovery:
        opts.update({"ForceDeleteWithoutRecovery": force_delete_without_recovery})

    response = client.delete_secret(**opts)

    return response


# errors
ERROR_DESCRIPTIONS = {
    "DecryptionFailureException": """\
    Secrets Manager can't decrypt the protected secret text using the provided KMS key.""",
    "InternalServiceErrorException": """\
    An error occurred on the server side.""",
    "InvalidParameterException": """\
    You provided an invalid value for a parameter.""",
    "InvalidRequestException": """\
    You provided a parameter value that is not valid for the current state of the resource.""",
    "ResourceNotFoundException": """\
    We can't find the resource that you asked for.""",
}
