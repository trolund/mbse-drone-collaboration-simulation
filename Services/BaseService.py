import logging
from typing import Dict


class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.logger.debug("BaseService")


class UserService(BaseService):

    def __init__(self) -> None:
        super().__init__()
        self.logger.debug("UserService")

    def get_user(self, email: str) -> Dict[str, str]:
        self.logger.debug("User %s has been found in database", email)
        return {"email": email, "password_hash": "..."}