from dotenv import load_dotenv

from service.spotify_service import get_spotify_data_directly
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


@app.get("/users/{user_id}/playlists")
async def get_user_playlists(user_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT id, name FROM playlists WHERE user_id={user_id}")
    playlists = mycursor.fetchall()
    mydb_conn.commit()
    mydb_conn.close()
    user_playlists = [{"name": playlist[1]} for playlist in playlists]
    return JSONResponse(content={"playlists": user_playlists}, status_code=200)

@app.post("/users/{user_id}/playlists")
async def create_user_playlist(user_id: int, request: Request):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    request =  await request.json() 
    name = request['name']
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO playlists (name, user_id) VALUES ('{name}', {user_id})")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "Playlist created successfully"}, status_code=201)

@app.delete("/users/{user_id}/playlists/{playlist_id}")
async def delete_user_playlist(user_id: int, playlist_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"DELETE FROM playlists WHERE id={playlist_id} AND user_id={user_id}")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "Playlist deleted successfully"}, status_code=200)

@app.put("/users/{user_id}/playlists/{playlist_id}")
async def update_user_playlist(user_id: int, playlist_id: int, request: Request):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    request =  await request.json()  
    name = request['name']
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"UPDATE playlists SET name='{name}' WHERE id={playlist_id} AND user_id={user_id}")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "Playlist updated successfully"}, status_code=200)

#Ver canciones de una `playlist`
@app.get("/users/{user_id}/playlists/{playlist_id}/tracks")
async def get_playlist_tracks(user_id: int, playlist_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT tracks.id, tracks.name FROM tracks JOIN playlist_tracks ON tracks.id = playlist_tracks.track_id WHERE playlist_tracks.playlist_id = {playlist_id}")
    tracks = mycursor.fetchall()
    mydb_conn.close()
    playlist_tracks = [{"name": track[1]} for track in tracks]
    return JSONResponse(content={"tracks": playlist_tracks}, status_code=200)


#Añadir una cancion a una `playlist`
@app.post("/users/{user_id}/playlists/{playlist_id}/tracks")
async def add_track_to_playlist(user_id: int, playlist_id: int, request: Request):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    request =  await request.json()  
    track_name = request['track_name']
    mycursor = mydb_conn.cursor(buffered=True)
    mycursor.execute(f"SELECT id FROM tracks WHERE name='{track_name}'")
    track = mycursor.fetchone()
    if track:
        track_id = track[0]
        mycursor.execute(f"INSERT INTO playlist_tracks (playlist_id, track_id) VALUES ({playlist_id}, {track_id})")
        mydb_conn.commit()
        mydb_conn.close()
        return JSONResponse(content={"message": "Track added to playlist successfully"}, status_code=201)
    else:
        mydb_conn.close()
        return JSONResponse(content={"message": "Track not found"}, status_code=404)
    

#Eliminar una cancion de una `playlist`
@app.delete("/users/{user_id}/playlists/{playlist_id}/tracks/{track_id}")
async def remove_track_from_playlist(user_id: int, playlist_id: int, track_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"DELETE FROM playlist_tracks WHERE playlist_id={playlist_id} AND track_id={track_id}")
    mydb_conn.commit()
    mydb_conn.close()
    return JSONResponse(content={"message": "Track removed from playlist successfully"}, status_code=200)


##API

@app.get("/artists/{artist_id}")
async def get_artist(artist_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT name FROM artists WHERE id={artist_id}")
    artist = mycursor.fetchone()
    artist = artist[0] if artist else ""
    mydb_conn.commit()
    mydb_conn.close()

    response = get_spotify_data_directly(artist, 'artist', API_CLIENT_ID, API_CLIENT_SECRET)
    return JSONResponse(content={"artist_data": response}, status_code=200)


@app.get("/tracks/{track_id}")
async def get_track(track_id: int):
    mydb = DatabaseConnection( 
        host="localhost",
        user="root",
        password="root",
        database="apispotify"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT name FROM tracks WHERE id={track_id}")
    track = mycursor.fetchone()
    track = track[0] if track else ""
    mydb_conn.commit()
    mydb_conn.close()

    response = get_spotify_data_directly(track, 'track', API_CLIENT_ID, API_CLIENT_SECRET)
    return JSONResponse(content={"track_data": response}, status_code=200)
