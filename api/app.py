from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functions.results_filtering import get_response_recipe, process_search, get_response_uri
from functions.database_functions import fetch_user_favorites

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    # Retrieve the JSON data from the client side
    args_dict = request.get_json()

    # For Testing (Will be replaced with Requests)
    # with open(join("../samplejson", "recipe.json"), "r") as read_file:
    #     data = json.load(read_file)

    # For Production
    response = get_response_recipe(args_dict)
    if response.status_code == 200:
        data = response.json()

        result_args = {
            "count": 0,
            "uri": [],
            "image": [],
            "name": [],
            "calories": [],
            "protein": [],
            "ingredient": [],
            "recipeURL": [],
        }

        for recipe in data["hits"]:
            if process_search(args_dict, recipe):
                result_args["uri"].append(recipe["recipe"]["uri"])
                result_args["image"].append(recipe["recipe"]["image"])
                result_args["name"].append(recipe["recipe"]["label"])
                result_args["calories"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"],
                        ndigits=3,
                    )
                )
                result_args["protein"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"],
                        ndigits=3,
                    )
                )
                result_args["ingredient"].append(recipe["recipe"]["ingredientLines"])
                result_args["recipeURL"].append(recipe["recipe"]["url"])
                result_args["count"] += 1
    else:
        return jsonify({"error": "API Service Unavailable"}), 503

    # Favorite list check, if user has logged in, and the dish is already in list, heart remains red
    # favorites = []
    # if current_user.is_authenticated is True:
    #     for dish in return_data("Favorites", current_user.email):
    #         favorites.append(dish["dish_uri"])

    return jsonify(result_args)

@app.route("/favourites", methods=["POST"])
def favourites():
    user_email = request.form["user"]
    favorites_uri = fetch_user_favorites(user_email)

    response = get_response_uri(favorites_uri)
    if response.status_code == 200:
        data = response.json()

        favorites_list = []
        for recipe in data["hits"]:
            favorites = {}
            favorites["uri"] = recipe["recipe"]["uri"]
            favorites["image"] = recipe["recipe"]["image"]
            favorites["name"] = recipe["recipe"]["label"]
            favorites["calories"] = round(recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"], ndigits=3)
            favorites["protein"] = round(recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"], ndigits=3)
            favorites["ingredient"] = recipe["recipe"]["ingredientLines"]
            favorites["recipeURL"] = recipe["recipe"]["url"]
            favorites_list.append(favorites)
    
        return jsonify(favorites_list)
    return jsonify({"error": "API Service Unavailable"}), 503
