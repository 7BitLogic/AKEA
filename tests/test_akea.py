import unittest
from akea import akea

ref_binary_digest               = ('./akea_test_dummies/test_dummie1.txt', '_sha512-336_',b'\xae#vm\x87\t,\xd2\x9dd\x8c\xd7L\r\xb7\xf2%\x9du\x15\xb0c<\xc3\x12\xb1Z\x81\x9e\xb3\x96\x94J,\x81\xfc\x8d\x92\x86\xcc\xae\x18')
ref_binary_digest_with_folder   = ('./akea_test_dummies/', '_sha512-336_',[b'\xae#vm\x87\t,\xd2\x9dd\x8c\xd7L\r\xb7\xf2%\x9du\x15\xb0c<\xc3\x12\xb1Z\x81\x9e\xb3\x96\x94J,\x81\xfc\x8d\x92\x86\xcc\xae\x18', b'\xae#vm'])
ref_hex_digest                  = ('./akea_test_dummies/test_dummie1.txt', '_sha512-336x_','ae23766d87092cd29d648cd74c0db7f2259d7515b0633cc312b15a819eb396944a2c81fc8d9286ccae18')
ref_hex_digest_with_folder      = ('./akea_test_dummies/', '_sha512-336x_',['ae23766d87092cd29d648cd74c0db7f2259d7515b0633cc312b15a819eb396944a2c81fc8d9286ccae18', 'ae23766d'])



class AKEAtest(unittest.TestCase):

    def testAKEA_hash_and_file_functions(self):
        """Test the AKEA hashing functions.

        Test all AKEA basic functions by using some test files.

        Args:
            self: object

        Returns:
            None
        """
        self.assertEqual(akea.binary_digest('./akea_test_dummies/test_dummie1.txt'), ref_binary_digest)
        self.assertEqual(akea.hex_digest('./akea_test_dummies/test_dummie1.txt'), ref_hex_digest)
        self.assertEqual(akea.binary_digest('./akea_test_dummies/'), ref_binary_digest_with_folder)
        self.assertEqual(akea.hex_digest('./akea_test_dummies/'), ref_hex_digest_with_folder)



if __name__ == "__main__":
    unittest.main()