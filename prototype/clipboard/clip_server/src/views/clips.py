import decorators as decorators
from views.base_clip import BaseClip
from flask import abort, current_app, jsonify, make_response, request, url_for


class Clips(BaseClip):
    """
    Class responsible for handling a set of Clips
    """

    @decorators.access_hooks
    def post(self):
        """
        Create a new clip
        """
        data = self.parser.get_data_from_request(request)
        if not data:
            return jsonify(error='Unable to parse data'), 400
        elif 'error' in data:
            return jsonify(error=data['error']), 413
        elif 'parent' in data:
            return jsonify(error='Please send to url of intended parent'), 42

        new_item = decorators.commit_hooks(self.db.create_clip)(self, data=data)

        decorators.notify_hooks(self.emitter.send_to_recipients)(
            self,
            new_item,
            self.emitter.recipients,
            data.pop('from_hook', False),
            data.pop('sender_id', ''),
        )

        res = make_response(new_item.pop('data'), 201)
        self.set_headers(res, new_item)
        return res

    @decorators.access_hooks
    def get(self):
        """
        Get all clips from the db. This will not get their data to reduce
        the amount of data sent to the clients. To get the data, one has
        to request the clip directly by its url ( /clip/{CLIP_ID}/
        """
        clips = self.db.get_all_clips()

        if clips is None:
            return jsonify(error='No clips saved yet'), 404
        else:
            clips = list(map(Clips.__add_url__, clips))
            return jsonify(clips), 200

    @decorators.access_hooks
    def delete(self):
        """
        Remove all clips from database, or by option just the ones older than a certain date.
        """
        before_date = request.args.get('before')
        result = None
        if before_date is None :
            result = self.db.delete_all_clips()
        else:
            result = self.db.delete_clips_before(before_date)
        if result is not None:
            return "Clips Deleted Successfully", 200
        else:
            return "Error deleting multiple clips", 500

    @staticmethod
    def __add_url__(clip):
        """"
        Map method to add the url for a clip
        """
        clip['url'] = url_for('clip_details', clip_id=clip['_id'], _external=True)
        return clip