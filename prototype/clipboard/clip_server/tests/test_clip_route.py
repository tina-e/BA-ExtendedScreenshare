import requests
import unittest
from uuid import uuid4
import os
from .t_util import wipe


class SimpleTextServerTest(unittest.TestCase):

    CLIP_URL = 'http://localhost:5000/clips/'
    CLIP_ID_URL = 'http://localhost:5000/clips/{}/'
    client = None
    db = None
    collection = None

    @classmethod
    def setUpClass(cls):
        wipe()


    @classmethod
    def tearDownClass(cls):
        wipe()

    def test_latest_return_404_if_no_item(self):
        wipe()
        print(requests.get(self.CLIP_URL).content.decode())
        r = requests.get(self.CLIP_URL + 'latest/')
        self.assertEqual(r.status_code, 404)

    def test_get_same_mimetype(self):
        headers = {'Content-Type': 'text/plain'}
        r = requests.post(self.CLIP_URL, data='Clip 1', headers=headers)

        _id = r.headers['X-C2-_id']

        r = requests.get(self.CLIP_URL + _id)
        header = r.headers.get('content-type')
        self.assertIn('text/plain', header)

    def test_can_save_and_retrieve_single_item(self):
        headers = {'Content-Type': 'text/plain'}
        r = requests.post(self.CLIP_URL, data='Clip 1', headers=headers)
        self.assertEqual(r.status_code, requests.codes.created)

        _id = r.headers['X-C2-_id']
        r = requests.get(self.CLIP_URL + _id)
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertIn('Clip 1', r.text)

    def test_can_save_and_retrieve_multiple_items(self):
        headers = {'Content-Type': 'text/plain'}
        r = requests.post(self.CLIP_URL, data='Clip 1', headers=headers)
        self.assertEqual(r.status_code, requests.codes.created)
        object_id_1 = r.headers['X-C2-_id']

        r = requests.post(self.CLIP_URL, data='Clip 2', headers=headers)
        self.assertEqual(r.status_code, requests.codes.created)
        object_id_2 = r.headers['X-C2-_id']

        object_1 = requests.get(self.CLIP_URL + object_id_1)
        object_2 = requests.get(self.CLIP_URL + object_id_2)

        self.assertIn('Clip 1', object_1.text)
        self.assertNotIn('Clip 2', object_1.text)

        self.assertIn('Clip 2', object_2.text)
        self.assertNotIn('Clip 1', object_2.text)

    @unittest.skip
    def test_POST_need_correct_key(self):
        headers = {'Content-Type': 'text/plain'}
        r = requests.post(self.CLIP_URL, data={ 'mimetype': 'text/plain', 'wrong': 'key'})
        self.assertEqual(r.status_code, requests.codes.bad_request)

    def test_not_existing_id_raises_404(self):
        _id = uuid4()
        r = requests.get(self.CLIP_URL + str(_id))
        self.assertEqual(r.status_code, requests.codes.not_found)

    def test_POST_with_uuid_returns_405(self):
        r = requests.post(self.CLIP_ID_URL.format(str(uuid4())))
        self.assertEqual(r.status_code, requests.codes.method_not_allowed)

    @unittest.skip
    def test_GET_without_id_returns_all_clips(self):
        requests.post(self.CLIP_URL, json={
            'mimetype': 'text/plain',
            'data': 'Clip 1'})
        requests.post(self.CLIP_URL, json={
            'mimetype': 'text/plain',
            'data': 'Clip 2'})

        r = requests.get(self.CLIP_URL)
        objects = r.json()

        self.assertEqual(len(objects), 2)

    def test_PUT_needs_id(self):
        r = requests.put(self.CLIP_URL)
        self.assertEqual(r.status_code, requests.codes.method_not_allowed)

    def test_PUT_needs_existing_url(self):
        _id = uuid4()
        r = requests.put(self.CLIP_ID_URL.format(str(_id)),
                         json={'mimetype': 'text/plain', 'data': 'clip new'})

        self.assertEqual(r.status_code, requests.codes.not_found)

    def test_correct_PUT_returns_updated_clip(self):
        r = requests.post(self.CLIP_URL,
                          json={'mimetype': 'text/plain', 'data': 'old clip'})
        _id = r.headers['X-C2-_id']

        r = requests.put(self.CLIP_ID_URL.format(_id),
                         json={'mimetype': 'text/plain', 'data': 'new clip'})

        self.assertIn(_id, r.headers['X-C2-_id'])
        self.assertNotIn('old clip', r.text)
        self.assertIn('new clip', r.text)

    def test_delete_item_returns_no_content_on_success(self):
        r = requests.post(self.CLIP_URL,
                          json={'mimetype': 'text/plain',
                                'data': 'Test delete'})
        _id = r.headers['X-C2-_id']

        r = requests.delete(self.CLIP_ID_URL.format(_id))

        self.assertEqual(r.status_code, 200)


    def test_deleted_item_get_no_longer_returned(self):
        r = requests.post(self.CLIP_URL,
                          json={'mimetype': 'text/plain',
                                'data': 'Test delete'})
        _id = r.headers['X-C2-_id']
        r = requests.delete(self.CLIP_ID_URL.format(_id))
        r = requests.get(self.CLIP_ID_URL.format(_id))
        self.assertEqual(r.status_code, 404)

    def test_cannot_delete_non_existing_item(self):
        _id = str(uuid4())
        r = requests.delete(self.CLIP_ID_URL.format(_id))

        self.assertEqual(r.status_code, 404)

    def test_can_get_latest_item_by_shortcut(self):
        headers = {'Content-Type': 'text/plain'}
        requests.post(self.CLIP_URL,
                          data='First item',
                          headers=headers)
        requests.post(self.CLIP_URL,
                          data='Second item',
                          headers=headers)

        r = requests.get(self.CLIP_URL + 'latest/')
        text = r.text

        self.assertEqual(r.status_code, 200) 
        self.assertNotIn('First item', text)
        self.assertIn('Second item', text)


if __name__ == "__main__":
    unittest.main()
