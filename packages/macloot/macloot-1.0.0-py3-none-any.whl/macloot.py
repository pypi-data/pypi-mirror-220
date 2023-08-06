#!/usr/bin/env python
"""
macloot.py

Unleash the power of MAC addresses! Lookup OUIs, transform formats, and conquer the world of 
    networking with ease.

This module provides a command-line tool for MAC address manipulation. Look up the 
    Organization (OUI) of MAC addresses, transform between different MAC address formats, and more.

Usage:
- Lookup OUI: `macloot mac_addresses.txt`
- Transform formats: `macloot -O . mac_addresses.txt`
- Update OUI database: `macloot --update-db`

For detailed instructions and additional options, refer to the README.md file or 
    run `macloot --help`.

Note: The OUI database will be downloaded upon first use (with your approval) to ensure 
    up-to-date information for accurate lookups.

- Also: Why did the MAC address go on a diet? It wanted to shed a few colons!

Let the MAC address mastery begin!
"""
import argparse
import os
import sys

from dataclasses import dataclass
from site import USER_BASE
from oui import OuiDatabase
from mac import MacAddress, MacAddressGenerator

import app_info


@dataclass
class FormatArguments:
    """ Dataclass representing CLI arguments passed by the user. """
    delimiter: str
    upper: bool
    lower:bool
    verbose: bool

