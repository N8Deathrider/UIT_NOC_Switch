#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#TODO: Add description
"""

# Standard libraries
import logging
from sys import exit

# Third-party libraries
from rich.logging import RichHandler
from netmiko import ConnectHandler
from netmiko import SSHDetect
from netmiko import BaseConnection

# Local libraries
from vlan import Vlan

# Standard exit codes
EXIT_SUCCESS = 0  # No errors
EXIT_GENERAL_ERROR = 1  # General error
EXIT_INVALID_ARGUMENT = 120  # Invalid argument to exit
EXIT_KEYBOARD_INTERRUPT = 130  # Keyboard interrupt (Ctrl+C)


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
log: logging.Logger = logging.getLogger("rich")
logging.getLogger("paramiko").setLevel(logging.WARNING)


class Switch:

    def __init__(self, address: str, username: str, password: str):
        self._connection_settings = {
            "device_type": "autodetect",
            "host": address,
            "username": username,
            "password": password,
        }
        try:
            guesser = SSHDetect(**self._connection_settings)
            best_match = guesser.autodetect()
            log.debug(f"Best match: {best_match}")
            self._connection_settings["device_type"] = best_match
            self._connection = ConnectHandler(**self._connection_settings)
        except Exception as e:
            log.exception(f"Failed to connect to {address}: {e}")
        else:
            log.debug(f"Connected to {address} using {best_match}")

        self._get_facts()

    def __del__(self):
        try:
            self._connection.disconnect()
        except Exception as e:
            log.exception(f"Failed to disconnect: {e}")
        else:
            log.debug("Disconnected")

    def _get_facts(self) -> None:
        show_version = self._connection.send_command("show version", use_textfsm=True)
        vlans = self._connection.send_command("show vlan", use_textfsm=True)
        self.vlans = {vlan["vlan_id"]: Vlan(_connection=self._connection, **vlan) for vlan in vlans}

        self.uptime = show_version[0]["uptime"]
        self.hostname = show_version[0]["hostname"]
        self.model = show_version[0]["hardware"]
        self.uptime_years = show_version[0]["uptime_years"]
        self.uptime_weeks = show_version[0]["uptime_weeks"]
        self.uptime_days = show_version[0]["uptime_days"]
        self.uptime_hours = show_version[0]["uptime_hours"]
        self.uptime_minutes = show_version[0]["uptime_minutes"]
        self.reload_reason = show_version[0]["reload_reason"]
        self.version = show_version[0]["version"]
        self.reload_reason = show_version[0]["reload_reason"]
        self.image = show_version[0]["running_image"]
        self.config_register = show_version[0]["config_register"]
        self.mac_address = show_version[0]["mac"]
        self.restarted = show_version[0]["restarted"]



if __name__ == "__main__":  #DEBUG
    from auth import SSH
    from rich import print as rprint
    s = Switch("172.31.16.52", **SSH.full)

