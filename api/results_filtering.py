import requests
import os
import urllib.parse


# Ensure the search results contains only the specified filter
def process_search(args_dict, recipeJSON):
    result = []

    result.append(
        all(diet in recipeJSON["recipe"]["dietLabels"] for diet in args_dict["diet"])
    )
    result.append(
        all(
            health in recipeJSON["recipe"]["healthLabels"]
            for health in args_dict["health"]
        )
    )
    result.append(
        all(
            cuisine in recipeJSON["recipe"]["cuisineType"]
            for cuisine in args_dict["cuisine"]
        )
    )
    result.append(
        all(dish in recipeJSON["recipe"]["dishType"] for dish in args_dict["dish"])
    )

    return all(result)


def get_response_recipe(args_dict):
    edamam_api = (
        "https://api.edamam.com/api/recipes/v2?type=public&app_id="
        + os.getenv("EDAMAM_APP_ID")
        + "&app_key="
        + os.getenv("EDAMAM_APP_KEY")
    )

    if args_dict["dishname"] != "":
        edamam_api += "&q=" + urllib.parse.quote(args_dict["dishname"], safe="")

    for diet in args_dict["diet"]:
        edamam_api += "&diet=" + str.lower(diet)

    for health in args_dict["health"]:
        edamam_api += "&health=" + str.lower(health)

    for cuisine in args_dict["cuisine"]:
        edamam_api += "&cuisineType=" + urllib.parse.quote(cuisine)

    for dish in args_dict["dish"]:
        edamam_api += "&dishType=" + urllib.parse.quote(dish)

    return requests.get(edamam_api)


def get_response_uri(uri_list):
    edamam_api = (
        "https://api.edamam.com/api/recipes/v2/by-uri?type=public&app_id="
        + os.getenv("EDAMAM_APP_ID")
        + "&app_key="
        + os.getenv("EDAMAM_APP_KEY")
    )

    for uri in uri_list:
        edamam_api += "&uri=" + urllib.parse.quote(uri, safe="")

    return requests.get(edamam_api)
