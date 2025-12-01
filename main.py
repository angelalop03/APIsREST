from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
import mysql.connector
from configuration.conections import DatabaseConnection
import os

API_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
API_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my Mini Spotify"}


@app.get("/users")
def get_users():
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root",
        password="root",
        database="apispotify"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    mydb.close()
    return {"users": users}


@app.post("/users")
async def create_user(request: Request): 
    mydb = DatabaseConnection(          
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )

    mydb_conn = await mydb.get_connection()
    request =  await request.json()  
    name = request['name']
    email = request['email']

    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)