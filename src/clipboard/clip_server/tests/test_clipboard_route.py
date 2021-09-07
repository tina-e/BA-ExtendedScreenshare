import requests
import unittest
import os
from .t_util import wipe


class SimpleTextServerTest(unittest.TestCase):

    CLIP_URL = 'http://localhost:5000/clips/'
    CLIPBOARD_URL = 'http://localhost:5000/clipboards/'
    client = None
    db = None
    collection = None

    @classmethod
    def setUpClass(cls):
        wipe()


    @classmethod
    def tearDownClass(cls):
        wipe()

    def test_get_returns_json(self):
        r = requests.post(self.CLIP_URL, json={
            'mimetype': 'text/plain', 'data': 'Clip 1'})

        _id = r.headers['X-C2-_id']

        r = requests.get(self.CLIP_URL + _id)
        header = r.headers.get('content-type')
        self.assertIn('application/json', header)

    def test_register_returns_201_when_url(self):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.CLIPBOARD_URL + 'register',
                          headers=headers,
                          json={'url': 'http://localhost:5010/'})
        self.assertEqual(r.status_code, 201)

    def test_server_only_accepts_json(self):
        r = requests.post(self.CLIPBOARD_URL + 'register',
                          data={'url': 'http://localhost:5010/'})
        self.assertEqual(r.status_code, 415)

    def test_server_refuses_non_url(self):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.CLIPBOARD_URL + 'register',
                          headers=headers, json={'url': 'notAnURL'})
        self.assertEqual(r.status_code, 422)


if __name__ == '__main__':
    unittest.main()
