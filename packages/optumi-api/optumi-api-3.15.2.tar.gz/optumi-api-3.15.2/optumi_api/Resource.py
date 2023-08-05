##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .api import graphics_card_types
from typing import Union

from optumi_core.exceptions import (
    OptumiException,
)


class Resource:
    """A class for creating resource specifications to be used when running scripts, notebooks or containers."""

    def __init__(self, gpu: Union[bool, str] = True, memory_per_card=0):
        """Constructor for a Resource object.

        Args:
            gpu (Union[bool, str]): The type of graphics card to be used, either True to allow any graphics card, or a specific string value representing one of the types in graphics_card_types(). Default is True.
            memory_per_card (int): Memory allocated per graphics card. Default is 0.

        Raises:
            OptumiException: Raised if an unsupported GPU card is specified.
        """
        if type(gpu) is str and not gpu.lower() in [x.lower() for x in graphics_card_types()]:
            raise OptumiException("Unexpected GPU type '" + gpu + "', expected one of " + str(graphics_card_types()))
        self._gpu = gpu
        self._memory_per_card = memory_per_card

    @property
    def gpu(self):
        """Obtain the type of graphics card to be used, either True for any, or a specific string value representing one of the types in graphics_card_types()

        Returns:
            bool or str: The type of graphics card to be used, either True for any graphics card, or a specific string value representing one of the types in graphics_card_types()
        """
        return self._gpu

    @property
    def memory_per_card(self):
        """Obtain the memory required per graphics card.

        Returns:
            int: the memory required per graphics card, specified in GB.
        """
        return self._memory_per_card

    def __str__(self):
        return "gpu=" + str(self.gpu)
