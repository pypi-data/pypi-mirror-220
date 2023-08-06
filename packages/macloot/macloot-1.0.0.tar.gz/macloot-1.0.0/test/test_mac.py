""" Unit Testing Script for mac.py module. """
import os
import unittest

from test_oui import OuiDatabaseTestCase
from mac import MacAddress, MacAddressGenerator
from oui import OuiDatabase


class MacAddressTestCase(unittest.TestCase):
    """ Test cases testing the parsing capabilities of MAC addresses. """
    def test_format_mac_address(self):
        """ Test the formatting capabilitites of the format_mac_address() method. """
        mac1 = "001122334455"
        mac2 = "AABBCCDDEEFF"
        mac3 = "112233445566"
        mac4 = "112233445566"

        expected1 = "00:11:22:33:44:55"
        expected2 = "AA-BB-CC-DD-EE-FF"
        expected3 = "1122.3344.5566"
        expected4 = "112233445566"

        self.assertEqual(MacAddress.format(mac1), expected1)
        self.assertEqual(MacAddress.format(mac2, '-'), expected2)
        self.assertEqual(MacAddress.format(mac3, '.', section_size=4), expected3)
        self.assertEqual(MacAddress.format(mac4, ''), expected4)

    def test_get_octet_separator(self):
        """ Get the octet separator character from a MAC address string. """
        mac_address_dot     = "0011.22AA.BBCC"
        mac_address_colon   = "00:11:22:AA:BB:CC"
        mac_address_hyphen  = "00-11-22-AA-BB-CC"
        mac_address_empty   = "001122AABBCC"

        expected_separator_dot      = "."
        expected_separator_colon    = ":"
        expected_separator_hyphen   = "-"
        expected_separator_empty    = ""

        result_dot      = MacAddress.get_octet_separator(mac_address_dot)
        result_colon    = MacAddress.get_octet_separator(mac_address_colon)
        result_hyphen   = MacAddress.get_octet_separator(mac_address_hyphen)
        result_empty    = MacAddress.get_octet_separator(mac_address_empty)

        self.assertEqual(result_dot, expected_separator_dot)
        self.assertEqual(result_colon, expected_separator_colon)
        self.assertEqual(result_hyphen, expected_separator_hyphen)
        self.assertEqual(result_empty, expected_separator_empty)

    def test_remove_separators(self):
        """ Return a string with separator characters removed from the MAC address. """
        mac_address_dot     = "00.11.22.33.44.55"
        mac_address_colon   = "00:11:22:33:44:55"
        mac_address_hyphen  = "00-11-22-33-44-55"
        mac_address_empty   = "001122334455"

        expected_result = "001122334455"

        result_dot      = MacAddress.remove_separators(mac_address_dot)
        result_colon    = MacAddress.remove_separators(mac_address_colon)
        result_hyphen   = MacAddress.remove_separators(mac_address_hyphen)
        result_empty    = MacAddress.remove_separators(mac_address_empty)

        self.assertEqual(result_dot, expected_result)
        self.assertEqual(result_colon, expected_result)
        self.assertEqual(result_hyphen, expected_result)
        self.assertEqual(result_empty, expected_result)

    def test_extract_addresses(self):
        """ Test MAC address extraction from different types of strings. """
        input_string_1 = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, " \
                         "sed do eiusmod tempor incididunt ut labore et dolore 00:11:22:33:44:55 " \
                         "magna aliqua."
        input_string_2 = "Multiple MAC addresses: 00:11:22:33:44:55, 66:77:88:99:AA:BB, " \
                         "A1:B2:C3:D4:E5:F6, AABBCCDDEEFF found in this string."
        input_string_3 = """
                         Log file entry 1: 00:11:22:33:44:55, 00-11-22-33-44-55, 0011.2233.4455
                         Log file entry 2: 0011:2233:4455, AABB.CCDD.EEFF, AABBCCDDEEFF
                         Log file entry 3: Aa:Bb:Cc:Dd:Ee:Ff, AaBbCcDdEeFf and 0123-abcd-1337, 
                         """
        input_string_4 = "No MAC addresses here!"

        expected_addresses_1 = ["00:11:22:33:44:55"]
        expected_addresses_2 = ["00:11:22:33:44:55", "66:77:88:99:AA:BB",
                                "A1:B2:C3:D4:E5:F6", "AABBCCDDEEFF"]
        expected_addresses_3 = ["00:11:22:33:44:55", "00-11-22-33-44-55", "Aa:Bb:Cc:Dd:Ee:Ff",
                                "0011.2233.4455", "AABB.CCDD.EEFF", "AABBCCDDEEFF", "AaBbCcDdEeFf"]
        expected_addresses_4 = []

        result_1 = MacAddress.extract_addresses(input_string_1)
        result_2 = MacAddress.extract_addresses(input_string_2)
        result_3 = MacAddress.extract_addresses(input_string_3)
        result_4 = MacAddress.extract_addresses(input_string_4)

        self.assertEqual(result_1, expected_addresses_1)
        self.assertEqual(result_2, expected_addresses_2)
        self.assertEqual(result_3, expected_addresses_3)
        self.assertEqual(result_4, expected_addresses_4)

    def test_format(self):
        """ Test MAC address formatting with octet separators. """
        mac1 = "001122334455"
        mac2 = "ABCD1234a1b2"
        mac3 = "a1b2c3d4e5f6"

        expected_result1 = "00:11:22:33:44:55"
        expected_result2 = "AB-CD-12-34-a1-b2"
        expected_result3 = "a1b2.c3d4.e5f6"

        result1 = MacAddress.format(mac1)
        result2 = MacAddress.format(mac2, separator="-")
        result3 = MacAddress.format(mac3, separator=".", section_size=4)

        self.assertEqual(result1, expected_result1)
        self.assertEqual(result2, expected_result2)
        self.assertEqual(result3, expected_result3)

    def test_oui_property(self):
        """ Test the MacAddress OUI property. """
        mac_address1 = MacAddress('00:11:22:33:44:55')
        mac_address2 = MacAddress('AA-BB-CC-DD-EE-FF')
        mac_address3 = MacAddress('AaBbCcDdEeFf')
        mac_address4 = MacAddress('a1b2.c3d4.e5f6')

        expected_oui1 = '001122'
        expected_oui2 = 'AABBCC'
        expected_oui3 = 'AABBCC'
        expected_oui4 = 'A1B2C3'

        result1 = mac_address1.oui
        result2 = mac_address2.oui
        result3 = mac_address3.oui
        result4 = mac_address4.oui

        self.assertEqual(result1, expected_oui1)
        self.assertEqual(result2, expected_oui2)
        self.assertEqual(result3, expected_oui3)
        self.assertEqual(result4, expected_oui4)

    def test_lowercase_property(self):
        """ Test the MacAddress lowercase property. """
        mac_address1 = MacAddress('00:11:22:33:44:55')
        mac_address2 = MacAddress('AA-BB-CC-DD-EE-FF')
        mac_address3 = MacAddress('AaBbCcDdEeFf')
        mac_address4 = MacAddress('a1b2.c3d4.e5f6')

        expected_lower1 = '00:11:22:33:44:55'
        expected_lower2 = 'aa-bb-cc-dd-ee-ff'
        expected_lower3 = 'aabbccddeeff'
        expected_lower4 = 'a1b2.c3d4.e5f6'

        result1 = mac_address1.lowercase
        result2 = mac_address2.lowercase
        result3 = mac_address3.lowercase
        result4 = mac_address4.lowercase

        self.assertEqual(result1, expected_lower1)
        self.assertEqual(result2, expected_lower2)
        self.assertEqual(result3, expected_lower3)
        self.assertEqual(result4, expected_lower4)

    def test_uppercase_property(self):
        """ Test the MacAddress uppercase property. """
        mac_address1 = MacAddress('00:11:22:33:44:55')
        mac_address2 = MacAddress('AA-BB-CC-DD-EE-FF')
        mac_address3 = MacAddress('AaBbCcDdEeFf')
        mac_address4 = MacAddress('a1b2.c3d4.e5f6')

        expected_upper1 = '00:11:22:33:44:55'
        expected_upper2 = 'AA-BB-CC-DD-EE-FF'
        expected_upper3 = 'AABBCCDDEEFF'
        expected_upper4 = 'A1B2.C3D4.E5F6'

        result1 = mac_address1.uppercase
        result2 = mac_address2.uppercase
        result3 = mac_address3.uppercase
        result4 = mac_address4.uppercase

        self.assertEqual(result1, expected_upper1)
        self.assertEqual(result2, expected_upper2)
        self.assertEqual(result3, expected_upper3)
        self.assertEqual(result4, expected_upper4)

    def test_octet_separator_property(self):
        """ Test the MacAddress octet separator property. """
        mac_address1 = MacAddress('00:11:22:33:44:55')
        mac_address2 = MacAddress('AA-BB-CC-DD-EE-FF')
        mac_address3 = MacAddress('AaBbCcDdEeFf')
        mac_address4 = MacAddress('a1b2.c3d4.e5f6')
        expected_separator1 = ':'
        expected_separator2 = '-'
        expected_separator3 = ''
        expected_separator4 = '.'

        result1 = mac_address1.octet_separator
        result2 = mac_address2.octet_separator
        result3 = mac_address3.octet_separator
        result4 = mac_address4.octet_separator

        self.assertEqual(result1, expected_separator1)
        self.assertEqual(result2, expected_separator2)
        self.assertEqual(result3, expected_separator3)
        self.assertEqual(result4, expected_separator4)

    def test_organization_name_property(self):
        """ Test the MacAddress organization name property. """
        mac_address = MacAddress('00:11:22:33:44:55')
        expected_name = 'Organization Name'

        result = mac_address.organization_name

        self.assertIsNone(result)

        mac_address.organization_name = expected_name

        result = mac_address.organization_name

        self.assertEqual(result, expected_name)

    def test_organization_address_property(self):
        """ Test the MacAddress organization address property. """
        mac_address = MacAddress('00:11:22:33:44:55')
        expected_address = 'Organization Address'

        result = mac_address.organization_address

        self.assertIsNone(result)

        mac_address.organization_address = expected_address

        result = mac_address.organization_address

        self.assertEqual(result, expected_address)


class TestMacAddressGenerator(unittest.TestCase):
    """ Test cases testing the generating capabilities of the MacAddressGenerator class. """
    def setUp(self):
        # Create a temporary file in the CSV format
        self.temp_file_path = OuiDatabaseTestCase.get_sample_database_csv_file()

        database = OuiDatabase(self.temp_file_path)

        # Create a MacAddressGenerator instance for testing
        self.generator = MacAddressGenerator(database)

    def tearDown(self):
        # Remove the temporary file
        os.remove(self.temp_file_path)

    def test_generate_mac_address(self):
        """ Test the MAC address generator method. """
        mac_address = self.generator.generate_mac_address()
        self.assertIsInstance(mac_address, MacAddress)

    def test_generate_mac_address_list(self):
        """ Test the MAC address list generator method. """
        num = 5
        octet_separator = '-'
        upper = True
        mac_list = self.generator.generate_mac_address_list(num, octet_separator, upper)
        mac_addresses = mac_list.split('\n')
        self.assertEqual(len(mac_addresses), num)
        for mac_address in mac_addresses:
            self.assertEqual(mac_address, mac_address.upper())
