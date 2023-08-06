""" Unit Testing Script for oui.py module. """
import datetime
import os
import unittest
import tempfile

from oui import OuiDatabase, OuiEntry


class OuiEntryTestCase(unittest.TestCase):
    """ Test cases testing the capabilities of the OUI database entry class. """


class OuiDatabaseTestCase(unittest.TestCase):
    """ Test cases testing the capabilities of the OUI database class. """

    def setUp(self):
        # Remember the temporary file path for later use
        self.temp_file_path = OuiDatabaseTestCase.get_sample_database_csv_file()

    def tearDown(self):
        # Remove the temporary file
        os.remove(self.temp_file_path)

    @classmethod
    def get_sample_database_csv_file(cls):
        """ Create a temporary sample database file in the CSV format. """
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:

            # Write test data to the temporary file
            temp_file.write(b'Registry,Assignment,Organization Name,Organization Address\n')
            temp_file.write(b'MA-L,001122,PiPlus Microelectronics Limited,123 Building 1 ' \
                                 b'No.123 Shedang Xia Road Shanghai\n')
            temp_file.write(b'MA-L,AABBCC,Boomerang Corporation,"#100,00, Jongram, ' \
                                b'Songbook Seoul "\n')
            temp_file.write(b'MA-L,A1B2C3,Nevigon,Lysfjun Torg 1  Lysfjun  NO NO-1234\n')
            temp_file.write(b'MA-L,334455,"Panazonica Automotive Systems Co.,Ltd",1337 ' \
                                b'Matsumoto City Nagano JP 100-1234 \n')
            temp_file.write(b'MA-L,111333,Barista Networks,1234 Great America Parkway ' \
                                b'Santa Clara CA US 98765 \n')
            temp_file.write(b'MA-L,A1A1A1,"Semsung Electronics Co.,Ltd","#83-1, Imtoo-Long ' \
                                b'Gummi Gyeongbook "\n')
            temp_file.write(b'MA-L,123456,"Semsung Electronics Co.,Ltd","#83-1, Imtoo-Long ' \
                                b'Gummi Gyeongbook "\n')
            temp_file.flush()

        return temp_file.name

    def test_load_database_and_get_entries(self):
        """ Test if the loaded records from the temporary CSV file match the test records. """
        oui_db = OuiDatabase(self.temp_file_path)
        expected_entries = [
            OuiEntry(registry='MA-L', assignment='001122',
                     organization_name='PiPlus Microelectronics Limited',
                     organization_address='123 Building 1 No.123 Shedang Xia Road Shanghai'),
            OuiEntry(registry='MA-L', assignment='AABBCC',
                     organization_name='Boomerang Corporation',
                     organization_address='#100,00, Jongram, Songbook Seoul'),
            OuiEntry(registry='MA-L', assignment='A1B2C3',
                     organization_name='Nevigon',
                     organization_address='Lysfjun Torg 1  Lysfjun  NO NO-1234'),
            OuiEntry(registry='MA-L', assignment='334455',
                     organization_name='Panazonica Automotive Systems Co.,Ltd',
                     organization_address='1337 Matsumoto City Nagano JP 100-1234'),
            OuiEntry(registry='MA-L', assignment='111333',
                     organization_name='Barista Networks',
                     organization_address='1234 Great America Parkway Santa Clara CA US 98765'),
            OuiEntry(registry='MA-L', assignment='A1A1A1',
                     organization_name='Semsung Electronics Co.,Ltd',
                     organization_address='#83-1, Imtoo-Long Gummi Gyeongbook'),
            OuiEntry(registry='MA-L', assignment='123456',
                     organization_name='Semsung Electronics Co.,Ltd',
                     organization_address='#83-1, Imtoo-Long Gummi Gyeongbook')
        ]

        # Load the test database
        oui_db.load_database()

        # Retrieve the loaded OUI entries
        loaded_entries = oui_db.get_entries()

        # Assert that the loaded entries match the expected entries
        self.assertEqual(len(loaded_entries), len(expected_entries))
        for loaded_entry, expected_entry in zip(loaded_entries, expected_entries):
            self.assertEqual(loaded_entry.registry, expected_entry.registry)
            self.assertEqual(loaded_entry.assignment, expected_entry.assignment)
            self.assertEqual(loaded_entry.organization_name, expected_entry.organization_name)
            self.assertEqual(loaded_entry.organization_address, expected_entry.organization_address)

    def test_lookup_existing_mac(self):
        """ Test the database lookup using an existing MAC address. """

        # Setup the database instance
        oui_db = OuiDatabase(self.temp_file_path)
        oui_db.load_database()

        # Test for an existing MAC address
        mac_address = 'A1:B2:C3:33:44:55'
        expected_entry = OuiEntry(registry='MA-L', assignment='A1B2C3', organization_name='Nevigon',
                                  organization_address='Lysfjun Torg 1  Lysfjun  NO NO-1234')

        # Perform the lookup
        result = oui_db.lookup(mac_address)

        # Assert the result
        self.assertEqual(result, expected_entry)

    def test_lookup_non_existing_mac(self):
        """ Test the database lookup using an non-existing MAC address. """

        # Setup the database instance
        oui_db = OuiDatabase(self.temp_file_path)
        oui_db.load_database()

        # Test for a non-existing MAC address
        mac_address = 'FF:FE:FD:44:55:66'

        # Perform the lookup
        result = oui_db.lookup(mac_address)

        # Assert the result
        self.assertIsNone(result)

    def test_search_existing_organization(self):
        """ Test the database search using an existing organization name. """

        # Setup the database instance
        oui_db = OuiDatabase(self.temp_file_path)
        oui_db.load_database()

        # Test for an existing organization
        organization_name = 'Semsung Electronics Co.,Ltd'
        expected_results = [
            OuiEntry(registry='MA-L', assignment='A1A1A1',
                     organization_name='Semsung Electronics Co.,Ltd',
                     organization_address='#83-1, Imtoo-Long Gummi Gyeongbook'),
            OuiEntry(registry='MA-L', assignment='123456',
                     organization_name='Semsung Electronics Co.,Ltd',
                     organization_address='#83-1, Imtoo-Long Gummi Gyeongbook')
        ]

        # Perform the search
        results = oui_db.search(organization_name)

        # Assert the results
        self.assertEqual(results, expected_results)

    def test_search_non_existing_organization(self):
        """ Test the database search using an non-existing organization name. """

        # Setup the database instance
        oui_db = OuiDatabase(self.temp_file_path)
        oui_db.load_database()

        # Test for a non-existing organization
        organization_name = 'XYZ Company'

        # Perform the search
        results = oui_db.search(organization_name)

        # Assert the results
        self.assertEqual(results, [])

    def test_database_age(self):
        """ Create a sample database file which is 5 days old. """

        # Create a sample database file
        database_file = 'sample_database.csv'
        with open(database_file, 'w', encoding='utf8') as file:
            file.write('Registry,Assignment,Organization Name,Organization Address\n')
            file.write('MA-L,001122,PiPlus Microelectronics Limited,123 Building 1 ' \
                                 'No.123 Shedang Xia Road Shanghai\n')
            file.write('MA-L,AABBCC,Boomerang Corporation,"#100,00, Jongram, ' \
                                'Songbook Seoul "\n')

        # Get the current datetime and subtract five days
        current_datetime = datetime.datetime.now()
        modified_datetime = current_datetime - datetime.timedelta(days=5)

        # Get the modified timestamp in seconds
        modified_timestamp = modified_datetime.timestamp()

        # Update the modified time of the sample database file
        os.utime(database_file, (modified_timestamp, modified_timestamp))

        # Create an instance of OuiDatabase
        database = OuiDatabase(database_file)

        # Set the database file in the instance
        database.load_database()

        # Calculate the expected age in days
        expected_age = 5

        # Call the database_age() method
        result = database.database_age()

        # Assert that the result matches the expected age
        self.assertEqual(result, expected_age)

        # Clean up the sample database file
        os.remove(database_file)
