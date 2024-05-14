#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#TODO: Add description
"""

# Standard libraries
import logging
from sys import exit
from dataclasses import dataclass

# Third-party libraries
from rich.logging import RichHandler
from netmiko import BaseConnection

# Local libraries


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
log: logging.Logger = logging.getLogger("rich")


class WriteStatusError(Exception):
    pass


class WriteVlanIDError(Exception):
    pass


class WriteInterfacesError(Exception):
    pass


class Vlan:
    def __init__(self, connection: BaseConnection, vlan_id: int, name: str, status: str, interfaces: list[str]):
        self.connection = connection
        self._vlan_id = vlan_id
        self._name = name
        self._status = status
        self._interfaces = interfaces

    @property
    def vlan_id(self) -> int:
        """
        Get the VLAN ID.

        :return: The VLAN ID.
        :rtype: int
        """
        return self._vlan_id

    @property
    def name(self) -> str:
        """
        Get the name of the VLAN.

        :return: The name of the VLAN.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Set the name of the VLAN.

        :param name: The name of the VLAN.
        :type name: str
        :raises ValueError: If the name is not a string or if the VLAN is reserved.
        """
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")

        if self.vlan_id in [1, 1002, 1003, 1004, 1005]:
            raise ValueError(
                "VLANs 1, 1002, 1003, 1004, and 1005 are reserved and cannot be modified."
            )

        commands = [f"vlan {self.vlan_id}", f"name {name}"]
        self._connection.send_config_set(commands)
        self._connection.save_config()
        self._name = name
        log.info(f"VLAN {self.vlan_id} name set to {name}")

    @property
    def status(self) -> str:
        """
        Get the status of the VLAN.

        :return: The status of the VLAN.
        :rtype: str
        """
        return self._status

    @property
    def interfaces(self) -> list[str]:
        """
        Get the interfaces assigned to the VLAN.

        :return: The interfaces assigned to the VLAN.
        :rtype: list[str]
        """
        return self._interfaces
