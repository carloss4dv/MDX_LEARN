from __future__ import annotations

from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from dataclasses import replace
from typing import TYPE_CHECKING

from _atoti_core import LicenseKeyLocation
from py4j.java_gateway import DEFAULT_ADDRESS
from py4j.protocol import Py4JError

from ._activeviam_client import ActiveViamClient
from ._atoti_client import AtotiClient
from ._create_branding_app_extension import create_branding_app_extension
from ._generate_session_id import generate_session_id
from ._is_jwt_expired import is_jwt_expired
from ._java_api import JavaApi
from .config import SessionConfig

if TYPE_CHECKING:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency
        ServerSubprocess,
    )


def _add_branding_app_extension_to_config(config: SessionConfig, /) -> SessionConfig:
    if config.branding is None:
        return config

    branding_app_extension = create_branding_app_extension(title=config.branding.title)

    return replace(
        config,
        app_extensions={
            **config.app_extensions,
            **branding_app_extension,
        },
    )


def _get_url(*, address: str, https_domain: str | None, port: int) -> str:
    if address == DEFAULT_ADDRESS:
        address = "localhost"

    protocol = "http"

    if https_domain is not None:
        address = https_domain
        protocol = "https"

    return f"{protocol}://{address}:{port}"


@contextmanager
def started_session_resources(
    *,
    address: str | None,
    config: SessionConfig,
    distributed: bool,
    enable_py4j_auth: bool,
    py4j_server_port: int | None,
    start_application: bool,
) -> Generator[tuple[AtotiClient, JavaApi, ServerSubprocess | None, str], None, None]:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency,shortest-import
        ServerSubprocess,
        resolve_license_key,
    )

    if address is None:
        address = DEFAULT_ADDRESS

    for plugin_key, plugin in config.plugins.items():
        config = plugin.session_config_hook(config)
        assert isinstance(
            config,
            SessionConfig,
        ), f"Plugin `{plugin_key}` returned an invalid session config: `{config}`."
    config = _add_branding_app_extension_to_config(config)

    session_id = generate_session_id()

    server_subprocess: ServerSubprocess | None = None

    with ExitStack() as exit_stack:
        try:
            # Attempt to connect to an existing detached process (useful for debugging).
            # Failed attempts are very fast (usually less than 2ms): users won't notice them.
            java_api = exit_stack.enter_context(
                JavaApi.create(
                    address=address,
                    detached=True,
                    distributed=distributed,
                    py4j_auth_token=None,
                    py4j_java_port=py4j_server_port,
                    session_id=session_id,
                ),
            )
            if config.license_key == LicenseKeyLocation.EMBEDDED:
                # Allows debugging the Java side of an Atoti Python SDK test with the same license key as the one set up on the Python side.
                license_key = resolve_license_key(config.license_key)
                assert license_key is not None
                config = replace(config, license_key=license_key)
        # When another Atoti session already created a Py4J server on the default port, trying to attach to it without passing the right `py4j_auth_token` will raise a `Py4JError`.
        # When there are no Atoti sessions or detached processes running, there will be no Py4J server listening on the default port: a `ConnectionRefusedError` will be raised.
        except (ConnectionRefusedError, Py4JError):
            server_subprocess = exit_stack.enter_context(
                ServerSubprocess.create(
                    address=address,
                    enable_py4j_auth=enable_py4j_auth,
                    extra_jars=config.extra_jars,
                    java_options=config.java_options,
                    license_key=config.license_key,
                    logs_destination=config.logging.destination
                    if config.logging
                    else None,
                    port=config.port,
                    py4j_server_port=py4j_server_port,
                    session_id=session_id,
                ),
            )
            java_api = exit_stack.enter_context(
                JavaApi.create(
                    address=address,
                    detached=False,
                    distributed=distributed,
                    py4j_auth_token=server_subprocess.py4j_auth_token,
                    py4j_java_port=server_subprocess.py4j_java_port,
                    session_id=session_id,
                ),
            )

        if start_application:
            try:
                java_api.start_application(config)
            except Exception as error:  # noqa: BLE001
                raise RuntimeError(
                    f"An error occurred while starting the session:\n{error}",
                ) from None

        jwt_key = "key"
        jwt_holder: dict[str, str | None] = {"jwt": None}

        def get_jwt() -> str:
            jwt = jwt_holder.get(jwt_key)
            if not jwt or is_jwt_expired(jwt):
                jwt_holder[jwt_key] = java_api.generate_jwt()
            jwt = jwt_holder[jwt_key]
            assert jwt
            return jwt

        url = _get_url(
            address=address,
            https_domain=config.security.https.domain
            if config.security and config.security.https
            else None,
            port=java_api.get_session_port(),
        )

        with ActiveViamClient.create(
            url,
            authentication=lambda _url: {"Authorization": f"Jwt {get_jwt()}"},
            certificate_authority=config.security.https.certificate_authority
            if config.security and config.security.https
            else None,
            ping=not distributed,
        ) as activeviam_client:
            atoti_client = AtotiClient(activeviam_client=activeviam_client)
            yield atoti_client, java_api, server_subprocess, session_id
