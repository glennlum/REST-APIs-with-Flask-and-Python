from flask_restful import Resource, reqparse

from models.task import TaskModel
from models.related import RelatedModel
from cache import related_cache, CacheManager


class Like(Resource):

    '''
    This resource is accessed when a user likes
    a post of another user in the system.
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
    parser.add_argument('target',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        '''
        Create a new like - POST /api/task/like

        This will 1) insert a new 'like' action into the 'tasks' 
        table, 2) insert a corresponding record in the 'related'
        table and 3) update the cache for future lookups. 

        The request will fail if:
            -The verb used is not like
            -The object being liked cannot be found in the system
            -The target is not the author of the post
            -The object is already liked by the actor
        '''
        data = Like.parser.parse_args()

        if 'like' != data['verb']:
            return {"message": "Incorrect verb '{}' should be 'like'".format(data['verb'])}, 400

        if None is TaskModel.find_by_object(data['object']):
            return{"message": "Object '{}' not found".format(data['object'])}, 400

        if None is TaskModel.find_original_poster(data['target'], data['object']):
            return{"message": "Target '{}' is not the author of '{}'".format(data['target'], data['object'])}, 400

        if TaskModel.is_liked_by_actor(data['actor'], data['object']):
            return{"message": "Object '{}' has already been liked by '{}'".format(data['object'], data['actor'])}, 400

        new_task = TaskModel(**data)
        _id = new_task.save_to_db()
        new_task.set_id(_id)

        '''
        [POC] In a production environment, the following operations will be added 
        to a task queue and executed it in the background.

        Link the 'like' action to the original post and update the 'related' cache.
        '''

        '''Start of background task '''

        original_post_id = TaskModel.get_original_post_id(data['object'])
        new_related = RelatedModel(original_post_id, _id)
        new_related.save_to_db()

        CacheManager.save_to_cache(
            related_cache, original_post_id, new_task.json_with_id())

        '''End of background task '''

        return {"message": "Like added successfully"}, 201
