"""This module provides classes and functions for AES-256 encryption and decryption"""


from typing import Union
import hmac as hmc
import base64
import os
import struct
import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import padding


class IterationsOutofRangeError(Exception):
    """Exception raised when iterations come to be out of range usually due to message tampering
    where the bytes representing the KDF iterations get touched"""

    def __init__(self, num: any) -> None:
        self.display = f'Iterations must be between 50 and 100000. RECEIVED : {num} '
        super().__init__(self.display)


class Enc:
    """Class to encrypt data of either type bytes or strings"""

    def __init__(self, message: Union[str, bytes], mainkey: str) -> None:
        if isinstance(message, str):
            self.message = message.encode()
        elif isinstance(message, bytes):
            self.message = message

        self.mainkey = mainkey
        self._iv = os.urandom(16)
        self.salt = os.urandom(16)
        self.pepper = os.urandom(16)
        self.iterations = 50
        if self.iterations < 50 or self.iterations > 100000:
            raise IterationsOutofRangeError(self.iterations)
        self.enc_key = self.derkey(self.mainkey, self.salt, self.iterations)
        self.hmac_key = self.derkey(self.mainkey, self.pepper, self.iterations)

    @staticmethod
    def derkey(mainkey: str, salt_pepper: bytes, iterations: int) -> bytes:
        """AES Key & HMAC derivation function"""
        return bcrypt.kdf(
            password=mainkey.encode('UTF-8'),
            salt=salt_pepper,
            desired_key_bytes=32,
            rounds=iterations)

    @staticmethod
    def genkey() -> str:
        """Generates a random 256-bit key as a hex string."""
        return os.urandom(32).hex()

    def mode(self):
        """Returns AES Cipher Block Chaining (CBC) mode with the chosen initialization vector"""
        return modes.CBC(self._iv)

    def cipher(self):
        """Creates AES cipher object using the encryption key and CBC mode"""
        return Cipher(
            algorithms.AES(
                key=self.enc_key),
            mode=self.mode(),
            backend=default_backend())

    def cipher_encryptor(self):
        """Returns the encryptor for the AES cipher"""
        return self.cipher().encryptor()

    def padded_message(self) -> bytes:
        """Pads the message to a multiple of the block size using PKCS#7 padding"""
        padder = padding.PKCS7(128).padder()
        return padder.update(self.message) + padder.finalize()

    def ciphertext(self) -> bytes:
        """Encrypts the padded message using AES and returns the ciphertext"""
        return self.cipher_encryptor().update(self.padded_message()) + \
            self.cipher_encryptor().finalize()

    def hmac(self) -> bytes:
        """Computes the HMAC-SHA512 of the ciphertext"""
        _hmac = self.hmac_key
        _hmac = hmac.HMAC(_hmac, hashes.SHA512())
        _hmac.update(self.ciphertext())
        return _hmac.finalize()

    def setup_iterations(self) -> bytes:
        """Packs the number of iterations into bytes using the 'big-endian' format"""
        iters_bytes = struct.pack('!I', self.iterations)
        return iters_bytes

    def enc_to_bytes(self) -> bytes:
        """Returns the encrypted data as bytes in the form 'HMAC' -> 'IV'
        -> 'Salt value' -> 'pepper value' -> 'iterations' -> 'ciphertext """
        return self.hmac() + self._iv + self.salt + self.pepper + \
            self.setup_iterations() + self.ciphertext()

    def enc_to_str(self) -> str:
        """Returns a URL safe base 64 encoded string of the encrypted data"""
        return base64.urlsafe_b64encode(self.enc_to_bytes()).decode('UTF-8')


class MessageTamperingError(Exception):
    """Raised when any part of the message gets tampered with. DISCARD THE MESSAGE"""

    def __init__(self) -> None:
        self.display = 'HMAC mismatch ! Message has been TAMPERED with ,\n' \
                       ' or Possible key difference'
        super().__init__(self.display)


class Dec:
    """Class to decrypt data of either type bytes or strings"""

    def __init__(self, message: Union[str, bytes], mainkey: str) -> None:
        if isinstance(message, str):
            mess = message.encode('UTF-8')
            self.message = base64.urlsafe_b64decode(mess)
        elif isinstance(message, bytes):
            self.message = message
        self.key = mainkey
        self.rec_hmac = self.message[:64]
        self.rec_iv = self.message[64:80]
        self.rec_salt = self.message[80:96]
        self.rec_pepper = self.message[96:112]
        self.rec_iterations = struct.unpack('!I', self.message[112:116])[0]
        if self.rec_iterations < 50 or self.rec_iterations > 100000:
            raise IterationsOutofRangeError(self.rec_iterations)
        self.rec_ciphertext = self.message[116:]
        self.dec_key = Enc.derkey(self.key, self.rec_salt, self.rec_iterations)
        self.hmac_k = Enc.derkey(
            self.key,
            self.rec_pepper,
            self.rec_iterations)
        if self.verify_hmac() is False:
            raise MessageTamperingError()

    def calculated_hmac(self) -> bytes:
        """Computes the HMAC-SHA512 of the received ciphertext"""
        _hmac = self.hmac_k
        _hmac = hmac.HMAC(_hmac, hashes.SHA512())
        _hmac.update(self.rec_ciphertext)
        return _hmac.finalize()

    def verify_hmac(self) -> bool:
        """Verifies the received HMAC-SHA512 against the calculated HMAC"""
        return hmc.compare_digest(self.calculated_hmac(), self.rec_hmac)

    def mode(self):
        """Returns the AES Cipher Block Chaining (CBC) mode with the received  IV"""
        return modes.CBC(self.rec_iv)

    def cipher(self):
        """Creates an AES cipher object using the decryption key and CBC mode"""
        return Cipher(
            algorithms.AES(
                key=self.dec_key),
            mode=self.mode(),
            backend=default_backend())

    def cipher_decryptor(self):
        """Returns the decryptor for the AES cipher"""
        return self.cipher().decryptor()

    def pre_unpadding_dec(self) -> bytes:
        """Decrypts the received ciphertext and returns the pre-unpadded data"""
        return self.cipher_decryptor().update(self.rec_ciphertext) + \
            self.cipher_decryptor().finalize()

    def unpadded_m(self) -> bytes:
        """Unpads the pre-unpadded data and returns the original message """
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(self.pre_unpadding_dec()) + unpadder.finalize()

    def dec_to_bytes(self) -> bytes:
        """Returns the decrypted message as bytes"""
        return self.unpadded_m()

    def dec_to_str(self) -> str:
        """Returns the decrypted message as a UTF-8 encoded string"""
        return self.unpadded_m().decode('UTF-8')
