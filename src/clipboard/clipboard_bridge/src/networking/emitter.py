import requests
from requests import exceptions as req_exceptions


class ClipEmitter:
    """
    ClipSender on the other will send clips that were created locally and
    send them to the remote server.
    This was necessary since flask cannot take action itself withouth receiing
    a request
    """

    def __init__(self, clip_server_url, id_updater):
        self.post_url = clip_server_url + "clips/"
        self.add_child_url = self.post_url + "{}/children"
        self.id_updater = id_updater

    def _post_clip(self, clip, parent_id=None):
        """
        Sends a clip received from the local clipboard to the server
        """
        headers = {'Content-Type': clip['mimetype'],
                   'X-C2-sender_id': self._id, }
        if 'filename' in clip:
            headers['X-C2-filename'] = clip['filename']
        if parent_id:
            url = self.add_child_url.format(parent_id)
        else:
            url = self.post_url

        try:
            r = requests.post(
                url,
                headers=headers,
                data=clip['data'],
                timeout=100
            )
            r.raise_for_status()
        except req_exceptions.ConnectionError as e:
            print('Connection refused by server')
            r = None
        except req_exceptions.Timeout as e:
            print(e)
            print('Server failed to respond in time')
            r = None
        except req_exceptions.HTTPError as e:
            print('Remote server responded with statuscode {}\n'.format(
                r.status_code))
            print('Message from server: {}'.format(r.text))
            r = None
        return r

    def add_clips_to_server(self, clip_list):
        """
        Receives the current clipboard-data and pushes them onto the server
        """
        if not clip_list:
            return
        r = self._post_clip(clip_list[0])
        if r and r.status_code == 201:
            parent_id = r.headers['X-C2-_id']
            self.id_updater(parent_id)
            if len(clip_list) > 1:
                # adds subsequent entries as children of the first
                for c in clip_list[1:]:
                    r = self._post_clip(c, parent_id)