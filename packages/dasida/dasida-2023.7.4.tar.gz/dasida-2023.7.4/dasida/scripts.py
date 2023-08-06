import logging
import os

import click
from click_loglevel import LogLevel
from InquirerPy import prompt, inquirer
from tabulate import tabulate

from . import aws

logger = logging.getLogger(__file__)


@click.group()
def dasida():
    pass


################################################################
# AWS SecretsManager
################################################################
@dasida.group()
def secretsmanager():
    pass


@secretsmanager.command()
@click.argument("patterns", default="*")
@click.option("--profile", default=None)
def list(patterns, profile):
    aws.secretsmanager.list_secrets(patterns=patterns, profile_name=profile)


@secretsmanager.command()
@click.argument("secret_name")
@click.option("--profile", default=None)
def get(secret_name, profile):
    secrets = aws.secretsmanager.get_secrets(secret_name=secret_name, profile_name=profile)
    if secrets:
        print(f"Secret '{secret_name}':")
        for k, v in secrets.items():
            print(f" - {k}: {v}")


@secretsmanager.command()
@click.argument("secret_name")
@click.option("--profile", default=None)
def delete(secret_name, profile):
    _ = aws.secretsmanager.delete_secrets(secret_name=secret_name, profile_name=profile)
    print(f"Secret '{secret_name}' is deleted!")


@secretsmanager.command()
@click.argument("secret_name")
@click.option("--profile", default=None)
def create(secret_name, profile):
    if aws.secretsmanager.get_secrets(secret_name=secret_name, profile_name=profile):
        logger.error("Secret '{}' is already exist!".format(secret_name))
        return

    secrets = dict()
    while True:
        key = inquirer.text(message="Key:").execute()
        value = inquirer.text(message="Value:").execute()
        secrets.update({key: value})
        proceed = inquirer.confirm(message="Add New Key-Value?").execute()
        if not proceed:
            break

    print(f"\nAdd new secret '{secret_name}' as follows?:")
    for k, v in secrets.items():
        print(f" - {k}: {v}")

    proceed = inquirer.confirm(message="Confirm?", default=False).execute()
    if proceed:
        _ = aws.secretsmanager.create_secrets(secret_name=secret_name, secrets=secrets, profile_name=profile)
    else:
        logger.error("Abort!")


@secretsmanager.command()
@click.argument("secret_name")
@click.option("--profile", default=None)
def update(secret_name, profile):
    secrets = aws.secretsmanager.get_secrets(secret_name=secret_name, profile_name=profile)
    if not secrets:
        msg = f"Secret name '{secret_name}' not found!"
        raise KeyError(msg)

    new_secrets = dict()
    for k, v in secrets.items():
        key = inquirer.text(message="Key:", default=k).execute()
        value = inquirer.text(message="Value:", default=v).execute()
        if value:
            new_secrets.update({key: value})

    while True:
        proceed = inquirer.confirm(message="Add New Key-Value?").execute()
        if not proceed:
            break
        key = inquirer.text(message="Key:").execute()
        value = inquirer.text(message="Value:").execute()
        new_secrets.update({key: value})

    print(f"\nUpdate secret '{secret_name}' as follows?:")
    for k, v in new_secrets.items():
        print(f" - {k}: {v}")

    proceed = inquirer.confirm(message="Confirm?", default=False).execute()
    if proceed:
        _ = aws.secretsmanager.update_secrets(secret_name=secret_name, secrets=new_secrets, profile_name=profile)
    else:
        logger.error("Abort!")


################################################################
# AWS S3
################################################################
@dasida.group()
def s3():
    pass


