import unittest
import binascii
from akea import qrakea
from akea import akea

ref_hash_data = ('./akea_test_dummies/test_dummie1.txt', '_sha512-336x_', 'ae23766d87092cd29d648cd74c0db7f2259d7515b0633cc312b15a819eb396944a2c81fc8d9286ccae18')

class QRAKEAtest(unittest.TestCase):

    def testQRAKEA_QR_gen_and_read_functions(self):
        """Test the QRAKEA QR functions.

        Test all QRAKEA basic functions by generating a QR image and decode it again..

        Args:
            self: object

        Returns:
            None
        """
        file_path = './akea_test_dummies/test_dummie1.txt'
        data = akea.hex_digest(file_path)
        self.assertEqual(data, ref_hash_data)
        img = qrakea.generate_qr_code(data)
        img.save(file_path+'.qrakea', format='PNG', dpi=(600, 600))

        re_read_data = qrakea.get_qr_image(file_path+'.qrakea')
        self.assertEqual(binascii.unhexlify(data[2]), re_read_data)


if __name__ == "__main__":
    unittest.main()