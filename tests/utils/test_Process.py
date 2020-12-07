from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Process import Process


class test_Process(TestCase):

    def test_run__ls(self):     # todo: add @patch('builtins.print') and confirm print data was correct
        result = Process.run('ls')
        #assert result == {'runParams': ['ls'], 'stderr': '', 'stdout': 'Test_Process.py\naws\n'}
        Dev.pprint(result)
        result = Process.run('ls', ['-la', '..'])
        #assert '-rw-r--r--@  1 dinis  staff  6148 Oct 29 11:59 .DS_Store\n' in result['stdout']
        Dev.pprint(result)

