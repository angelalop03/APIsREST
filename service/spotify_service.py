import requests 


def get_spotify_data_directly(name: str, type_: str, client_id: str, client_secret: str):
    
    token_resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=15
    )
    token_resp.raise_for_status()
    access_token = token_resp.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    search_resp = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params={"q": name, "type": type_, "limit": 1},
        timeout=15
    )
    search_resp.raise_for_status()
    return search_resp.json()

