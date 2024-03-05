from dotenv import load_dotenv
import os
import requests
import json
from api.results_filtering import process_search

load_dotenv()

def test_edamam_id_and_key_are_valid():
    edamam_api = (
        "https://api.edamam.com/api/recipes/v2?type=public&app_id="
        + os.getenv("EDAMAM_APP_ID")
        + "&app_key="
        + os.getenv("EDAMAM_APP_KEY")
    )

    response = requests.get(edamam_api)

    assert response.status_code == 200


def test_process_search_return_correct_boolean_list_1():
    test_args = {"dishname": "", "diet": ["high-protein", "low-carb"], "health": ["dairy-free", "gluten-free"], "cuisine": ["asian", "british"], "dish": ["main course"]}

    # recipes = json.load(open("test/recipe_test.json"))
    recipes = json.load(open("test/recipe_test.json"))

    results = []
    for recipe in recipes["hits"]:
        results.append(process_search(test_args, recipe))

    assert results == [False, False, False]


def test_process_search_return_correct_boolean_list_1():
    test_args = {"dishname": "", "diet": ["High-Protein", "Low-Carb"], "health": ["Dairy-Free", "Gluten-Free"], "cuisine": ["asian", "british"], "dish": ["main course"]}

    recipes = json.load(open("test/recipe_test.json"))

    results = []
    for recipe in recipes["hits"]:
        results.append(process_search(test_args, recipe))

    assert results == [False, False, False]


def test_process_search_return_correct_boolean_list_2():
    test_args = {"dishname": "", "diet": ["Low-Carb"], "health": ["Gluten-Free"], "cuisine": [], "dish": []}

    recipes = json.load(open("test/recipe_test.json"))

    results = []
    for recipe in recipes["hits"]:
        results.append(process_search(test_args, recipe))

    # Third recipe is not gluten-free
    assert results == [True, True, False]


def test_process_search_return_correct_boolean_list_3():
    test_args = {"dishname": "", "diet": [], "health": [], "cuisine": ["asian"], "dish": ["main course"]}

    recipes = json.load(open("test/recipe_test.json"))

    results = []
    for recipe in recipes["hits"]:
        results.append(process_search(test_args, recipe))

    # First and second recipe are not asian cuisine
    assert results == [False, False, True]