def create_argument_parser() -> argparse.ArgumentParser:
    """ Create an argument parser for the CLI arguments. """
    app_epilog  = f"examples:\n" \
                  f"  {app_info.NAME} macdump.txt\n" \
                  f"  {app_info.NAME} 0019.5600.beef\n" \
                  f"  {app_info.NAME} 80-C5-E6-00-B0-0B\n" \
                  f"  {app_info.NAME} \"Cisco: 0019.5600.beef, Windows: 80-C5-E6-00-B0-0B, " \
                  f"*nix: b8:27:eb:00:de:ad\" -O : -l\n" \
                  f"  ifconfig | {app_info.NAME} -O .\n" \
                  f"  {app_info.NAME} macdump.txt -d \";\" -o output.csv -q\n" \
                  f"  {app_info.NAME} -s Cisco\n" \

    # Create argument parser
    parser = argparse.ArgumentParser(
        description=app_info.DESCRIPTION,
        prog=app_info.NAME,
        epilog=app_epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Transformation arguments
    transform_group = parser.add_argument_group('transformational arguments')
    transform_group.add_argument("-O", "--octet-separator", default=None, metavar='CHAR',
                        help="character to use between octets in output (default: keep original)")
    transform_group.add_argument("-l", "--lower-case", action="store_true",
                        help="output MAC addresses in lower case")
    transform_group.add_argument("-u", "--upper-case", action="store_true",
                        help="output MAC addresses in upper case")

    # Output arguments
    output_group = parser.add_argument_group('output arguments')
    output_group.add_argument("-d", "--delimiter", default=None, metavar='CHAR',
                        help="delimiting character to use between fields in output (default: TAB)")
    output_group.add_argument("-o", "--output-file", metavar='FILE', help="write output to file")
    output_group.add_argument("-q", "--quiet", action="store_true",
                        help="suppress output to stdout")
    output_group.add_argument("-v", "--verbose", action="store_true",
                        help="include OUI information in output")

    # Generator arguments
    generator_group = parser.add_argument_group('generator arguments')
    generator_group.add_argument('-a', '--address-list', action="store_true",
                        help='generate a list of MAC addresses, default: 10; use -c to override')
    generator_group.add_argument('-c', '--count', default=10, type=int, metavar='INT',
                                 help='specify the count as an integer')
    generator_group.add_argument('-e', '--example-tables',
                        choices=['ios', 'arubaos', 'routeros'],
                        help='generate example MAC address tables for specific vendors,\n' \
                             'default: 10; use -c to override')

    # Define input parameters
    parser.add_argument("INPUT", nargs="?", default="-",
                        help="A filename or text input from stdin (see examples section).")
    parser.add_argument("-s", "--search", action="store_true",
                        help="search for OUI or organization in database")
    parser.add_argument("-V", "--version", action="store_true",
                        help="print version information and exit")
    parser.add_argument("-U", "--update-db", action="store_true",
                        help="force an update of the OUI database and exit")

    return parser

def print_version():
    """ Print version information and exit. """
    print(f"{app_info.NAME} {app_info.VERSION}")
    sys.exit(0)

def parse_input(input_string: str):
    """ Parse the input coming into the application via file or stdin. """

    # Check if input should come from a file or stdin
    if input_string == "-":
        # Read from stdin (pipe)
        try:
            input_lines = sys.stdin.readlines()
        except KeyboardInterrupt:
            print('\nExecution aborted by user.')
            sys.exit(1)
    else:
        # Read from file
        try:
            with open(input_string, 'r', encoding='utf-8') as file:
                input_lines = file.readlines()
        except FileNotFoundError:
            input_lines = input_string
    return input_lines

def create_mac_addresses(mac_addresses_input: str, database: OuiDatabase,
                         octet_separator: str = None) -> list:
    """ Create a list of MacAddress objects for every MAC address found in user input. """

    # Create one MacAddress instance for every MAC address in input
    mac_addresses = []
    for mac_address in mac_addresses_input:
        mac = MacAddress(mac_address)
        oui_entry = database.lookup(mac.address)
        if oui_entry:
            mac.organization_name = oui_entry.organization_name
            mac.organization_address = oui_entry.organization_address

        if octet_separator:
            mac.octet_separator = octet_separator
        mac_addresses.append(mac)
    return mac_addresses

def print_mac_addresses(mac_addresses: list, delimiter: str = None, upper_case: bool = False,
                        lower_case:bool = False, verbose: bool = False) -> None:
    """ Print a list of MacAddress objects. """
    for mac in mac_addresses:
        delim = '\t' if delimiter is None else delimiter
        if upper_case:
            mac_address = mac.uppercase
        elif lower_case:
            mac_address = mac.lowercase
        else:
            mac_address = mac.address

        if verbose:
            print(f"{mac_address}{delim}{mac.organization_name}{delim}{mac.organization_address}")
        else:
            print(f"{mac_address}{delim}{mac.organization_name}")

def write_mac_addresses_to_file(mac_addresses: list, outfile: str, args: FormatArguments) -> None:
    """ Write a list of MacAddress objects to file. """
    with open(outfile, 'w', encoding='utf8') as file:
        for mac in mac_addresses:
            delim = '\t' if args.delimiter is None else args.delimiter
            if args.upper:
                mac_address = mac.uppercase
            elif args.lower:
                mac_address = mac.lowercase
            else:
                mac_address = mac.address

            if args.verbose:
                file.write(f"{mac_address}{delim}{mac.organization_name}" \
                           f"{delim}{mac.organization_address}\n")
            else:
                file.write(f"{mac_address}{delim}{mac.organization_name}\n")

def generate_addresses(args: list, database: str) -> None:
    """ Generate MAC addresses in various formats. """

    count = args.count
    count_max = 1024
    address_list = args.address_list
    example_tables = args.example_tables

    if not 1 <= count <= count_max:
        print(f"{app_info.NAME}: error: argument -c/--count: expected " \
              f"integer between 1 and {count_max}")
        sys.exit(1)

    macgen = MacAddressGenerator(database)
    output = None

    if address_list:
        output = macgen.generate_mac_address_list(num=count, octet_separator=args.octet_separator,
                                                  upper=args.upper_case)
        print(output)
    elif example_tables:
        if example_tables == 'ios':
            output = macgen.generate_ios_output(count)
            print(output)
        elif example_tables == 'arubaos':
            output = macgen.generate_arubaos_output(count)
            print(output)
        else:
            output = macgen.generate_routeros_output(count)
            print(output)

def main():
    """ Entry point of the application. """

    # Initiate the OUI database
    csv_file = os.path.join(USER_BASE, f"share/{app_info.NAME}/oui.csv")
    oui_db = OuiDatabase(csv_file)

    # Create an argument parser instance
    parser = create_argument_parser()

    # Check for help argument
    if "-h" in sys.argv or "--help" in sys.argv:
        parser.print_help()
        sys.exit(0)

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Print version information and exit
    if args.version:
        print_version()

    # Update the OUI database if nessecary
    if args.update_db:
        # User requested a forced update via the -U argument
        oui_db.update_database(force_update=True)
        sys.exit(0)
    else:
        # Make sure that the OUI database is present
        oui_db.update_database()

    # Read the CSV file into memory
    oui_db.load_database()

    # Generating example MAC addresses
    if args.address_list or args.example_tables:
        generate_addresses(args=args, database=oui_db)
        sys.exit(0)

    # Check if the user is requesting a search
    if args.search:
        # Parse search input from stdin
        input_lines = args.INPUT

        delim = '\t' if args.delimiter is None else args.delimiter
        if len(input_lines) < 3:
            print(f"{app_info.NAME}: error: argument -s/--search: search term " \
                  "must be 3 or more characters long.")
            sys.exit(1)

        oui_entries = oui_db.search(input_lines)
        for entry in oui_entries:
            try:
                print(f"{entry.assignment}{delim}{entry.organization_name}")
            except BrokenPipeError:
                pass
    else:
        # Parse input from a file or stdin
        input_lines = parse_input(args.INPUT)

        # Process input lines
        data_input = "".join(input_lines).strip()

        # Find all MAC addresses in the user input
        mac_list = MacAddress.extract_addresses(data_input)

        # Create a list of MacAddress instance objects
        mac_addresses = create_mac_addresses(mac_addresses_input=mac_list, database=oui_db,
                                             octet_separator=args.octet_separator)

        # Print the list of MacAddress objects
        if not args.quiet:
            print_mac_addresses(mac_addresses=mac_addresses, delimiter=args.delimiter,
                                upper_case=args.upper_case, lower_case=args.lower_case,
                                verbose=args.verbose)
        if args.output_file:
            arg_list = FormatArguments(delimiter=args.delimiter, upper=args.upper_case,
                                       lower=args.lower_case, verbose=args.verbose)
            write_mac_addresses_to_file(mac_addresses=mac_addresses, outfile=args.output_file,
                                        args=arg_list)

    sys.exit(0)

if __name__ == "__main__":
    main()
