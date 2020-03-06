#!/home/rochet/Logiciels/anaconda3/bin/python3
import requests

url = 'https://api.ceptyconsultant.localhost'


# SANS LOGIN =======================================

# GET
# accéder aux données
r = requests.get(url + '/data/a', verify=False)
#print(r.json())
assert r.json() == {'message': 'token manquant'}


# DELETE
# Supprimer des données
params = {'article_id': '93ecdcd3-c570-4891-94ac-e4c7d449a7bc'}
r = requests.delete(url + '/data', params=params, verify=False)
#print(r.json())
assert r.json() == {'message': 'token manquant'}

# PUT
# ajouter des données
contrib = {
    "article_id": "93ecdcd3-c570-4891-94ac-e4c7d449a7bc",
    "contrib_data": "mlem-_sound_2-2019-09-03T193015.084Z-.wav",
    "contrib_name": "m\u025b\u0301le\u0304m",
    "contrib_path": "https://ntealan.net/soundcontrib/",
    "contrib_type": "sound",
    "dico_id": "yb_fr_3031",
    "last_update": "2019-09-03 19:32:51.447000",
    "ntealan": True,
    "public_id": "5e328321-e943-4ab5-b892-3d45ed4f94dd",
    "user_id": "b42e96a8-7b0b-8b45-ae69-7c2efd472e1d",
    "user_name": "Bergier",
    "validate": True
}
r = requests.put(url + '/data', json=contrib, verify=False)
#print(r.json())
assert r.json() == {'message': 'token manquant'}



# OBTENIR LE TOKEN ================================
# login et obtenir le token
r = requests.post(url + '/login', json={"username":"Thomas", "password":"Mikolov"}, verify=False)
assert "Token" in r.json()
token = r.json()["Token"]
headers = { 'x-access-tokens' : token }


# AVEC LOGIN =======================================

# GET
# accéder aux données
r = requests.get(url + '/data/a', headers=headers, verify=False)
assert 'data' in r.json()

# DELETE
# supprimer des données
params = {'article_id': '93ecdcd3-c570-4891-94ac-e4c7d449a7bc'}
headers = { 'x-access-tokens' : token }
r = requests.delete(url + '/data', headers=headers, params=params, verify=False)
#print(r.json())
assert r.json() == {'OK': 'Article supprimé avec succés'}


# PUT
# ajouter des données
contrib = {
    "article_id": "93ecdcd3-c570-4891-94ac-e4c7d449a7bc",
    "contrib_data": "mlem-_sound_2-2019-09-03T193015.084Z-.wav",
    "contrib_name": "m\u025b\u0301le\u0304m",
    "contrib_path": "https://ntealan.net/soundcontrib/",
    "contrib_type": "sound",
    "dico_id": "yb_fr_3031",
    "last_update": "2019-09-03 19:32:51.447000",
    "ntealan": True,
    "public_id": "5e328321-e943-4ab5-b892-3d45ed4f94dd",
    "user_id": "b42e96a8-7b0b-8b45-ae69-7c2efd472e1d",
    "user_name": "Bergier",
    "validate": True
}

headers = { 'x-access-tokens' : token }
r = requests.put(url + '/data', headers=headers, json=contrib, verify=False )
#print(r.json())
assert r.json() == {'OK': 'Article ajouté avec succès'}

print("--> test success !")