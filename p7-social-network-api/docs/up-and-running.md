# Up and Running

## Running the App
```
docker pull nomadicfurrybeaver/poc-glenn && \
docker run -p 5000:5000 nomadicfurrybeaver/poc-glenn
```
The app will be running on http://localhost:5000

# Test-Driving the App
###  The following is a quick demonstration of the API
Checkout the POC's [Postman collection](https://go.postman.co/workspace/horangi-poc-glenn~9491e700-acc1-4827-8d83-a4acdcce5b22/collection/20308838-5fc61c6d-5cda-4c42-acc3-d7241a181b6f?action=share&creator=20308838]) for the full suite of API endpoints and API documentation. 

## Create Your First Post
Create a new post in the system  
```
POST /api/task/post
```
Request Body (JSON)
```json
{
  "actor":"ivan",
  "verb":"post",
  "object":"photo:1"
}
```
Response
```json
{
    "message": "Post created successfully"
}
```
## Add Followers
Follow other users in the system
```
POST /api/follow/eric
```
Request Body (JSON)
```json
{
  "follow": "ivan"
}
```
Response
```json
{
    "message": "'eric' is now following 'ivan'"
}
```

## Create Another Post
Posts can now be read by followers
```
POST /api/task/post
```
Request Body (JSON)
```json
{
  "actor":"ivan",
  "verb":"post",
  "object":"photo:2"
}
```
Response
```json
{
    "message": "Post created successfully"
}
```
## Like a Post
Followers can react to posts with `likes`
```
POST /api/task/like
```
Request Body (JSON)
```json
{
  "actor": "eric",
  "verb": "like",
  "object": "photo:2",
  "target": "ivan"
}
```
Response
```json
{
    "message": "Like added successfully"
}
```
  
## Share a Post
Followers can `share` posts
```
POST /api/task/share
```
Request Body (JSON)
```json
{
  "actor": "eric",
  "verb": "share",
  "object": "photo:2",
  "target": "niko"
}
```
Response
```json
{
    "message": "Shared successfully"
}
```
## View Eric's Friend Feed
Followers can view posts of their friends
```
GET /api/feed/eric/0
```
Response
```json
{
    "my_feed": [
        {
            "id": 3,
            "actor": "ivan",
            "verb": "post",
            "object": "photo:2",
            "target": null,
            "related": [
                {
                    "id": 4,
                    "actor": "eric",
                    "verb": "like",
                    "object": "photo:2",
                    "target": "ivan"
                },
                {
                    "id": 5,
                    "actor": "eric",
                    "verb": "share",
                    "object": "photo:2",
                    "target": "niko"
                }
            ]
        }
    ]
}
```

## View Ivan's Personal Feed
Users can view their own activity feed
```
GET /api/history/ivan/0
```
Response
```json
{
    "my_feed": [
        {
            "actor": "ivan",
            "verb": "post",
            "object": "photo:1",
            "target": null
        },
        {
            "actor": "ivan",
            "verb": "post",
            "object": "photo:2",
            "target": null
        }
    ]
}
```
