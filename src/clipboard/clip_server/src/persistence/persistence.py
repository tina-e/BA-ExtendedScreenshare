from datetime import datetime
from uuid import UUID, uuid4
from pathlib import Path
import os
from exceptions import (GrandchildException, ParentNotFoundException, ClipNotFoundException, NoClipsExistingException)
from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict
from appdirs import user_data_dir
folderPath = Path(user_data_dir('extensible-clipboard', 'extensible-clipboard'))
folderPath.mkdir(parents=True, exist_ok=True)
path = os.path.join(str(folderPath),'clips.db')
database = SqliteDatabase(path)
from persistence.__models__ import Clip, Recipient, PreferredTypes

################################################################################################
#
# SQLite peewee Implementation of database
#
################################################################################################


class Persistence:

    def __init__(self):
        print(path)
        database.create_tables([Clip, Recipient, PreferredTypes])

    def _get_parent(self, child):
        if(child['parent'] is None):
            return child
        else:
            q = Clip.select().where(Clip._id == child['parent'])
            if(q.count() < 1):
                return None
            else:
                return model_to_dict(q.get())

    def _get_children(self, parent):
        childrenCursor = Clip.select().where(Clip.parent == parent['_id']).execute()
        result = []
        for item in childrenCursor:
            result.append(model_to_dict(item))
        return result

    def _find_best_match(self, clip, preferred_types):
        """
        Searches all children of parent if a direct match for
        the specified mimetypes can be found.
        :param parent: Mongo-object, should have children in db
        :param preferred_types: List of tuples representing the Accept-header
            of the request. Format: ('text/plain', 1.0).
            The list is to be sorted by the rules of the Accept-header
        :return: The Mongo-object with the closes match. None, if no match
        """
        parent = self._get_parent(clip)
        children = self._get_children(parent)

        # first round, exact match
        for curr_type in preferred_types:
            if parent['mimetype'] == curr_type[0]:
                return parent
            for child in children:
                if child['mimetype'] == curr_type[0]:
                    return child

        # second round, wildcard match
        for curr_type in preferred_types:
            # Check if mimestring is wildcard and get part before the /
            mime_base = curr_type[0]
            if '*' in mime_base:
                mime_base = mime_base.split('/')[0]

                for child in children:
                    if mime_base in child['mimetype']:
                        return child

        # No exact or wildcard match, default to sent-in clip
        return clip

    def __get_uuidv4__(self):
        return (uuid4().__str__())

    def add_recipient(self, url, is_hook, subscribed_types):
        """
        Adds a recipient to the database. If there is already an recipient
        with the same URL, this will be returned instead. Subscribed types
        for a hook will be updated beforehand.

        :param url: The URL the recipient can be reached at
        :param is_hook: True, if recipient is a hook otherwise it will be
                        treated as a clipboard
        :param subscribed_types: List of mimetypes the hook is interested in.
                                 Will be ignored for clipboards
        """

        clipboards_with_url = Recipient.select().where(Recipient.url==url)
        if clipboards_with_url.count() > 0:
            return model_to_dict(clipboards_with_url.get())
        else:
            id = self.__get_uuidv4__()
            clipboard = Recipient.create(_id=id,url=url,is_hook=is_hook)
            clipboard.save()
            if subscribed_types:
                for type in subscribed_types:
                    newItem = PreferredTypes.create(parent=id, type=type)
                    newItem.save()
            return model_to_dict(Recipient.get(Recipient._id==id))

    def get_recipients(self):
        """
        Returns a list of all saved recipients represented as dicts
        """
        recipients = Recipient.select().execute()
        results = []
        for rec in recipients:
            current_recipient = model_to_dict(rec, backrefs=True)
            # TODO: refactor this to avoid cumbersome mapping
            current_recipient['preferred_types'] = list(map(lambda item: item['type'], current_recipient['preferred_types']))
            results.append(current_recipient)
        return results

    def create_child_clip(self, data):
        """
        Create a child clip.
        :param data:
        :return:
        """
        if Clip.select().where(Clip._id == data['parent']).count() < 1:
            raise ParentNotFoundException
        elif model_to_dict(Clip.select().where(Clip._id == data['parent']).get())['parent'] is not None:
            raise GrandchildException
        return self.create_clip(data)

    def create_clip(self, data):
        """
        Create a new clip.
        :param data:
        :return:
        """
        id = self.__get_uuidv4__()
        clip = Clip.create(
            _id=id,
            mimetype=data['mimetype'],
            creation_date=str(datetime.now()),
            last_modified=str(datetime.now()),
            data=data['data'],
            src_app=data.get('src_app'),
            filename=data.get('filename'),
            parent=data.get('parent')
        )
        clip.save()
        return model_to_dict(Clip.get(Clip._id==id))

    def get_clip_by_id(self, clip_id, preferred_types=None):
        """
        Get clip with a certain id or a better fitting alternative mimetype for it.
        :param clip_id:
        :param preferred_types:
        :return:
        """
        q = Clip.select().where(Clip._id == clip_id)
        clip = None
        if(q.count() < 1):
            raise ClipNotFoundException
        else:
            clip = model_to_dict(q.get())
        if preferred_types and clip['mimetype'] is not preferred_types[0]:
            clip = self._find_best_match(clip, preferred_types)
        return clip

    def get_all_clips(self):
        """
        Get overview on all clips
        :return:
        """
        # Exclude 'data' from fetch (would be too large)
        clips_cursor = Clip.select(
            Clip._id,
            Clip.mimetype,
            Clip.creation_date,
            Clip.src_app,
            Clip.filename,
            Clip.parent
        ).execute()
        results = list(map(lambda item: model_to_dict(item), clips_cursor))
        return results

    def delete_all_clips(self):
        """
        Delete all clips from database (DANGEROUS, protected through pre_hooks)
        :return:
        """
        return Clip.delete().execute()

    def delete_clips_before(self, date):
        """
        Delete all clips posted earlier than date.
        :param date:
        :return:
        """
        return Clip.delete().where(Clip.creation_date < date).execute()

    def get_latest_clip(self):
        """
        Fetch the newest parent clip.
        :return:
        """
        q = Clip.select().where(Clip.parent.is_null()).order_by(Clip.creation_date.desc())
        if q.count() < 1:
            raise NoClipsExistingException
        else:
            return model_to_dict(q.get())

    def delete_clip_by_id(self, clip_id):
        """
        Delete clip with specified ID
        :param clip_id:
        :return:
        """
        q = Clip.select().where(Clip._id == clip_id)
        if q.count() < 1:
            raise ClipNotFoundException
        return Clip.delete().where((Clip._id==clip_id) | (Clip.parent==clip_id)).execute()

    def get_alternatives(self, clip_id):
        """
        Returns all siblings and the parent for clip_id
        as a list of dicts
        """
        q = Clip.select().where(Clip._id == clip_id)
        if q.count() < 1:
            raise ClipNotFoundException
        else:
            q = q[0]
            query =  ((Clip._id==clip_id) | (Clip.parent==q.parent)| (Clip._id==q.parent))
            if not q.parent:
                query = ((Clip._id==clip_id) | (Clip.parent==q._id))
            clips_cursor = Clip.select(
                Clip._id,
                Clip.mimetype,
                Clip.creation_date,
                Clip.src_app,
                Clip.filename,
                Clip.parent
            ).where(query).execute()
            clips = list(map(lambda item: model_to_dict(item), clips_cursor))
            return clips

    def update_clip(self, object_id, data):
        """
        Update clip with a certain ID with input data.
        :param object_id:
        :param data:
        :return:
        """
        q = Clip.select().where(Clip._id == object_id)
        if q.count() < 1:
            raise ClipNotFoundException
        else:
            clip = q.get()
            clip.data = data['data']
            clip.last_modified = str(datetime.now())
            clip.save()
            return model_to_dict(Clip.get_by_id(object_id))