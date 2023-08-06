"""
oui.py

This module provides classes for working with the OUI (Organizationally Unique Identifier) database.
The OuiDatabase class represents the entire OUI database and provides methods for querying 
    and retrieving information.
The OuiEntry class represents a single entry in the OUI database and contains information
    about an organization's MAC address assignment.

Classes:
- OuiDatabase: Represents the OUI database and provides methods for data retrieval.
- OuiEntry: Represents a single entry in the OUI database with registry, assignment,
    organization name, and address fields.

Usage:
1. Import the module: `from oui import OuiDatabase, OuiEntry`
2. Create an OuiDatabase object: `database = OuiDatabase()`
3. Open the CSV file containing the database: `database.load_database('oui.csv')`
3. Retrieve OuiEntry objects from the database: `entries = database.get_entries()`
4. Access the fields of an OuiEntry: `entry.registry`, `entry.assignment`,
    `entry.organization_name`, `entry.organization_address`

Note: The OUI database is not included in this module and must be provided separately in 
    the `oui.csv` format.

For more information, refer to the documentation or visit the official IEEE OUI database website.
"""

import csv
import datetime
import os
import re
import requests

class OuiEntry:
    """ Class definition of an OUI entry in the CSV database file. """

    def __init__(self, registry: str, assignment: str, \
                 organization_name: str, organization_address: str):
        """ Initialize an OuiEntry object with the provided fields. """
        self.__registry = registry
        self.__assignment = assignment
        self.__organization_name = organization_name
        self.__organization_address = organization_address

    def __str__(self) -> str:
        """ Return a string representation of the OuiEntry. """
        return f"OuiEntry(registry='{self.registry}', assignment='{self.assignment}', " \
               f"organization_name='{self.organization_name}', "\
               f"organization_address='{self.organization_address}')"

    def __repr__(self) -> str:
        """ Return a string representation of the OuiEntry for object re-creation. """
        return f"OuiEntry(registry='{self.registry}', assignment='{self.assignment}', " \
               f"organization_name='{self.organization_name}', " \
               f"organization_address='{self.organization_address}')"

    def __eq__(self, other):
        """ Compare two OuiEntry objects for equality. """
        if isinstance(other, OuiEntry):
            return (
                self.__registry == other.registry and
                self.__assignment == other.assignment and
                self.__organization_name == other.organization_name and
                self.__organization_address == other.organization_address
            )
        return False

    @property
    def registry(self) -> str:
        """ Get the registry field of the OuiEntry. """
        return self.__registry

    @property
    def assignment(self) -> str:
        """ Get the assignment field of the OuiEntry. """
        return self.__assignment

    @property
    def organization_name(self) -> str:
        """ Get the organization name field of the OuiEntry. """
        return self.__organization_name

    @property
    def organization_address(self) -> str:
        """ Get the organization address field of the OuiEntry. """
        return self.__organization_address


class OuiDatabase:
    """ Class definition of the OUI database. """

    def __init__(self, database_file: str) -> None:
        """ Constructor method for the OuiDatabase class. """
        self.__oui_entries      = []
        self.__oui_csv_url      = 'https://standards-oui.ieee.org/oui/oui.csv'
        self.__database_file = database_file

    def load_database(self) -> None:
        """ Load the OUI database from the specified file. """

        # Clear the OUI data
        self.__oui_entries.clear()

        # Open and read the CSV file
        with open(self.__database_file, 'r', encoding='utf-8') as csv_file:

            # Create a CSV reader object
            csv_reader = csv.reader(csv_file)

            # Skip the first line (column names)
            next(csv_reader)

            # Read and process each row in the CSV file
            for row in csv_reader:
                oui_entry = OuiEntry(registry=row[0], assignment=row[1], \
                                     organization_name=row[2], organization_address=row[3].rstrip())
                self.__oui_entries.append(oui_entry)

    def lookup(self, mac_address: str) -> OuiEntry:
        """ Lookup the organization (OUI) of the given MAC address. """

        # Convert any MAC address into assignment format 'ABCDEF' (6 hex characters in upper case)
        assignment = re.sub(r'[^\da-fA-F]', '', mac_address)[:6].upper()

        # Look for an OUI entry matching the assignment ID (OUI)
        for entry in self.__oui_entries:
            if entry.assignment == assignment:
                return entry
        return None

    def search(self, organization_name: str) -> list:
        """ Search for OUIs belonging to an organization. """

        # List of resulting OuiEntry objects
        results = []

        # Look for an OUI entry matching the assignment ID (OUI)
        for entry in self.__oui_entries:
            if organization_name.lower() in entry.organization_name.lower():
                results.append(entry)
        return results

    def get_entries(self) -> list:
        """ Get the list of OuiEntry items read from the database file. """
        return self.__oui_entries

    def update_database(self, force_update = False) -> bool:
        """ Update the OUI database with the latest version. """

        # Check if the file exists in the current directory
        if not os.path.exists(self.__database_file) or force_update:
            update_action = 'has been requested' if force_update else 'is required'
            print(f"An update of the OUI database {update_action}...")

            db_age = self.database_age()
            if db_age == 0:
                updated_text = "today"
            elif db_age == 1:
                updated_text = "one day ago"
            else:
                updated_text = f"{db_age} days ago"

            # Only print age if 0 or more days (-1 == never)
            if db_age >= 0:
                print(f"The database was last updated {updated_text}.\n")

            # Get the size of the file to be downloaded
            response = requests.get(self.__oui_csv_url, stream=True, timeout=5)
            total_size = int(response.headers.get('Content-Length', 0))
            block_size = 1024  # Adjust the block size as desired
            mebibytes = total_size / (1024 * 1024)

            # File does not exist, ask for user confirmation
            try:
                user_choice = input(f"Proceed with the download of the following file? \n" \
                                f"- {self.__oui_csv_url} ({mebibytes:.2f} MiB)? (Y/n): ")
                if user_choice.lower() == "n":
                    return False
            except KeyboardInterrupt:
                print("\nThe user has terminated the operation.")
                return False

            # Create the directory if it doesn't exist
            directory = os.path.dirname(self.__database_file)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # User confirmed, download the file
            with open(self.__database_file, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded_size = file.tell()
                    percent = int(downloaded_size * 100 / total_size)
                    print(f"Downloaded {downloaded_size} bytes ({percent}%)\r", end="")

            print("\nFile downloaded successfully.")
            return True
        return False

    def database_age(self) -> int:
        """ Get the age of the OUI database (in days). """
        if os.path.exists(self.__database_file):
            # Get the modification time of the database file
            modification_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(self.__database_file)
            )

            # Calculate the age in days
            current_time = datetime.datetime.now()
            age = (current_time - modification_time).days
            return age

        return -1
