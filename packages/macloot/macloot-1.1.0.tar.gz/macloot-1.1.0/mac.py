"""
mac.py

This module provides the `MacAddress` classes and functionality for handling MAC addresses. 
The main `MacAddress` class represents a MAC address and includes methods for manipulation,
    formatting and analysis.

Classes:
- MacAddress: Represents a MAC address and provides various methods for MAC address handling.
- MacCase: Enumeration class representing the character casing used by the MacAddress class.
- MacAddressGenerator: Generates testing addresses and output in various formats.

Note: The methods in the `MacAddress` class operate on well-formed MAC addresses. Ensure that the 
    MAC address string provided adheres to the standard format.

For more information, refer to the documentation or relevant code comments.
"""
import random
import re

from enum import Enum
from oui import OuiDatabase, OuiOrganization

class MacCase(Enum):
    """ Defines three possible character case values. """
    ORIGINAL  = 0   # Leave as provided by input
    UPPERCASE = 1   # Uppercase
    LOWERCASE = 2   # Lowercase

class MacAddress:
    """ Class definition of a MAC address. """

    def __init__(self, mac_address: str, case: MacCase = MacCase.ORIGINAL) -> None:
        """ Initialize a MacAddress object with the provided MAC address. """
        self.__address = MacAddress.remove_separators(mac_address)
        self.__organization = OuiOrganization(name=None, address=None)
        self.__octet_separator = MacAddress.get_octet_separator(mac_address)
        self.__case = case

    def __str__(self):
        """ Get the string representation of the MacAddress object. """
        return self.address

    def __eq__(self, other):
        """ Compare this MacAddress with another MacAddress object. """
        if isinstance(other, MacAddress):
            return  self.__address == other.address and \
                    self.__organization.name == other.organization.name
        return False

    def __lt__(self, other):
        """ Check if this MacAddress is 'less than' another MacAddress object. """
        if isinstance(other, MacAddress):
            return self.to_int() < other.to_int()
        return False

    def to_bytes(self):
        """ Convert the MAC address into a bytes representation. """
        # Implement logic to convert the MAC address into a bytes representation
        raise NotImplementedError

    def to_int(self):
        """ Convert the MAC address into an integer representation. """
        return int(self.__address, 16)

    def to_list(self, verbose: bool = False) -> list:
        """ Return a subset or all printable properties of the MacAddress class as a list. """
        if verbose:
            return [str(self.address), str(self.__organization.name),
                    str(self.__organization.address)]
        return [str(self.address), str(self.__organization.name)]

    @classmethod
    def check_case(cls, mac_address: str) -> str:
        """ Check if the MAC address is in upper or lower case. """

        # Check if the MAC address contains only digits
        if mac_address.isdigit():
            return None

        # Find the first character that is a letter
        for char in mac_address:
            if char.isalpha():
                return "lower" if char.islower() else "upper"

        return None

    @classmethod
    def from_bytes(cls, mac_bytes):
        """ Create a MacAddress instance from a bytes representation. """
        # Implement logic to create a MacAddress instance from a bytes representation
        raise NotImplementedError

    @classmethod
    def get_octet_separator(cls, mac_address: str) -> str:
        """ Find the octet separator character used in the MAC address provided. """
        for separator in [":", "-", "."]:
            if separator in mac_address:
                return separator
        return ""

    @classmethod
    def remove_separators(cls, mac_address: str) -> str:
        """ Convert the given MAC address into a string containing only hexadecimal characters. """
        return re.sub(r'[^\da-fA-F]', '', mac_address)

    @classmethod
    def extract_addresses(cls, input_string) -> list:
        """ Find and return a list of MAC addresses using the most common formats. """

        # Regex pattern to find 1a2b3c4D5E6F, b0:0b:fa:ce:13:37 or B0-0B-FA-CE-13-37
        common_pattern = re.findall(r'((?:[\da-fA-F]{2}[:\-]){5}[\da-fA-F]{2})', input_string)

        # Regex pattern to find b00b.face.1337 or B00B.face.1234
        cisco_pattern  = re.findall(r'((?:[\da-fA-F]{4}[\.]){2}[\da-fA-F]{4})', input_string)

        # Regex pattern to find b00bface1337 or B00Bface1234
        hex_pattern  = re.findall(r'(?:[\da-fA-F]{12})', input_string)

        return common_pattern + cisco_pattern + hex_pattern

    @classmethod
    def format(cls, mac: str, separator: str = ":", section_size: int = 2,
               case: MacCase = MacCase.ORIGINAL) -> str:
        """ Insert separator between octets in the MAC address string. """
        mac_octets = [mac[i:i+section_size] for i in range(0, len(mac), section_size)]
        mac_address = separator.join(mac_octets)
        if case == MacCase.UPPERCASE:
            mac_address = mac_address.upper()
        elif case == MacCase.LOWERCASE:
            mac_address = mac_address.lower()
        return mac_address

    @property
    def address(self):
        """
        Return the MAC address using the delimiter from the self.__delimiter variable.
        
        If the delimiter is a . (dot) we return the address Cisco style:
         - xxxx.xxxx.xxxx
        Else we return the address "everyone else" style:
         - xx-xx-xx-xx-xx-xx
         - xx:xx:xx:xx:xx:xx
        """
        if self.octet_separator == ".":
            mac_address = MacAddress.format(self.__address, separator=self.octet_separator,
                                            section_size=4, case=self.__case)
        else:
            mac_address = MacAddress.format(self.__address, separator=self.octet_separator,
                                            case=self.__case)
        return mac_address

    @property
    def oui(self):
        """ Get the OUI part of the MAC address (the first 6 characters). """
        return self.__address[:6].upper()

    @property
    def organization(self):
        """ Get the Organization data object. """
        return self.__organization

    @property
    def octet_separator(self):
        """ Get the octet separator to be used between octets in the MAC address. """
        return self.__octet_separator

    @octet_separator.setter
    def octet_separator(self, value):
        """ Set the octet separator to be used between octets in the MAC address. """
        self.__octet_separator = value

