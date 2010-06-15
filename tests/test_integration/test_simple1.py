from freequery.test import IntegrationTestCase
from freequery.test.base import sh

class TestSimple1(IntegrationTestCase):

    def test_simple1(self):
        # add documents
        self.assertEquals("0",
            sh("python bin/add-document.py /tmp/fq-test/ " \
               "http://example.com '<h1>Welcome to example</h1>'"))
        self.assertEquals("1",
            sh("python bin/add-document.py /tmp/fq-test/ " \
               "http://apple.com '<h1>Welcome to Apple</h1>'"))

        # build forward index
        fwdindex = sh("python bin/make-forward-index.py " \
                      "/tmp/fq-test/ /tmp/fq-test/fwdindex 0 2")
        self.assertEquals(fwdindex,
                          "0\thttp://example.com\n1\thttp://apple.com")

        # build inverted index
        invindex = sh("python bin/make-inverted-index.py " \
                      "/tmp/fq-test/fwdindex /tmp/fq-test/invindex")
        self.assertEquals(invindex, "0\n1")

        # query
        query_cmd = "python bin/query.py /tmp/fq-test/ /tmp/fq-test/invindex "
        self.assertEquals("0\thttp://example.com\n1\thttp://apple.com",
                          sh(query_cmd + "welcome"))
        self.assertEquals("0\thttp://example.com", sh(query_cmd + "example"))
        self.assertEquals("1\thttp://apple.com", sh(query_cmd + "apple"))
        
        
                    
            
                       