# list objects
@s3.command()
@click.option("-b", "--bucket", type=str, required=True, help="S3 Bucket Name.")
@click.option("--prefix", type=str, default=None, help="Object Prefix. Example: 'dataset_a/daily'")
@click.option("--pattern", type=str, default=None, help="Pattern. Example: '2022-*-*-file.csv'")
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="AWS Profile Name.")
def list_objects(bucket, prefix, pattern, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get results
    contents = aws.s3.list_objects(bucket, prefix, pattern, session=session)

    # print results
    path = "/".join([x for x in [bucket, prefix, pattern] if x is not None])
    print(f"ls {path}\n" + tabulate(contents))


# delete objects
@s3.command()
@click.option("-b", "--bucket", type=str, required=True, help="S3 Bucket Name.")
@click.option("--prefix", type=str, default=None, help="Object Prefix. Example: 'dataset_a/daily'")
@click.option("--pattern", type=str, default=None, help="Pattern. Example: '2022-*-*-file.csv'")
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="AWS Profile Name.")
def delete_objects(bucket, prefix, pattern, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get results
    response = aws.s3.delete_objects(bucket, prefix, pattern, session=session)
    if response is None:
        return

    # print results
    path = "/".join([x for x in [bucket, prefix, pattern] if x is not None])

    # logging
    print(f"total {len(response)} objects are deleted from {path}!")


################################################################
# AWS SQS
################################################################
@dasida.group()
def sqs():
    pass


@sqs.command()
@click.option("--prefix", type=str, default=None)
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="Log Level.")
def list_queues(prefix, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get queue urls
    queue_urls = aws.sqs.list_queues(prefix=prefix, session=session)
    print("List of Queues.\n" + tabulate([(q.rsplit("/", 1)[-1], q) for q in sorted(queue_urls)]))


@sqs.command()
@click.argument("queue-name", type=str, default=None)
@click.option("--delete-dlq", type=bool, default=True)
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="Log Level.")
def delete_queue(queue_name, delete_dlq, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get queue urls
    try:
        _ = aws.sqs.delete_queue(queue_name=queue_name, delete_dlq=delete_dlq, session=session)
    except KeyError:
        print(f"No Queue '{queue_name}' was Found. exit!")
        return
    except Exception as ex:
        logger.error(ex)
        return

    print(f"Queue '{queue_name}' is Deleted.")


@sqs.command()
@click.argument("queue-name", type=str, default=None)
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="Log Level.")
def purge_queue(queue_name, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get queue urls
    try:
        _ = aws.sqs.purge_queue(queue_name=queue_name, session=session)
    except KeyError:
        print(f"No Queue '{queue_name}' was Found. exit!")
        return
    except Exception as ex:
        logger.error(ex)
        return

    print(f"Queue '{queue_name}' is Purged.")


@sqs.command()
@click.argument("queue-name", type=str, default=None)
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="Log Level.")
def get_queue_url(queue_name, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get queue urls
    try:
        queue_url = aws.sqs.get_queue_url(queue_name=queue_name, session=session)
    except KeyError:
        print(f"No Queue '{queue_name}' was Found. exit!")
        return
    except Exception as ex:
        logger.error(ex)
        return

    print(f"QueueUrl: {queue_url}")


@sqs.command()
@click.argument("queue-name", type=str, default=None)
@click.option("--delay-seconds", type=int, default=0)
@click.option("--visibility-timeout", type=int, default=60)
@click.option("--dlq_after_received", type=int, default=10, help="Not Create DLQ if This Value is Minus")
@click.option("--profile", type=str, default=None, help="AWS Profile Name.")
@click.option("--log-level", type=LogLevel(), default=logging.INFO, help="Log Level.")
def create_queue(queue_name, delay_seconds, visibility_timeout, dlq_after_received, profile, log_level):
    # set log level
    logger.setLevel(level=log_level)

    # create session
    session = aws.common.session_maker(profile_name=profile)

    # get queue urls
    try:
        response = aws.sqs.create_queue(
            queue_name=queue_name,
            delay_seconds=delay_seconds,
            visibility_timeout=visibility_timeout,
            dlq_after_received=dlq_after_received,
            wait_for_queue_to_ready_sec=60,
            session=session,
        )
    except Exception as ex:
        print(f"Create Queue '{queue_name}' Failed. Exit!")
        logger.error(ex)
        return

    if response is None:
        return
    print(f"Queue '{queue_name}' Created. (QueueUrl: {response['QueueUrl']})")