class MacAddressGenerator:
    """ A MAC address generator class which outputs addresses in various formats. """

    def __init__(self, database: OuiDatabase):
        """ Initialize the MacAddressGenerator with the given OUI database. """
        database.load_database()
        self.__oui_list = database.get_entries()

    def generate_mac_address(self, case: MacCase = MacCase.LOWERCASE):
        """ Generate a random and valid MAC address and return MacAddress object. """

        # Randomly pick a valid OUI from the OUI database (first 6 digits of MAC)
        first_three_octets = random.choice(self.__oui_list).assignment.lower()

        # Randomly generate the last 3 octets (last 6 digits of MAC)
        last_three_octets = random.getrandbits(24)

        # Combine the two and return as a MacAddress object
        return MacAddress(f"{first_three_octets}{last_three_octets:06x}", case=case)

    def generate_mac_address_list(self, num: int, octet_separator: str,
                                  case: MacCase = MacCase.LOWERCASE):
        """ Generate a list MAC addresses. """
        output = []

        for _ in range(num):
            # Get a random MAC address with a valid OUI
            mac = self.generate_mac_address(case=case)

            # Use default octet separator ':' if none is provided
            mac.octet_separator = ':' if octet_separator is None else octet_separator

            # Print MAC addresses in users preferred case
            output.append(f"{mac.address}")
        return "\n".join(output)

    def generate_ios_output(self, count):
        """ Generate a number of rows of Cisco IOS MAC Address Table. """
        output = []
        output.append('Mac Address Table')
        output.append('-------------------------------------------')
        output.append('Vlan    Mac Address       Type        Ports')
        output.append('----    -----------       --------    -----')
        vlan = 0
        for i in range(count):
            vlan += 1 if i % random.choice([2,4,8]) == 0 else 0
            mac = self.generate_mac_address()
            mac_addr = MacAddress.format(mac.address, '.', 4, case=MacCase.UPPERCASE)
            output.append(f" {vlan:2}     {mac_addr}    DYNAMIC     Gi0/1")
        return "\n".join(output)

    def generate_routeros_output(self, count):
        """ Generate a number of rows of RouterOS MAC Address Table. """
        output = []
        output.append("Flags: D - DYNAMIC; E - EXTERNAL")
        output.append("Columns: MAC-ADDRESS, VID, ON-INTERFACE, BRIDGE")
        output.append(" #    MAC-ADDRESS        VID  ON-INTERFACE  BRIDGE")
        for i in range(count):
            mac = self.generate_mac_address()
            mac_addr = MacAddress.format(mac.address)
            vlan = random.choice([1, 5, 10, 20, 30, 40])
            output.append(f"{i:2} DE {mac_addr}  {vlan:3}  ether1        bridge")
        return "\n".join(output)

    def generate_arubaos_output(self, count):
        """ Generate a number of rows of ArubaOS-CX MAC Address Table. """
        output = []
        output.append("MAC age-time            : 300 seconds")
        output.append(f"Number of MAC addresses : {count}")
        output.append("")
        output.append("MAC Address          VLAN     Type       Port")
        output.append("--------------------------------------------------")
        vlan = 0
        for i in range(count):
            vlan += 1 if i % random.choice([4,8,16]) == 0 else 0
            mac = self.generate_mac_address()
            mac_addr = MacAddress.format(mac.address, case=MacCase.LOWERCASE)
            output.append(f"{mac_addr}    {vlan:3}      dynamic    1/1/1")
        return "\n".join(output)
