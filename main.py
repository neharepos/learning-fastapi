from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

ls = []

class Post(BaseModel):
    name : str
    details : str
    age : int = 22
    rating : Optional[int]= None
    

@app.get('/')
def home():
    return {'name':'nishant'}

@app.get('/items/{itemname}')
def items(itemname):
    return {'item':itemname}

@app.post('/posts')
def post(post: Post):
    print(f"name : {post.name} \ndetails : {post.details} \nage: {post.age} \nrating : {post.rating}")
    post_dict = post.dict()
    ls.append(post_dict)
    print(ls)
    return{"data":post_dict}
