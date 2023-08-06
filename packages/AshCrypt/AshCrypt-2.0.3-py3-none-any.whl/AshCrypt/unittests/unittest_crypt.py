import unittest
import struct
import AshCrypt.crypt as Ash


class AshModuleTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.message1 = 'Hello there testing if it works'
        self.message2 = b'this is bytes now'
        self.mainkey = '6ce113be19e898c2b98df82b7fa8efb166928925fc05574a54eb1114c3410900'
        self.ins1 = Ash.Enc(message=self.message1, mainkey=self.mainkey)
        self.string_message = self.ins1.enc_to_str()
        self.bytes_message = self.ins1.enc_to_bytes()
        self.ins2 = Ash.Dec(message=self.bytes_message, mainkey=self.mainkey)

    def tearDown(self) -> None:
        pass

    def test_KeyLength(self):
        self.assertEqual(32, bytes.fromhex(Ash.Enc.genkey()).__len__())

    def test_KeyType(self):
        self.assertIs(str, type(Ash.Enc.genkey()))

    def test_HMAC(self):
        self.assertTrue(self.bytes_message[:64] == self.ins1.HMAC())

    def test_IV(self):
        self.assertTrue(self.bytes_message[64:80] == self.ins1.iv)

    def test_Salt(self):
        self.assertTrue(self.bytes_message[80:96] == self.ins1.salt)

    def test_Pepper(self):
        self.assertTrue(self.bytes_message[96:112] == self.ins1.pepper)

    def test_Iterations(self):
        self.assertTrue(
            self.bytes_message[112:116] == self.ins1.setup_iterations())

    def test_Ciphertext(self):
        self.assertTrue(self.bytes_message[116:] == self.ins1.ciphertext())

    def test_TypeIterations(self):
        self.assertIs(bytes, type(self.ins1.setup_iterations()))

    def test_IterationsFixed_size(self):
        self.assertEqual(4, self.ins1.setup_iterations().__len__())

    def test_EncOutputBytes(self):
        self.assertIs(bytes, type(self.ins1.enc_to_bytes()))

    def test_EncOutputString(self):
        self.assertIs(str, type(self.ins1.enc_to_str()))

    def test_HMAC_Comp(self):
        self.assertEqual(self.ins1.HMAC(), self.ins2.rec_hmac)

    def test_IV_Comp(self):
        self.assertEqual(self.ins1.iv, self.ins2.rec_iv)

    def test_Salt_Comp(self):
        self.assertEqual(self.ins1.salt, self.ins2.rec_salt)

    def test_Pepper_Comp(self):
        self.assertEqual(self.ins1.pepper, self.ins2.rec_pepper)

    def test_Iterations_Comp(self):
        self.assertEqual(self.ins1.iterations, self.ins2.rec_iterations)

    def test_Ciphertext_Comp(self):
        self.assertEqual(self.ins1.ciphertext(), self.ins2.rec_ciphertext)

    def test_HMAC_MismatchError(self):
        tampered_HMAC = self.ins1.enc_to_bytes()[:63] + b'1'
        tampered_message = tampered_HMAC + self.ins1.enc_to_bytes()[64:]
        with self.assertRaises(Ash.MessageTamperingError):
            Ash.Dec(message=tampered_message, mainkey=self.mainkey)

    def test_IterationsOutOfRangeError2(self):
        enb = self.ins1.enc_to_bytes()
        tampered_message = enb[:112] + struct.pack('!I', 100001) + enb[116:]
        with self.assertRaises(Ash.IterationsOutofaRangeError):
            Ash.Dec(message=tampered_message, mainkey=self.mainkey)

    def test_DecOutputBytes(self):
        self.assertEqual(bytes, type(self.ins2.dec_to_bytes()))

    def test_DecOutputString(self):
        self.assertEqual(str, type(self.ins2.dec_to_str()))


if __name__ == '__main__':
    unittest.main()
