from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'fastapi', user = 'postgres', password = 'daddy', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected")
        break
    except Exception as error:
        print("Unable to connect")
        print("Error:", error)
        time.sleep(4)

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
    title : str
    content : str
    published : bool = True
    

@app.get('/')
def home():
    return {'name':'nishant'}

@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}

@app.get('/posts/{id}')
def get_post_id(id : int, response : Response):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message' : f"{id} was not found"}
    return {"data" : post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int, post : Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s,published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"post with id: {id} does not exist")

    
    return {"data" : updated_post}





