# Copyright 2023 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import os
from . import logger

class ClientConfig():
    """Global configuration for the Python client communicating with a running Cegal Hub Server. This is used primarily with ConnectionParameters objects.
    When a ConnectionParameters object is created but no values are provided, the ConnectionParameters object will rely on the ClientConfig and ServerConfig 
    global configurations for defaults.
    """

    __use_auth: bool = None
    __user_access_token: str = None

    @staticmethod
    def set_use_auth(use_auth: bool):
        """Update the ClientConfig to use auth or not.

        Args:
            use_auth (bool): True to indicate authentication should be used, False otherwise.
        """        
        ClientConfig.__use_auth = use_auth

    @staticmethod
    def get_use_auth():
        """Get the configuration for whether or not to use authentication. This will look for an environment variable called CEGAL_HUB_USE_AUTH
        which it will expect to be set to True or False.

        Returns:
            [bool]: Whether or not to use authentication.
        """  
        if ClientConfig.__use_auth is None:
            val = ClientConfig.__get_envvar("CEGAL_HUB_USE_AUTH")
            if val[0]:
                return val[1].lower() == "true"
            else:
                return False
        else:
            return ClientConfig.__use_auth

    @staticmethod
    def set_user_access_token(token: str):
        """Set the predefined user access token.

        Args:
            token (str): The access token to use. Set to None to clear the user access token and restore the default behaviour
        """
        ClientConfig.__user_access_token = token

    @staticmethod
    def get_user_access_token() -> str:
        """Get a predefined user access token if defined.

        Returns:
            [str]: The access token, if None no user access token is defined
        """
        return ClientConfig.__user_access_token

    @staticmethod
    def __get_envvar(key: str):
        env = os.environ
        try:
            return (True, env[key])
        except:
            return (False, "")

    @staticmethod
    def __repr__():
        return "use auth:" + repr(ClientConfig.get_use_auth())
