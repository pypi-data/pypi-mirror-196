##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .api import providers, machines

from optumi_core.exceptions import (
    OptumiException,
)


# Support embedding the provider in the machine string, have no default provider argument
class Server:
    """A class specifying a server with specific machine capabilities from a given cloud provider."""

    def __init__(self, size: str = "Standard_NC4as_T4_v3", provider: str = "Azure"):
        """Constructor for the Server object.

        Args:
            size (str, optional): The machine size, e.g., 'Standard_NC4as_T4_v3'. If the size string contains a colon (':'), then the first part of the string is treated as the provider name and the second part of the string is treated as the size name. Available sizes can be listed using machines(). Defaults to "Standard_NC4as_T4_v3".
            provider (str, optional): The name of the provider for the server, e.g., 'Azure'. Defaults to "Azure".

        Raises:
            OptumiException: Raised if an unexpected provider or size is specified.
        """
        if ":" in size:
            s = size.split(":")
            self._provider = s[0].lower()
            self._size = s[1].lower()
        else:
            self._provider = provider.lower()
            self._size = size.lower()

        if not self._provider in [x.lower() for x in providers()]:
            raise OptumiException("Unexpected provider '" + self._provider + "', expected one of " + str(providers()))

        if not self._provider + ":" + self._size in [x.lower() for x in machines()]:
            raise OptumiException("Unexpected machine size '" + self._provider + ":" + self._size + "', expected one of " + str(machines()))

    @property
    def provider(self):
        """Obtain the cloud provider name.

        Returns:
            str: The name of the cloud provider for the allocated machine.
        """
        return self._provider

    @property
    def size(self):
        """Obtain the server size.

        Returns:
            str: The size of the allocated machine.
        """
        return self._size

    def __str__(self):
        return str(self.provider) + ":" + str(self.size)
