"""Containers module."""

import logging.config
from datetime import datetime

from dependency_injector import containers, providers

from Logging.eventlogger import EventLogger
from Services.BaseService import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logger = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini"
    )

    event_logger = providers.Singleton(EventLogger)

    user_service = providers.Factory(UserService)
