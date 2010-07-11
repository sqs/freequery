from django.test import TestCase

class TestHome(TestCase):
    def test_home(self):
        res = self.client.get('/')
        self.assertContains(res, 'Freequery Search')

class TestResults(TestCase):
    def test_results_q_missing(self):
        res = self.client.get('/search')
        self.assertRedirects(res, '/')

    def test_results_q_empty(self):
        res = self.client.get('/search?q=')
        self.assertRedirects(res, '/')

    def test_results_q_whitespace(self):
        res = self.client.get('/search?q=%20%20')
        self.assertRedirects(res, '/')

    def test_results_q_in_title(self):
        res = self.client.get('/search?q=abc123')
        self.assertContains(res, '<title>abc123 - Freequery</title>')
