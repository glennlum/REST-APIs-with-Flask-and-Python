from flask_restful import Resource

from models.task import TaskModel


class History(Resource):

    def get(self, name, offset):
        '''
        Return a list of user activity - GET /api/history/<name>/<offset>

        This will return a list of tasks performed by a user with some 
        rudimentary pagination. The page-size limit is fixed at 2.
        To start from the beginning set offset = 0.
        '''
        size_limit = 2
        new_offset = offset+size_limit

        next_url = 'http://127.0.0.1:5000/api/history/{}/{}'.format(
            name, new_offset)
        
        '''
        [POC] In a production environment, the following records should be 
        fetched with the ROWNUM and LIMIT sql statements to reduce latency.
        '''

        my_feed = [task.json() for task in TaskModel.find_by_actor(name)]
        feed_length = len(my_feed)

        '''Provides rudimentary pagination given the small number of records'''

        if new_offset > feed_length-1:
            return {'my_feed': my_feed[offset:]}
        return {'my_feed': my_feed[offset: new_offset], 'next_url': next_url}
