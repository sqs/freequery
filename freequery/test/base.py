import unittest, commands

def sh(s):
    return commands.getoutput(s).strip()

class IntegrationTestCase(unittest.TestCase):
    
    def setUp(self):
        self.clear_tmp()
    
    def tearDown(self):
        self.clear_tmp()

    def clear_tmp(self):
        sh("rm -rf /tmp/fq-test/")
        sh("mkdir /tmp/fq-test/")        
