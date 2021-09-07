import re
import decorators as decorators
from hooks.hook_manager import HookManager
from views.__parser__ import RequestParser
from flask import current_app, jsonify, request, url_for
from flask.views import MethodView


class Recipient(MethodView):
    """
    Adds a recipient to the database. A recipient represents another webserver
    that is interested in the data saved on THIS server. There are two kinds
    of recipeints: remote clipboards and webhook. A clipboard will get
    virtually and data saved on the server while a webhook may subscribe to
    specific mimetypes it is interested in.
    """

    def __init__(self):
        self.parser = RequestParser(current_app.MAX_CONTENT_LENGTH)
        self.hook_manager = HookManager()
        self.db = current_app.db

    @decorators.access_hooks
    def post(self):
        """
        Adds another recipient. Depending on the URL, the request was sent
        to, it will be treated as a webhook or a clipboard.
        """
        if request.headers.get('CONTENT-TYPE') not in 'application/json':
            return jsonify(error='Please send aplication/json'), 415
        data = request.get_json()

        if 'url' not in data:
            return jsonify(error='No url specified'), 400
        url = data['url']

        if Recipient.__is_valid_url__(url):
            is_hook = 'hooks' in request.url
            r = self.db.add_recipient(url, is_hook, data.get('subscribed_types', None))
            return jsonify(_id=r['_id'],
                           response_url=url_for('clip', _external=True)), 201
        else:
            return 'Sent value for url was not an acceptable url', 422

    @staticmethod
    def __is_valid_url__(url):
        """
        Sanity-check to see if the data sent by the recipient seems to be
        an URL, might be imporoved
        """
        return re.match(r'^http://', url)