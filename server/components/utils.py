import json
import os
import requests
from dotenv import load_dotenv
from components.models import response


class obj:
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def dict_to_obj(d):
    return json.loads(json.dumps(d), object_hook=obj)


headers = {
        'acccept': 'application/json',
        'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
    }


load_dotenv()


def title_fetch(title: str):

    title = title.replace("+", "%20")

    url = os.getenv('URL')+ f'/search/movie?'

    query_string = {
        "query": title,
        "language": "en-US",
        "include_adult": "true",
        "page": "1",
    }

    response = requests.request("GET", url, headers=headers, params=query_string)

    data = dict_to_obj(json.loads(response.text))
    list_data = []
    response_data = {}

    if len(data.results) == 0:
        raise Exception("No data found")

    i = 0

    for x in data.results:
        if(x.title == None or x.release_date == None or x.poster_path == None):
            continue
        else:
            list_data.append({
                "id": x.id,
                "title": x.title[0:50],
                "genre_names": get_genres(x.genre_ids),
                "release_date": x.release_date[0:4],
                "overview": x.overview,
                "poster_path": x.poster_path,
                "vote_average": x.vote_average
            })
            i+=1

        if i == 4:
            break

    response_data["data"] = sort_by_vote_average(list_data)
    return response_data



def get_casts_by_id(id: int):
    url = f"{os.getenv('URL')}/movie/{id}/credits"

    query_string = {
        "language": "en"
    }
    
    response = requests.request("GET", url, headers=headers, params=query_string)

    data = dict_to_obj(json.loads(response.text))
    casts = []

    for x in data.cast:
        temp = {
            "name": x.name,
            "character": x.character,
            "cast_id": x.id,
            "popularity": x.popularity,
        }
        casts.append(temp)

    casts = sorted(casts, key=lambda x: x['popularity'], reverse=True)
    casts = casts[0:4]
    return casts



def get_genres(genres: list):
    genre_list = []

    for x in genres:
        genre_list.append(str(x))

    return genre_list



def sort_by_vote_average(data: list):
    return sorted(data, key=lambda x: x['vote_average'], reverse=True)



def common_genres(data: list[response]):
    commons = {}
    for x in data:
        for y in x.genre_names:
            if y in commons:
                commons[y] += 1
            else:
                commons[y] = 1

    return sorted(commons, key=lambda x: x[1], reverse=False)



def common_casts(data: list[response]):
    commons = {}
    for x in data:
        temp = get_casts_by_id(x.id)
        for y in temp:
            if y['cast_id'] in commons:
                commons[y['cast_id']] += 1
            else:
                commons[y['cast_id']] = 1

    key, values = zip(*(dict(sorted(commons.items(), key=lambda x: x[1], reverse=True))).items())
    return key[0:4]



def recommend(data: list):
    genres = common_genres(data)
    casts = common_casts(data)
    ids = [x.id for x in data]
    casts = [str(x) for x in casts]

    url = os.getenv('URL') + '/discover/movie?'


    genre_or = " | ".join(genres)
    casts_or = " | ".join(casts)

    query_string_1 = {
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
        "sort_by": "vote_average.desc",
        "vote_count.gte": "10000",
        "with_cast": casts_or,
    }

    query_string_2 = {
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
        "sort_by": "vote_average.desc",
        "vote_count.gte": "10000",
        "with_genres": genre_or,
    }

    query_string_3 = {
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
        "sort_by": "vote_average.desc",
        "vote_count.gte": "10000",
        "with_genres": genre_or,
        "with_cast": casts_or,
    }

    list_data = []
    list_ids = []

    response_1 = dict_to_obj(details_by_query_string(query_string_1))
    response_2 = dict_to_obj(details_by_query_string(query_string_2))
    response_3 = dict_to_obj(details_by_query_string(query_string_3))

    x: response
    if response_1 != None:
        for x in response_1.data:
            if x.id not in ids:
                list_data.append(x)
                list_ids.append(x.id)

    if response_2 != None:
        for x in response_2.data:
            if x.id not in ids and x.id not in list_ids:
                list_data.append(x)
                list_ids.append(x.id)

    if response_3 != None:
        for x in response_3.data:
            if x.id not in ids and x.id not in list_ids:
                list_data.append(x)

    return {
        "status": "success",
        "data": list_data
    }
    
    

    
    


    

def details_by_query_string(query_string: dict):
    url = os.getenv('URL') + '/discover/movie?'

    response = dict_to_obj(json.loads(requests.request("GET", url, headers=headers, params=query_string).text))

    list_data = []
    response_data = {}

    if len(response.results) == 0:
        return None

    i = 0

    for x in response.results:
        if(x.title == None or x.release_date == None or x.poster_path == None):
            continue
        else:
            list_data.append({
                "id": x.id,
                "title": x.title[0:50],
                "genre_names": get_genres(x.genre_ids),
                "release_date": x.release_date[0:4],
                "overview": x.overview,
                "poster_path": x.poster_path,
                "vote_average": x.vote_average
            })
            i+=1

        if i == 15:
            break

    response_data['data'] = list_data
    return response_data



# print(recommend(
#     [
#     {
#       "id": 1726,
#       "title": "Iron Man",
#       "genre_names": [
#         "28",
#         "878",
#         "12"
#       ],
#       "release_date": "2008",
#       "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
#       "poster_path": "/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
#       "vote_average": 7.646
#     },
#     {
#       "id": 68721,
#       "title": "Iron Man 3",
#       "genre_names": [
#         "28",
#         "12",
#         "878"
#       ],
#       "release_date": "2013",
#       "overview": "When Tony Stark's world is torn apart by a formidable terrorist called the Mandarin, he starts an odyssey of rebuilding and retribution.",
#       "poster_path": "/qhPtAc1TKbMPqNvcdXSOn9Bn7hZ.jpg",
#       "vote_average": 6.93
#     },
#     {
#       "id": 10138,
#       "title": "Iron Man 2",
#       "genre_names": [
#         "12",
#         "28",
#         "878"
#       ],
#       "release_date": "2010",
#       "overview": "With the world now aware of his dual life as the armored superhero Iron Man, billionaire inventor Tony Stark faces pressure from the government, the press and the public to share his technology with the military. Unwilling to let go of his invention, Stark, with Pepper Potts and James 'Rhodey' Rhodes at his side, must forge new alliances – and confront powerful enemies.",
#       "poster_path": "/6WBeq4fCfn7AN0o21W9qNcRF2l9.jpg",
#       "vote_average": 6.843
#     },
#     {
#       "id": 169934,
#       "title": "Iron Man: Rise of Technovore",
#       "genre_names": [
#         "878",
#         "16",
#         "28"
#       ],
#       "release_date": "2013",
#       "overview": "Iron Man enlists the help of ruthless vigilante the Punisher to track down War Machine's murderer. All the while, he's being pursued by S.H.I.E.L.D. agents Black Widow and Hawkeye, who suspect his involvement in a recent terrorist plot.",
#       "poster_path": "/eHDez1uN5X2ZAq4niX7HvhyZIIO.jpg",
#       "vote_average": 6.1
#     }
#   ]
# ))



    


