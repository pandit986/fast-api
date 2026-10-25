# import requests

# response = requests.get("https://jsonplaceholder.typicode.com/posts")

# data = response.json()
# print(data)

from fastapi import FastAPI, Request, HTTPException
import requests


app = FastAPI()

# get all data
@app.get("/posts")
async def get_posts():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# get data by id
@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int):
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))