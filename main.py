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


@app.put("/users/{user_id}")
async def update_user(user_id: int, request: Request):
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
    mycursor.execute(f"UPDATE users SET name='{name}', email='{email}' WHERE id={user_id}")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "User updated successfully"}, status_code=200)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"DELETE FROM users WHERE id={user_id}")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)


@app.get("/users/{user_id}/favourite_artists")
async def get_favourite_artists(user_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT artists.id, artists.name FROM user_fav_artists JOIN artists ON artists.id = user_fav_artists.artist_id WHERE user_fav_artists.user_id={user_id}")
    artists = mycursor.fetchall()
    mydb_conn.commit()
    mydb_conn.close()
    fav_artist = [{"name": artist[1]} for artist in artists]
    return JSONResponse(content={"favourite_artists": fav_artist}, status_code=200)

@app.get("/users/{user_id}/favourite_tracks")
async def get_favourite_tracks(user_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )   
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT tracks.id, tracks.name FROM user_fav_tracks JOIN tracks ON tracks.id = user_fav_tracks.track_id WHERE user_fav_tracks.user_id={user_id}")
    tracks = mycursor.fetchall()
    mydb_conn.commit()
    mydb_conn.close()
    fav_tracks = [{"name": track[1]} for track in tracks]
    return JSONResponse(content={"favourite_tracks": fav_tracks}, status_code=200)

@app.get("/users/{user_id}/favourite_genres")
async def get_favourite_genres(user_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()  
    mycursor.execute(f"SELECT genres.id, genres.name FROM user_fav_genres JOIN genres ON genres.id = user_fav_genres.genre_id WHERE user_fav_genres.user_id={user_id}")
    genres = mycursor.fetchall()
    mydb_conn.commit()
    mydb_conn.close()
    fav_genres = [{"name": genre[1]} for genre in genres]
    return JSONResponse(content={"favourite_genres": fav_genres}, status_code=200)