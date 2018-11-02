import unittest
from akea import dbakea
import configparser

class DBAKEAtest(unittest.TestCase):

    def testDBAKEA_hash_and_file_functions(self):
        """Test the DBAKEA hashing functions.

        Test  DBAKEA basic functions by creating and adding to dbakea base and
        than check backwards by reading the qrakea file.

        Args:
            self: object

        Returns:
            None
        """
        config = configparser.ConfigParser()
        config.read('test_akea.conf')
        dbakea.append_to_db('./akea_test_dummies/', config)     #E:/Programmieren/AKEA/tests
        dbakea_entry = dbakea.check_qr(config, './akea_test_dummies/test_dummie1.txt.qrakea')
        self.assertEqual(dbakea_entry, './akea_test_dummies\\test_dummie1.txt')

if __name__ == "__main__":
    unittest.main()