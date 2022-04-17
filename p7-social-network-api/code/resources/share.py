from flask_restful import Resource, reqparse

from models.task import TaskModel
from models.related import RelatedModel
from cache import related_cache, CacheManager


class Share(Resource):

    '''
    This resource is accessed when a user shares
    a post with another user in the system.
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
        Create a new share - POST /api/task/share

        This will 1) insert a new 'share' action into the 'tasks' 
        table, 2) insert a corresponding record in the 'related'
        table and 3) update the cache for future lookups. 


        The request will fail if:
        - The verb used is not 'share'
        - The object being shared cannot be found in the system
        - The actor has already shared the object with the target

        '''
        data = Share.parser.parse_args()

        if 'share' != data['verb']:
            return {"message": "Incorrect verb '{}' should be 'share'".format(data['verb'])}, 400

        if None is TaskModel.find_by_object(data['object']):
            return{"message": "Object '{}' not found".format(data['object'])}, 400

        if TaskModel.is_shared_with_target(data['actor'], data['object'], data['target']):
            return{"message": "Object '{}' has already been shared with target '{}'".format(data['object'], data['target'])}, 400

        new_task = TaskModel(**data)
        _id = new_task.save_to_db()
        new_task.set_id(_id)

        '''
        [POC] In a production environment, the following operations will be added
        to a task queue and executed it in the background.

        Link the 'share' action to the original post and update the 'related' cache.
        '''

        '''Start of background task'''

        original_post_id = TaskModel.get_original_post_id(data['object'])
        new_related = RelatedModel(original_post_id, _id)
        new_related.save_to_db()

        CacheManager.save_to_cache(
            related_cache, original_post_id, new_task.json_with_id())

        '''End of background task'''

        return {"message": "Shared successfully"}, 201
