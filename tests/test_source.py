import unittest

from fsimport.source import get_source

class TestSource(unittest.TestCase):

    def setUp(self):
        pass

    def test_http(self):
        """load simple mapping file"""
        result = get_source('http://download.thinkbroadband.com/5MB.zip')

    def test_file(self):
        """load simple mapping file"""
        result = get_source('file://tests/fixtures/sample.zip')

