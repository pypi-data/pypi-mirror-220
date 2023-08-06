import json
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

import click
import docker
import jwt
import toml
from click import ClickException
from jwt.exceptions import ExpiredSignatureError

from . import exc
from .config import Config
from .services.auth import AuthService
from .services.deployments import (
    DeployRequest,
    DeployServerlessRequest,
    DeploymentServiceV1,
)
from .services.users import UserServiceV1


_pyproject_toml = toml.load(Path(__file__).resolve().parent.parent / "pyproject.toml")


def update_core_api_credentials(access_token, refresh_token):
    config = Config()
    with open(config.credentials_path, "w") as f:
        f.write(f"COMPUTEX_CORE_API_ACCESS_TOKEN={access_token}\n")
        f.write(f"COMPUTEX_CORE_API_REFRESH_TOKEN={refresh_token}\n")


def refresh_credentials(f):
    """Automatically updates access and refresh tokens if needed."""

    @wraps(f)
    def inner(*args, **kwargs):
        config = Config()
        if not (config.core_api_access_token and config.core_api_refresh_token):
            raise exc.UnauthenticatedException()
        try:
            # Verify Access Token Isn't Expired
            # TODO: We should always use public key verification via RS256.
            #       This can be enforced after the encryption algorithm
            #       is changed to RS256 in the Core API.
            if config.core_api_public_key is None:
                token = jwt.decode(
                    config.core_api_access_token,
                    algorithms=["HS256"],
                    options=dict(verify_signature=False),
                )
                if token["exp"] < datetime.now(timezone.utc).timestamp():
                    raise ExpiredSignatureError()
            else:
                jwt.decode(
                    config.core_api_access_token,
                    config.core_api_public_key,
                    algorithms=["RS256"],
                )
        except ExpiredSignatureError:
            # Verify Refresh Token Isn't Expired
            try:
                # TODO: We should always use public key verification via RS256.
                #       This can be enforced after the encryption algorithm
                #       is changed to RS256 in the Core API.
                if config.core_api_public_key is None:
                    token = jwt.decode(
                        config.core_api_refresh_token,
                        algorithms=["HS256", "RS256"],
                        options=dict(verify_signature=False),
                    )
                    if token["exp"] < datetime.now(timezone.utc).timestamp():
                        raise ExpiredSignatureError()
                else:
                    jwt.decode(
                        config.core_api_refresh_token,
                        config.core_api_public_key,
                        algorithms=["RS256"],
                    )
            except ExpiredSignatureError:
                raise exc.RefreshTokenExpiredException()
            auth_service = AuthService()
            r = auth_service.refresh(
                config.core_api_access_token, config.core_api_refresh_token
            )
            update_core_api_credentials(r.access_token, r.refresh_token)
        return f(*args, **kwargs)

    return inner


@click.group()
@click.version_option(version=_pyproject_toml["tool"]["poetry"]["version"])
def cli():
    pass


@cli.command()
def info():
    config = Config()
    click.echo(json.dumps(config.dict(), indent=4))


@cli.command()
@click.option(
    "--username", help="Your ComputeX email or username (env: COMPUTEX_USERNAME)."
)
@click.option("--password", help="Your ComputeX password (env: COMPUTEX_PASSWORD).")
def login(username, password):
    config = Config()
    username = username or config.username
    password = password or config.password
    if not (username and password):
        raise ClickException("You must provide both --username and --password options.")
    login_response = UserServiceV1().login(username, password)
    update_core_api_credentials(
        login_response.access_token, login_response.refresh_token
    )
    click.echo("Successfully logged in. Welcome to CX.")


