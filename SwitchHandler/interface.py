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


@dataclass
class Interface:  # TODO: get the netmiko output for `sh run int {id}` and figure out what options are needed to init
    _connection: BaseConnection
    interface_id: str
    _description: str | None
    _access_vlan: int | str | None
    voice_vlan: int | str | None
    last_input: str
    last_output: str
    input_errors: str | int
    crc: str | int
    output_errors: str | int
    link_status: str
    hardware_type: str
    protocol_status: str


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    

    @property
    def description(self) -> str | None:
        """
        Returns the description of the interface.

        :returns: The description of the interface.
        :rtype: str or None
        """
        return self._description

    @description.setter
    def description(self, description: str | None):
        """
        Sets or removes the description of the interface.

        :param description: The description to set for the interface. Pass an empty string to remove the description.
        :type description: str or None

        :returns: None

        :raises: ValueError if the description is not a string or None.

        :example:
            # To set a description
            interface = switch.interface["Gi1/0/4"]
            interface.description = "This is the interface description"

            # To remove the description
            interface.description = None

            # Or
            interface.description = ""
        """
        if not isinstance(description, (str, type(None))):
            raise ValueError("Description must be a string or None.")

        self._description = description

        if description:
            self._connection.send_config_set([
                f'interface {self.interface_id}',
                f'description {self.description}'
            ])
        else:
            self._connection.send_config_set([
                f'interface {self.interface_id}',
                'no description'
            ])

    @property
    def access_vlan(self) -> int | str | None:
        """
        Returns the access VLAN of the interface.

        :returns: The access VLAN of the interface.
        :rtype: int or str or None
        """
        return self._access_vlan

    @access_vlan.setter
    def access_vlan(self, vlan_id: int | str | None):
        """
        Sets or removes the access VLAN of the interface.

        :param vlan_id: The VLAN ID to set for the interface. Pass None to remove the VLAN.
        :type vlan_id: int or str or None

        :returns: None

        :raises: ValueError if the VLAN ID is not an integer, string, or None.

        :example:
            # To set the access VLAN
            interface = switch.interface["Gi1/0/4"]
            interface.access_vlan = 10

            # Or
            interface.access_vlan = "10"

            # To remove the access VLAN
            interface.access_vlan = None
        """
        if not isinstance(vlan_id, (int, str, type(None))):
            raise ValueError("VLAN ID must be an integer, string, or None.")

        self._access_vlan = vlan_id

        if vlan_id:
            self._connection.send_config_set([
                f'interface {self.interface_id}',
                f'switchport access vlan {vlan_id}'
            ])
        else:
            self._connection.send_config_set([
                f'interface {self.interface_id}',
                'no switchport access vlan'
            ])


