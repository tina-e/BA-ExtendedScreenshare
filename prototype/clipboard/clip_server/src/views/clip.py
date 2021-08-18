import decorators as decorators
from exceptions import ClipNotFoundException, NoClipsExistingException
from views.base_clip import BaseClip
from flask import abort, current_app, jsonify, make_response, request, url_for


class Clip(BaseClip):
    """
    This class deals with operations on a single clip such as changing
    its contents or getting alternative representations of the same data.
    """

    @decorators.access_hooks
    def get(self, clip_id=None):
        """
        Reroute get requests on single clip.
        :param clip_id: The id for the queried clip.
        :return:  The requested clip, throwing 404 if none is found
        """
        # gets the siblings and parent or children of a clip
        if request.url.endswith('/alternatives/'):
            return self.__get_alternatives__(clip_id)

        # returns the last added parent-clip
        elif request.url.endswith('/latest/'):
            return self.__get_latest__()

        # returns the spcified clip or a sibling according to the CN
        else:
            preferred_type = None
            if request.accept_mimetypes.best != '*/*':  # Default value
                # Already sorted by Werkzeug
                preferred_type = request.accept_mimetypes
            return self.__get_by_id__(clip_id, preferred_type)

    def __get_by_id__(self, clip_id, preferred_type):
        """
        Queries the database for a clip with the specified uuid.
        :return: Json representation of the clip or None if no clip found
        """
        try:
            if('ignore-accept-types' in request.args):
                clip = current_app.db.get_clip_by_id(clip_id)
            else:
                clip = current_app.db.get_clip_by_id(clip_id, preferred_type)
        except ClipNotFoundException:
            return jsonify(error='No clip with specified id'), 404
        res = make_response(clip.pop('data'), 200)
        self.set_headers(res, clip)
        return res

    def __get_alternatives__(self, clip_id):
        """
        Gets a Json-Array containg id and mimetype of all related
        (child, siblings or parent) entries of clip_id
        :returns: Said array or None, if clip_id not found in db
        """
        clips = self.db.get_alternatives(clip_id)
        clips = list(map(Clip.__add_url__, clips))
        return jsonify(clips), 300

    def __get_latest__(self):
        """
        Returns the last added parent clip
        """
        try:
            clip = self.db.get_latest_clip()
            res = make_response(clip.pop('data'), 200)
            self.set_headers(res, clip)
            return res
        except NoClipsExistingException:
            return jsonify(error='No clip with specified id'), 404

    @decorators.access_hooks
    def put(self, clip_id=None):
        """
        Updates the clip specified by clip_id
        """
        if clip_id is None:
            return jsonify(
                    error='Please specify an existing object to update'), 405
        data = self.parser.get_data_from_request(request)
        print(data)
        if not data:
            return jsonify(error='Could not parse data'), 400

        try:
            clip = self.db.update_clip(clip_id, data)
            self.emitter.send_to_recipients(clip,
                                            self.emitter.recipients,
                                            data.pop('from_hook', False),
                                            data.pop('sender_id', False))
            res = make_response(clip.pop('data'), 200)
            self.set_headers(res, clip)
            return res
        except ClipNotFoundException:
            return jsonify(error='No clip with specified id'), 404

    @decorators.access_hooks
    def delete(self, clip_id=None):
        """
        Deletes a clip from the collection. If a parent is deleted, this will also delete its children.
        :return: Id of deleted clip
        """
        if clip_id is None:
            return jsonify(
                    error='Please specify an existing object to delete'), 404
        try:
            self.db.delete_clip_by_id(clip_id=clip_id)
            return jsonify(_id=clip_id), 200
        except ClipNotFoundException:
            return jsonify(error='No clip with specified id'), 404

    @staticmethod
    def __add_url__(clip):
        """"
        Map method to add the url for a clip
        """
        clip['url'] = url_for('clip_details', clip_id=clip['_id'], _external=True)
        return clip