@cli.command()
@click.option("--app", help="Your app's name.")
@click.option(
    "--image", help="A container image name that has been pushed to ComputeX."
)
@click.option("--num-cpu-cores", default=4, help="Number of CPU cores.")
@click.option("--num-gpu", default=1, help="Number of GPUs.")
@click.option(
    "--gpu", default="A40", help="The type of GPU you'd like to use."
)  # TODO: Add listing of SKUs
# @click.option(
#     "--cpu", default="intel_xeon_v3", help="The type of CPU you'd like to use."
# )
@click.option("--memory", default=4, help="Memory in GB to allocate.")
@click.option("--replicas", default=1, help="Number of replicas to use.")
@refresh_credentials
def deploy(
    app,
    image,
    num_cpu_cores,
    num_gpu,
    gpu,
    # cpu,
    memory,
    replicas,
):
    # TODO: Verify that image exists before deployment.
    r = UserServiceV1().get_registry_credentials()
    r = DeployRequest(
        app_name=app,
        container_image=f"{r.registry_host}/{r.registry_namespace}/{image}",
        num_cpu_cores=num_cpu_cores,
        num_gpu=num_gpu,
        gpu=gpu,
        # cpu_sku=cpu_sku,
        memory=memory,
        replicas=replicas,
    )
    DeploymentServiceV1().deploy(r)
    click.echo("Your app has successfully deployed.")


@cli.command()
@click.option("--app", help="Your app's name.")
@click.option(
    "--image", help="A container image name that has been pushed to ComputeX."
)
@click.option("--num-cpu-cores", default=4, help="Number of CPU cores.")
@click.option("--num-gpu", default=1, help="Number of GPUs.")
@click.option(
    "--gpu", default="A40", help="The type of GPU you'd like to use."
)  # TODO: Add listing of SKUs
# @click.option(
#     "--cpu", default="intel_xeon_v3", help="The type of CPU you'd like to use."
# )
@click.option("--memory", default=4, help="Memory in GB to allocate.")
@click.option(
    "--concurrency",
    default=1,
    help="Represents the number of simultaneous requests sent to a single backend pod at a given time. For GPU inference, this should usually be set to 1. For CPU-based non-blocking requests, this number can be reasonably high, i.e. 100.",
)
@click.option(
    "--min-scale", default=0, help="Minimum concurrent serverless invocations."
)
@click.option(
    "--max-scale", default=1, help="Maximum concurrent serverless invocations."
)
@click.option("--public", is_flag=True, default=False)
@refresh_credentials
def deploy_serverless(
    app: str,
    image: str,
    num_cpu_cores: int,
    num_gpu: int,
    gpu: str,
    # cpu: str,
    memory: int,
    concurrency: int,
    min_scale: int,
    max_scale: int,
    public: bool,
):
    # TODO: Verify that image exists before deployment.
    r = UserServiceV1().get_registry_credentials()
    r = DeployServerlessRequest(
        app_name=app,
        container_image=f"{r.registry_host}/{r.registry_namespace}/{image}",
        num_cpu_cores=num_cpu_cores,
        num_gpu=num_gpu,
        gpu=gpu,
        # cpu_sku=cpu_sku,
        memory=memory,
        concurrency=concurrency,
        min_scale=min_scale,
        max_scale=max_scale,
    )
    DeploymentServiceV1().deploy_serverless(r, is_public=public)
    click.echo("Your app has successfully deployed.")


@cli.command()
@refresh_credentials
def list_deployments():
    deployments = DeploymentServiceV1().list()
    click.echo(json.dumps(deployments.dict(), indent=4))


@cli.command()
@click.option("--app", help="Your app's name.")
@refresh_credentials
def delete_deployment(app):
    r = DeploymentServiceV1().delete(app)
    click.echo(json.dumps(r.dict(), indent=4))


@cli.command()
@click.argument("image")
@refresh_credentials
def push(image):
    r = UserServiceV1().get_registry_credentials()
    client = docker.from_env()
    client.login(
        username=r.registry_username,
        password=r.registry_password,
        registry=r.registry_host,
    )
    client.images.tag(image, f"{r.registry_host}/{r.registry_namespace}/{image}")
    client.images.push(f"{r.registry_host}/{r.registry_namespace}/{image}")


@cli.command()
@click.option("--app")
@refresh_credentials
def logs(app):
    r = DeploymentServiceV1().logs(app)
    click.echo(json.dumps(r.json(), indent=4))


@cli.command()
@click.option("--app")
@click.option("--data")
@click.option("--is-public", default=False)
@click.option("--is-serverless", default=False)
@refresh_credentials
def predict(app, data, is_public, is_serverless):
    data_dict = json.loads(data)
    r = DeploymentServiceV1().predict(
        app, data_dict, is_serverless=is_serverless, is_public=is_public
    )
    click.echo(json.dumps(r.dict(), indent=4))


if __name__ == "__main__":
    cli()
