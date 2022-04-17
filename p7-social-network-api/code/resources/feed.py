from flask_restful import Resource

from cache import feed_cache, related_cache, CacheManager
from models.task import TaskModel


class Feed(Resource):

    def get(self, name, offset):
        '''
        Return a list of friend activity - GET /api/feed/<name>/<offset>

        This will return a friend feed with some rudimentary pagination. 
        The page-size limit is fixed at 2. To start from the beginning set offset = 0.
        If a task is associated with related actions, a list of related actions will also be returned.

        [POC] The POC assumes that the relevant data is always cached and available.
        In a production environment, should a cache 'miss' happen, the relational database 
        should be queried as a backup.
        '''
        if False is CacheManager.contains_key(feed_cache, name):
            return {"friend_feed": []}

        size_limit = 2
        new_offset = offset+size_limit

        next_url = 'http://127.0.0.1:5000/api/feed/{}/{}'.format(
            name, new_offset)

        '''Pull the user's friend feed from 'message feed' cache'''

        friend_feed = CacheManager.find_by_key(feed_cache, name)

        '''Pull from the 'related' cache and insert related actions into friend feed'''

        for task in friend_feed:
            related = CacheManager.find_by_key(related_cache, task['id'])
            if related:
                TaskModel.insert_related(task, related)

        feed_length = len(friend_feed)

        '''Provides rudimentary pagination given the small number of records'''

        if new_offset > feed_length-1:
            return {'my_feed': friend_feed[offset:]}
        return {'my_feed': friend_feed[offset: new_offset], 'next_url': next_url}
