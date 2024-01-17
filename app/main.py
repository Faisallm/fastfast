from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random

# entry to our api
app = FastAPI()

#default in-memory database
my_posts = [{"title": "top beaches in lasgidi", "content": "check out these awesome beaches", "id": 1},
{"title": "top beaches in laguna", "content": "check out these awesome AI", "id": 2}]


class Post(BaseModel):
    title: str
    content: str
    # if user does not provide publish, it will
    # default to true.
    published: bool = True

def find_post(id):
    for post in my_posts:
        if id == post['id']:
            return post

def find_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

# this is like the homepage
# function should be descriptive as possible
@app.get('/')
def root():
    return {"message": "Faisal Lawan Muhammad, Welcome to my api"}


# retrieving all of our posts
@app.get('/posts')
def get_posts():
    return {'data': my_posts}

# post request send data to the api server
# when changing status codes we can provide a 
# status_code in the decorator.
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    id = random.randrange(1, 10000000)
    # creating a new id and adding to dictionary
    post['id'] = id
    # add post to in-memory database
    my_posts.append(post)
    print(my_posts)
    return {"data": post}

# the way to go when changing the http response status
# is to raise HTTPExceptions, seems much cleaner.
@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        # changing the status code of the http request
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with ID: {id}, was not found.'}
        # another cleaner way of doing it is to use HTTPException
        # we raise exceptions
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
    return {'post_detail': f"Here is the post id: {id}, post: {post}"}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # get index in the array that have the post
    
    index = find_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with index does not exist.')

    # deleting the post
    my_posts.pop(index)

    # deleting 204 should not send anything back
    # it should return a 204 response status code
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# even when updating posts, it should...
# respect our schema.
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail='post with index does not exist.')

    post_dict = post.dict()
    post_dict['id'] = id
    # update the post
    my_posts[index] = post_dict

    return {"data": post_dict}
