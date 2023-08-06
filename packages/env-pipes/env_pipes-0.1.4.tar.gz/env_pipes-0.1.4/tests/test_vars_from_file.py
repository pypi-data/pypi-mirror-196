#python
'''
Testing of vars generation in env_pipes
'''

import pathlib
import unittest

import env_pipes

PARENT_DIR = pathlib.Path( __file__ ).parent

class TestVarsFromFile(unittest.TestCase):
	'''
	Tests for the vars_from_file method
	'''

	def setUp(self):
		self.test_object = env_pipes.EnvironmentalPipes.vars_from_file
		self.files_dir = PARENT_DIR / 'fixtures'

	def test_run_empty(self):
		'''
		Test vars_from_file without files
		'''

		self.assertEqual('', self.test_object())

	def test_single_file(self):
		'''
		Test vars_from_file with a single file
		'''

		self.assertEqual('key1=value1 key2=value2 key3=value3', self.test_object(self.files_dir / 'vars1.json'))

	def test_multiple_files(self):
		'''
		Test vars_from_file with multiple files
		'''

		expected_result = 'key1=value1 key2=value2 key3=value3 altkey1=altvalue1 altkey2=altvalue2 altkey3=altvalue3'
		self.assertEqual(expected_result, self.test_object(self.files_dir / 'vars1.json', self.files_dir / 'vars2.json'))

	def test_uppercase_vars(self):
		'''
		Test vars_from_file with a single file and uppercase vars
		'''

		self.assertEqual('KEY1=value1 KEY2=value2 KEY3=value3', self.test_object(self.files_dir / 'vars1.json', uppercase_vars = True))

