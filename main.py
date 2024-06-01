from fastapi import FastAPI 
app = FastAPI()

@app.get('/')
def home():
    return {'name':'nishant'}

@app.get('/items/{itemname}')
def items(itemname):
    return {'item':itemname}
