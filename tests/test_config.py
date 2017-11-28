import unittest

from fsimport.config import load_config
from fsimport.mapping import Mapping

class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def test_01(self):
        """load simple mapping file"""
        tpl_file = open('tests/fixtures/01_mapping.yaml')
        mapping = Mapping(tpl_file, {})

    def test_02(self):
        """load simple mapping file"""
        tpl_file = open('tests/fixtures/02_mapping.yaml')
        mapping = Mapping(tpl_file, { 'app_home': '/tmp' })

    def test_load_config(self):
        """test loading configuration"""
        config = load_config()

