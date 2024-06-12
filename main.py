from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randint

app = FastAPI()

ls = [{"name" : "Nishant", "details" : "Bad boy", "age" : 77, "rating" : 4, "id" : 1},
      {"name" : "Nisha", "details": "Good girl", "age" : 12, "rating" : 6, "id" : 2}]

def search(id):
    for i in ls:
        if i["id"] == id:
            return i

def index_loc(id):
    for i, p in enumerate(ls):
        if p["id"] == id:
            return i

class Post(BaseModel):
    name : str
    details : str
    age : int = 22
    rating : Optional[int]= None
    

@app.get('/')
def home():
    return {'name':'nishant'}

@app.get('/posts')
def get_post():
    return {"data" : ls}

@app.post('/posts')
def post(post: Post):
    print(f"name : {post.name} \ndetails : {post.details} \nage: {post.age} \nrating : {post.rating}")
    post_dict = post.dict()
    post_dict["id"] = randint(1,20000000000)
    ls.append(post_dict)
    print(ls)
    return{"data":post_dict}

@app.get('/posts/{id}')
def get_post_id(id : int):
    result = search(id)
    return {"data" : result}

@app.delete("/posts/{id}")
def delete_post(id : int):
    location = index_loc(id)
    print(location)
    ls.pop(location)
    return {"message" : "the data is deleted" }

@app.put("/posts/{id}")
def update_post(id : int,update_post : Post):
    loc = index_loc(id)
    upd_data = update_post.dict()
    upd_data["id"] = id
    ls[loc] = upd_data
    return {"data" : upd_data}





