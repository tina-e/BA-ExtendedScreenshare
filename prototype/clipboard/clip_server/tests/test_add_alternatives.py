import requests
import unittest
from uuid import uuid4, UUID
from .t_util import wipe


class SimpleTextServerTest(unittest.TestCase):

    CLIP_URL = 'http://localhost:5000/clips/'
    CLIP_ID_URL = 'http://localhost:5000/clips/{}/'
    ADD_CHILD_URL = CLIP_URL + 'children'
    client = None
    db = None
    collection = None

    @classmethod
    def setUpClass(cls):
        wipe()


    @classmethod
    def tearDownClass(cls):
        wipe()

    def create_parent(self):
        headers = {'Content-Type': 'text/plain'}
        r = requests.post(self.CLIP_URL,
                          data='parentClip',
                          headers=headers)
        return r.headers['X-C2-_id']

    def add_child(self, parent_id):
        headers = {'Content-Type': 'text/html'}
        r = requests.post(
                self.CLIP_URL + parent_id + '/children',
                data='<h1>Child text</h1>',
                headers=headers)
        return r

    def test_add_without_parent_fails(self):
        fake_id = uuid4()

        r = requests.post(
                self.CLIP_URL + str(fake_id) + '/children',
                json={'mimetype': 'text/plain',
                      'data': 'ClipChild',
                      'parent': str(fake_id)})

        self.assertEqual(r.status_code, 412)

    def test_add_child_returns_child(self):
        parent_id = self.create_parent()

        r = self.add_child(parent_id)

        self.assertEqual(r.status_code, 201)
        self.assertNotIn('parent', r.content.decode())

        try:
            UUID(r.headers['X-C2-parent'])
        except ValueError:
            self.fail('Cannot create UUID from {}'.format(
                r.headers['X-C2-parent']))

    @unittest.skip
    def test_child_must_have_different_mimetype(self):
        parent_id = self.create_parent()

        r = requests.post(
                self.CLIP_URL + parent_id + '/children',
                json={'mimetype': 'text/plain',
                      'data': 'ClipChild',
                      'parent': parent_id})
        self.assertEqual(r.status_code, 422)

    def test_server_honors_ACCEPT_header(self):
        parent_id = self.create_parent()
        self.add_child(parent_id)
        header = {'accept': 'text/html, '
                            + 'application/json;q=0.5, '
                            + 'text/plain;q=0.8'}

        r = requests.get(
            self.CLIP_URL + parent_id,
            headers=header
        )

        self.assertIn('<h1>Child text</h1>', r.content.decode())

    def test_wildcard_in_ACCEPT_header_honored(self):
        parent_id = self.create_parent()
        self.add_child(parent_id)

        r = requests.post(
                self.CLIP_URL + parent_id + '/children',
                json={'mimetype': 'application/json',
                      'data': '{"key": "json-child"}',
                      'parent': parent_id
                      })

        header = {'accept': 'application/*'}
        r = requests.get(
            self.CLIP_URL + parent_id,
            headers=header
        )

        json = r.json()
        self.assertIn('json-child', json['data'])

    def test_cannot_create_grandchildren(self):
        parent_id = self.create_parent()
        child = self.add_child(parent_id)
        child_id = child.headers['X-C2-_id']
        grandchild = self.add_child(child_id)

        self.assertEqual(grandchild.status_code, 422)
        self.assertIn(
                'Can only create child for original entry',
                grandchild.json()['error'])

    def test_ACCEPT_will_always_get_best_result(self):
        # parent: plain, child: html, query:child but prefers plains
        #   -> parent delivered
        parent_id = self.create_parent()
        child = self.add_child(parent_id)
        child_id = child.headers['X-C2-_id']

        header = {'accept': 'text/plain;q=0.8, text/html;q=0.3'}

        r = requests.get(
                self.CLIP_URL + child_id,
                headers=header
        )

        self.assertIn('parentClip', r.content.decode())

    def test_delete_parent_will_delete_children(self):
        parent_id = self.create_parent()
        child = self.add_child(parent_id)
        child_id = child.headers['X-C2-_id']
        r = requests.get(self.CLIP_URL + child_id)
        self.assertEqual(r.status_code, 200)

        r = requests.delete(self.CLIP_ID_URL.format(parent_id))
        self.assertEqual(r.status_code, 200)

        r = requests.get(self.CLIP_URL + child_id)
        self.assertEqual(r.status_code, 404)

    def test_can_get_list_of_alternatives(self):
        parent_id = self.create_parent()
        child = self.add_child(parent_id)
        child_id = child.headers['X-C2-_id']
        r = requests.get(self.CLIP_URL + parent_id + '/alternatives/')
        self.assertEqual(r.status_code, 300)

        self.assertIn(parent_id, r.text)
        self.assertIn(child_id, r.text)

    def test_unrelated_clip_is_not_returned(self):
        parent_id = self.create_parent()
        child = self.add_child(parent_id)
        child_id = child.headers['X-C2-_id']
        r = requests.post(self.CLIP_URL,
                          json={'mimetype': 'text/plain',
                                'data': 'WrongTurn'})

        wrong_id = r.headers['X-C2-_id']
        r = requests.get(self.CLIP_URL + parent_id + '/alternatives/')

        self.assertIn(parent_id, r.text)
        self.assertIn(child_id, r.text)
        self.assertNotIn(wrong_id, r.text)


if __name__ == '__main__':
    unittest.main()
