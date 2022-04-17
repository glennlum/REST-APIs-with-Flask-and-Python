from flask_restful import Resource, reqparse

from models.follow import FollowModel
from models.task import TaskModel


class Unfollow(Resource):

    '''
    This resource is accessed when a user unfollows
    another user in the system.
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('unfollow',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def delete(self, name):
        '''
        Unfollow a user - DEL /api/unfollow/<name>

        This will remove a follower-followee record from the 'follows' table
        and insert a new 'unfollow' action in the 'tasks' table.

        The request will fail if:
        - The record is not found
        - The user is not a follower

        '''
        data = Unfollow.parser.parse_args()

        if None is FollowModel.find_row(name, data['unfollow']):
            return {"message": "'{}' is not a follower of '{}'".format(name, data['unfollow'])}, 400

        follow = FollowModel.find_row(name, data['unfollow'])
        follow.delete_from_db()

        new_task = TaskModel(name, 'unfollow', None, data['unfollow'])
        new_task.save_to_db()

        return {"message": "'{}' unfollowed '{}'".format(name, data['unfollow'])}, 201
