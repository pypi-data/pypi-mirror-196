##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json

from .Machine import Machine

from optumi_core.exceptions import (
    OptumiException,
)


class Machines:
    """A class for retrieving a list of dynamically allocated machines."""

    @classmethod
    def list(cls, status: str = None):
        """Obtain a list of all allocated machines optionally matching a given status.

        Args:
            status (str, optional): The status of the machine to match as one of "Acquiring", "Configuring", "Busy", "Idle", "Releasing". Defaults to None.

        Raises:
            OptumiException: Raised if an unrecognized status is provided.

        Returns:
            list of machines: A list of Machine objects matching any given status.
        """
        if status != None and not status in Machine.status_values:
            raise OptumiException("Unexpected machine status '" + status + "', expected one of " + str(Machine.status_values))

        machines = []

        response = json.loads(optumi.core.get_machines().text)

        for machine in response["machines"]:
            machine = Machine(*Machine.reconstruct(machine))
            if (status is None and machine.is_visible()) or (machine.status == status):
                machines.append(machine)

        return machines
