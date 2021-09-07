from exceptions import ParentNotFoundException, SameMimetypeException, GrandchildException
from hooks.hook_manager import HookManager
from views.__parser__ import RequestParser
from flask import current_app, jsonify, url_for
from flask.views import MethodView

class BaseClip(MethodView):
    """
    This Method view acts a parent-class for all following classes
    and provides several utility-methods for them like checking
    the objects received from  the database for errors and returning
    the correct error-code.
    It is not intended to act as a view like its subclasses and has no methods
    implemented for processing requests, this should be done by subclasses.
    """

    def __init__(self):
        self.parser = RequestParser(current_app.MAX_CONTENT_LENGTH)
        self.hook_manager = HookManager()
        self.db = current_app.db
        self.emitter = current_app.emitter

    def _load_pre_hooks(self):
        return []

    def resolve_error(self, new_item):
        """
        Checks if any errors occured during adding of child and
        returns directly aborts the request with an error code
        Works similar to passing of errors in Django
        """
        if 'error' in new_item:
            error = new_item['error']
            if isinstance(error, ParentNotFoundException):
                return jsonify(error='Parent specified by request not found '
                               + 'on server.'), 412
            elif isinstance(error, SameMimetypeException):
                return jsonify(error='Entry has same mimetype specified '
                               + 'as parent'), 422
            elif isinstance(error, GrandchildException):
                return jsonify(error='Can only create child for '
                               + 'original entry'), 422
            else:
                return None

    def set_headers(self, res, clip):
        """
        Iterates over all items of a clip and puts them into custom
        HTTP-headers prefixed with X-C2-
        Also sets the Content-Disposition- and Location-header as needed.
        """
        clip['mimetype'] = clip['mimetype'] + "; charset=utf8"
        res.headers['Content-Type'] = clip.pop('mimetype')
        for key, value in clip.items():
            res.headers['X-C2-{}'.format(key)] = value
        if 'filename' in clip:
            res.headers['Content-Disposition'] = \
                'inline; filename={}'.format(clip['filename'])
        res.headers['Location'] = url_for('clip_details',
                                          clip_id=clip['_id'],
                                          _external=True)