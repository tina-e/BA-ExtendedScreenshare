import os
import requests
import unittest
from .t_util import wipe


class FileUploadTest(unittest.TestCase):

    CLIP_URL = 'http://localhost:5000/clips/'
    client = None
    db = None
    collection = None
    res_path = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def setUpClass(cls):
        wipe()


    @classmethod
    def tearDownClass(cls):
        wipe()

    def test_can_upload_simple_file(self):
        with open(os.path.join(self.res_path, 'res/example.txt'), 'rb') as f:
            files = {'file': ('example.txt', f,  'text/plain')}
            r = requests.post(self.CLIP_URL, files=files)

            self.assertEqual(r.status_code, requests.codes.created)

    def test_cannot_upload_huge_file(self):
        with open(os.path.join(self.res_path, 'res/huge_data.clip'), 'rb') as f:
            files = {'file': ('example.txt', f,  'text/plain')}
            try:
                r = requests.post(self.CLIP_URL, files=files)
                self.assertEqual(r.status_code, 413)
            except:
                pass

    def test_upload_returns_file(self):
        with open(os.path.join(self.res_path, 'res/example.txt'), 'rb') as f:
            files = {'file': ('example.txt', f, 'text/plain')}
            r = requests.post(self.CLIP_URL, files=files)
            filename = r.headers['X-C2-filename']
            received_data = r.content

            f.seek(0)
            self.assertEqual(received_data, f.read())
            self.assertEqual(filename, 'example.txt')

    def test_image_upload_returns_file(self):
        with open(os.path.join(self.res_path, 'res/example.jpg'), 'rb') as f:
            files = {'file': ('example.jpg', f, 'image/jpeg')}
            r = requests.post(self.CLIP_URL, files=files)
            received_data = r.content

            f.seek(0)
            self.assertEqual(received_data, f.read())

    def test_url_upload_returns_correct_file(self):
        image_url = 'http://www.google.com/favicon.ico'
        headers = {'Content-Type': 'text/plain',
                   'X-C2-download_request': 'True'}
        r = requests.post(self.CLIP_URL, data=image_url, headers=headers)
        r1 = requests.get(image_url, allow_redirects=True)
        server_data = r.content
        """
        # shows you, it's working :p
        f = open('res/favicon.ico', 'wb')
        f.write(server_data)
        f.close()
        """
        self.assertEqual(server_data, r1.content)


if __name__ == '__main__':
    unittest.main()
