from django.test import TestCase

class TestHome(TestCase):
    def test_home(self):
        res = self.client.get('/')
        self.assertContains(res, 'Freequery Search')
        

