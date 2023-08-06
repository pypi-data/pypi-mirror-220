# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

from apistar.exceptions import ErrorResponse

from arkindex_cli.auth import Profiles
from arkindex_cli.git import LocalGitRepository

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def add_publish_parser(subcommands) -> None:
    recover_parser = subcommands.add_parser(
        "publish",
        description="Publish an available worker version, creating its Git stack (repository, revision, worker) if required",
        help="Publish an available worker version, creating its Git stack (repository, revision, worker) if required",
    )
    recover_parser.add_argument(
        "docker_image_tag",
        help="Tag of the Docker image to be published on the new worker version",
    )
    recover_parser.add_argument(
        "--worker-slug",
        help="Slug of the worker to be used (or created) to publish the new worker version",
        required=True,
    )
    recover_parser.add_argument(
        "--configuration-path",
        help="Path to a JSON file containing the configuration for the new worker version",
        type=Path,
        required=True,
    )
    recover_parser.add_argument(
        "--repository-url",
        help=(
            "URL of the Git project repository containing the worker. "
            "If unset, the repository is automatically detected from the current directory."
        ),
    )
    recover_parser.add_argument(
        "--revision-hash",
        help="",
    )
    recover_parser.add_argument(
        "--revision-message",
        help="",
    )
    recover_parser.add_argument(
        "--revision-author",
        help="",
    )
    recover_parser.add_argument(
        "--revision-branch",
        help="",
    )
    recover_parser.add_argument(
        "--revision-tags",
        nargs="+",
        help="",
    )
    recover_parser.add_argument(
        "--gpu",
        choices=("disabled", "supported", "required"),
        default="disabled",
        help="",
    )
    recover_parser.add_argument(
        "--requires-model",
        action="store_true",
        help="",
    )
    recover_parser.set_defaults(func=run)


def run(
    *,
    docker_image_tag,
    worker_slug,
    configuration_path,
    repository_url,
    revision_hash,
    revision_message,
    revision_author,
    revision_branch,
    revision_tags,
    gpu,
    requires_model,
    profile_slug=None,
) -> None:

    try:
        with configuration_path.open("r") as f:
            configuration = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"could not read JSON configuration at {configuration_path}: {e}"
        )

    local_repo = LocalGitRepository()

    if repository_url is None:
        logger.info("Identifying repository from the current directory")
        repository_url = local_repo.url
    if revision_hash is None:
        revision_hash = local_repo.hash
    if revision_message is None:
        revision_message = local_repo.message
    if revision_author is None:
        revision_author = local_repo.author
    if revision_branch is None:
        revision_branch = local_repo.branch
    if revision_tags is None:
        revision_tags = local_repo.tags

    logger.info("Building a new worker version:")
    logger.info(f" * Repository : {repository_url}")
    logger.info(f" * Revision : {revision_hash}")
    logger.info(f" * Message : {revision_message}")
    logger.info(f" * Author : {revision_author}")
    logger.info(f" * Branch: {revision_branch}")
    logger.info(f" * Tags: {revision_tags}")

    references = [{"type": "branch", "name": revision_branch}]
    references.extend([{"type": "tag", "name": val} for val in revision_tags])

    logger.info("Pushing new version to Arkindex")

    profiles = Profiles()
    profile = profiles.get_or_exit(profile_slug)
    api_client = profiles.get_api_client(profile)

    try:
        worker_version = api_client.request(
            "CreateDockerWorkerVersion",
            body={
                "docker_image_iid": docker_image_tag,
                "repository_url": repository_url,
                "worker_slug": worker_slug,
                "revision_hash": revision_hash,
                "revision_message": revision_message,
                "revision_author": revision_author,
                "revision_references": references,
                "gpu_usage": gpu,
                "model_usage": requires_model,
                "configuration": configuration,
            },
        )
    except ErrorResponse as e:
        logger.error(f"An error occurred: [{e.status_code}] {e.content}")
    else:
        logger.info(f"Successfully pushed version {worker_version['id']}")
