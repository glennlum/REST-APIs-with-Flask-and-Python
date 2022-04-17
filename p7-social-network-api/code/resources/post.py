from flask_restful import Resource, reqparse

from models.task import TaskModel
from models.follow import FollowModel
from cache import feed_cache, CacheManager


class Post(Resource):

    '''
    This resource is accessed when a user creates
    a new post in the system.
    '''

    parser = reqparse.RequestParser()
    parser.add_argument('actor',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('verb',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('object',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('target', type=str)
    # 'target' value is not required for a 'post'

    def post(self):
        '''
        Create a new post - POST /api/task/post

        This will 1) insert a new 'post' action into the 'tasks' 
        table and 2) Push the new post to the message feeds of 
        all the user's followers.

        The request will fail if:
        - The verb used is not 'post'

        '''
        data = Post.parser.parse_args()

        if 'post' != data['verb']:
            return {"message": "Incorrect verb '{}' should be 'post'".format(data['verb'])}, 400

        new_task = TaskModel(**data)
        _id = new_task.save_to_db()
        new_task.set_id(_id)

        '''
        [POC] In a production environment, the following operations will be added
        to a task queue and executed it in the background.

        Fan out and deliver the post to each follower's message feed.
        '''

        '''Start of background task'''

        followers = [row.get_follower()
                     for row in FollowModel.find_by_followee(data['actor'])]
        if followers:
            for follower in followers:
                CacheManager.save_to_cache(
                    feed_cache, follower, new_task.json_with_id())

        '''End of background task'''

        return {"message": "Post created successfully"}, 201
