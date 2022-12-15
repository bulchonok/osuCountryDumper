import json, sys

import requests

client_id = input("Enter client ID:")
client_secret = input("Enter client secret:")
countrySymb = input("Enter country Symbol(example:US,EN...):")
API_url = "https://osu.ppy.sh/api/v2"
TOKEN_url = "https://osu.ppy.sh/oauth/token"


def get_token():
    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "public"
    }
    return requests.post(TOKEN_url, data=body).json().get("access_token")


TOKEN = get_token()
print(TOKEN)


def get_users():
    USERS_url = "https://osu.ppy.sh/api/v2/rankings/osu/performance"

    params = {"country": countrySymb.upper(), }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    return requests.get(USERS_url, headers=headers, params=params).json().get("ranking")


result = get_users()

# print(json.dumps(result,indent=1))
users_list = list()

for i in range(0, len(result)):
    users_list.append(result[i]["user"]["id"])


def get_best_scores(id):
    BEST_SCORES_URL = API_url+ f"/users/{id}/scores/best"
    params = {"limit":100}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    return requests.get(BEST_SCORES_URL,headers=headers,params=params).json()

for i in users_list:
    f = open(f"user{i}.txt", "w+")
    f.write(json.dumps(get_best_scores(i),indent=1))
    f.close()
