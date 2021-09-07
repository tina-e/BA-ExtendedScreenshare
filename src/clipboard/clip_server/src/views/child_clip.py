import decorators as decorators
from exceptions import GrandchildException, ParentNotFoundException, SameMimetypeException
from views.base_clip import BaseClip
from flask import abort, current_app, jsonify, make_response, request, url_for

class ChildClip(BaseClip):
    """
    Responsible for adding a child to an existing clip.
    Introduced to simplify the flow of the application.
    """

    @decorators.access_hooks
    def post(self, clip_id=None):
        data = self.parser.get_data_from_request(request)
        if not data:
            abort(400)
        data['parent'] = clip_id
        try:
            new_item = decorators.commit_hooks(self.db.create_child_clip)(self, data=data)
            decorators.notify_hooks(self.emitter.send_to_recipients)
            (
                self,
                new_item,
                self.emitter.recipients,
                data.pop('from_hook', False),
                data.pop('sender_id', '')
            )
            res = make_response(new_item.pop('data'), 201)
            self.set_headers(res, new_item)
            return res
        except GrandchildException:
            return jsonify(error='Can only create child for original entry'), 422
        except ParentNotFoundException:
            return jsonify(error='No parent with specified id'), 412