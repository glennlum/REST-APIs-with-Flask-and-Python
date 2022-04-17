from flask_restful import Resource, reqparse

from models.follow import FollowModel
from models.task import TaskModel


class Follow(Resource):

    '''
    The follow resource is accessed when a user follows 
    another user in the system.
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('follow',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self, name):
        '''
        Create a new follower - POST /api/follow/<name>

        This will insert a new follower-followee record in the 'follows' table
        and a new 'follow' action in the 'tasks' table.

        The request will fail if:
        - The follower already exists

        '''
        data = Follow.parser.parse_args()

        if FollowModel.find_row(name, data['follow']):
            return {"message": "'{}' is already following '{}'".format(name, data['follow'])}, 400

        new_follow = FollowModel(name, data['follow'])
        new_follow.save_to_db()

        new_task = TaskModel(name, 'follow', None, data['follow'])
        new_task.save_to_db()

        return {"message": "'{}' is now following '{}'".format(name, data['follow'])}, 201
