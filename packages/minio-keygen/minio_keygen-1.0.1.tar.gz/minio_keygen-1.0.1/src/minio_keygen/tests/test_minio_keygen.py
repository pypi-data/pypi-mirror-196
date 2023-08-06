"""minio keygen tests"""
import sys
import unittest

from minio_keygen import compute_keys, main


class TestMinioKeyGen(unittest.TestCase):
    """
    Test the compute_keys function from the minio_keygen library
    """

    def test_compute_keys_integers(self):
        '''Integer input'''
        result = compute_keys(14, 30)
        self.assertEqual(len(result[0]), 19) and self.assertEqual(len(result[1]), 40) # pylint: disable=expression-not-assigned

    def test_compute_keys_float(self):
        '''Float input'''
        result = compute_keys(14.5, 30.2)
        self.assertEqual(len(result[0]), 19) and self.assertEqual(len(result[1]), 40) # pylint: disable=expression-not-assigned

    def test_compute_keys_key_string(self):
        '''String input'''
        with self.assertRaises(SystemExit):
            compute_keys('g', 30)

    def test_compute_keys_token_string(self):
        '''String input'''
        with self.assertRaises(SystemExit):
            compute_keys(30, 'z')

    def test_main(self):
        '''Main function'''
        sys.argv=['']
        self.assertEqual(main(), None)
        