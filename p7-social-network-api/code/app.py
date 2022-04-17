import os
from flask import Flask
from flask_restful import Api

from database import db
from resources.post import Post
from resources.like import Like
from resources.share import Share
from resources.follow import Follow
from resources.unfollow import Unfollow
from resources.history import History
from resources.feed import Feed

app = Flask(__name__)

'''
[POC] Stand-in for an enterprise RDBMS
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
# This requires extra memory and should be disabled if not needed

api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(Post, '/api/task/post')
api.add_resource(Like, '/api/task/like')
api.add_resource(Share, '/api/task/share')
api.add_resource(Follow, '/api/follow/<string:name>')
api.add_resource(Unfollow, '/api/unfollow/<string:name>')
api.add_resource(History, '/api/history/<string:name>/<int:offset>')
api.add_resource(Feed, '/api/feed/<string:name>/<int:offset>')

if __name__ == '__main__':
    db.init_app(app)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

'''
Postman collection:
https://go.postman.co/workspace/horangi-poc-glenn~9491e700-acc1-4827-8d83-a4acdcce5b22/collection/20308838-5fc61c6d-5cda-4c42-acc3-d7241a181b6f?action=share&creator=20308838
'''
