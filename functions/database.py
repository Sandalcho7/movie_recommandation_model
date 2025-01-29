from pymongo import MongoClient


def get_collections_from_db(
    host="localhost",
    port=27017,
    db_name="Movielens",
    users_col_name="Users",
    movies_col_name="Movies",
):
    """
    Connect to your MongoDB and returns list of documents for your collections

    Args:
    -----
    host (str): host adress of your MongoDB (default: 'localhost'),
    port (int): port of your MongoDB (default: 27017),
    db_name (str): name of your MongoDB (default: 'Movielens'),
    users_col_name (str): name of your users collection (default: 'users'),
    movies_col_name (str): name of your movies collection (default: 'movies')

    Returns:
    --------
    - users: list of documents in users collection
    - movies: list of documents in movies collection
    """
    client = MongoClient(host, port)
    db = client[db_name]

    users = db[users_col_name].find()
    movies = db[movies_col_name].find()

    return users, movies
