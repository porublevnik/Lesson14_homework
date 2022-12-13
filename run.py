from flask import Flask, jsonify
from utils import get_one, get_result, search_by_cast

app = Flask(__name__)

@app.get('/movie/<title>')
def get_by_title(title):
    query = f"""SELECT *
                FROM netflix 
                WHERE title = '{title}'
                ORDER BY release_year
                """

    query_result = get_one(query)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'description': query_result['description']
    }

    if query_result is None:
        return jsonify(status=404)
    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1, year2):
    query = f"""SELECT * 
    FROM netflix 
    WHERE release_year BETWEEN {year1} and {year2}
    LIMIT 100
    """

    result = []
    for item in get_result(query):
        result.append(
            {
                'title': item['title'],
                'release_year': item['release_year']
            }
        )

    return jsonify(result)


@app.get('/movie/rating/<rating>')
def get_movie_by_rating(rating):
    query = f"""
    SELECT * FROM netflix 
    """

    if rating == 'children':
        query += 'WHERE rating = "G"'
    elif rating == 'family':
        query += 'WHERE rating = "G" OR rating = "PG" OR rating = "PG-13"'
    elif rating == 'adult':
        query += 'WHERE rating = "R" OR rating = "NC-17"'
    else:
        return jsonify(status=404)

    result = []
    for item in get_result(query):
        result.append(
            {
                'title': item['title'],
                'rating': item['rating']
            }
        )

    return jsonify(result)


@app.get('/genre/<genre>')
def get_movie_by_genre(genre: str):
    query = f"""SELECT * FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added DESC
    LIMIT 10
    """

    result = []
    for item in get_result(query):
        result.append(
            {
                'title': item['title'],
                'rating': item['rating'],
                'description': item['description']
            }
        )
    if result == []:
        return jsonify(status=404)
    else:
        return jsonify(result)


@app.get('/actors/<name1>/<name2>')
def get_co_actors(name1: str, name2: str):
    query = f"""
    SELECT * FROM netflix
    WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
    """

    result = get_result(query)
    actors_list = search_by_cast(result, name1, name2)

    return jsonify(actors_list)


@app.get('/<film_type>/<int:year>/<genre>/')
def get_movie_by_type_year_and_genre(film_type, year, genre):
    query = f"""SELECT * 
    FROM netflix 
    WHERE `type` IS '{film_type}' AND release_year is {year} and listed_in LIKE '%{genre}%'
    """

    result = []
    for item in get_result(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
                'type': item['type'],
                'release_year': item['release_year'],
                'genre': item['listed_in'],
            }
        )

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)