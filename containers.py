"""Containers module."""

import logging.config

from dependency_injector import containers, providers

from Services.BaseService import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    user_service = providers.Factory(UserService)
