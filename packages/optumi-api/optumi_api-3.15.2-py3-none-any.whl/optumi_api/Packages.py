##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


class Packages(list):
    """A class for specifying the Python packages that must be installed before running a workload."""

    def __init__(self, packages: list = []):
        """Constructor to initialize the package list required by the workload.

        Args:
            packages (list, optional): List of packages to install before running a workload. Defaults to [].
        """
        super().__init__(packages)

    def __str__(self):
        return str(self.packages)
