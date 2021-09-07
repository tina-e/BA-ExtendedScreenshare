from flask import Flask, url_for

from event_emitter import ClipEventEmitter

from views.clips import Clips
from views.clip import Clip
from views.recipient import Recipient
from views.child_clip import ChildClip

class Server(Flask):
    """
    Wrapper around the Flask-server adding custom logic.
    Also responsible for passing data to the database and to send
    newly added data to the webhooks or remote clipboards registered to
    the server.
    """

    # Bigger requests will be discarded. Currently 15MB
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    def __init__(self, app_name, database, port=5000):
        super(Server, self).__init__(app_name)
        self.db = database
        self.port = port
        self.emitter = ClipEventEmitter(database)


        # TODO: these instance variables belong somewhere else
        # self.current_clip = ''
        self.config['MAX_CONTENT_LENGTH'] = self.MAX_CONTENT_LENGTH
        self.__init_routing()


    def __init_routing(self):
        """
        Since we use class-based routing for the server, we cannot utilize
        the decorators provided by Flask and instead have to plug in the
        routes manually
        """
        clip_view = Clip.as_view('clip')  # 'clip' can be used in url_for
        clip_details = Clip.as_view('clip_details')
        clip_list_view = Clips.as_view('clip_list')
        child_add_view = ChildClip.as_view('child_adder')
        recipient_view = Recipient.as_view('recipient')

        self.add_url_rule('/clips/',
                                       view_func=clip_list_view,
                                       methods=['GET', 'POST', 'DELETE'])
        self.add_url_rule('/clips/latest/',
                                       view_func=clip_view,
                                       methods=['GET'])
        self.add_url_rule('/clips/<uuid:clip_id>/',
                                       view_func=clip_details,
                                       methods=['GET', 'DELETE',
                                                'PUT', ])
        self.add_url_rule('/clips/<uuid:clip_id>/'
                                       + 'alternatives/',
                                       view_func=clip_view,
                                       methods=['GET'])
        self.add_url_rule('/clips/<uuid:clip_id>/children',
                                       view_func=child_add_view,
                                       methods=['POST'])
        self.add_url_rule('/clipboards/register',
                                       view_func=recipient_view,
                                       methods=['POST'])
        self.add_url_rule('/hooks/register',
                                       view_func=recipient_view,
                                       methods=['POST'])


    def start(self):
        """
        Starts the Flask development-server. Cannot use autoreload
        because it runs in a seperate thread
        """
        self.run(debug=False, use_reloader=False,
                 host='0.0.0.0', port=self.port)
