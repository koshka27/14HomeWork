from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)
# def main():
    # app = Flask(__name__)
    # app.config['JSON_AS_ASCII'] = False
    # app.config['DEBUG'] = True


def db_connect(query):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


@app.route('/movie/<title>')
def search_by_title(title):
    query = ("SELECT title, country, release_year, listed_in AS genre, description "
             "FROM netflix "
             f"WHERE title = '{title}' "
             "ORDER BY release_year DESC "
             "LIMIT 1 ")
    response = db_connect(query)[0]
    response_json = {
        'title': response[0],
        'country': response[1],
        'release_year': response[2],
        'genre': response[3],
        'description': response[4],
    }
    return jsonify(response_json)


@app.route('/movie/<int:start>/to/<int:end>')
def search_by_period(start, end):
    query = ("SELECT title, release_year "
             "FROM netflix "
             f"WHERE release_year BETWEEN {start} AND {end} "
             "ORDER BY release_year "
             "LIMIT 100 ")
    response = db_connect(query)
    response_json = []
    for movie in response:
        response_json.append({
            'title': movie[0],
            'release_year': movie[1],
        })
    return jsonify(response_json)


@app.route('/rating/<group>')
def search_by_rating(group):
    levels = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    if group in levels:
        level = '\", \"'.join(levels[group])
        level = f'\"{level}\"'
    else:
        return jsonify([])

    query = ("SELECT title, rating, description "
             "FROM netflix "
             f"WHERE rating IN ({level}) ")
    response = db_connect(query)
    response_json = []
    for movie in response:
        response_json.append({
            'title': movie[0],
            'rating': movie[1],
            'description': movie[2].strip(),
        })
        return jsonify(response_json)


@app.route('/genre/<genre>')
def search_by_genre(genre):
    query = ("SELECT title, description "
             "FROM netflix "
             f"WHERE listed_in LIKE '%{genre}%' "
             "ORDER BY release_year "
             "LIMIT 10 ")
    response = db_connect(query)
    response_json = []
    for movie in response:
        response_json.append({
            'title': movie[0],
            'description': movie[1],
        })
    return jsonify(response_json)


def get_actors(name1='Rose McIver', name2='BEN Lamb'):
    query = ("SELECT 'cast' "
             "FROM netflix "
             f"WHERE 'cast' LIKE '%{name1}%' "
             f"AND 'cast' LIKE '%{name2}%' ")
    response = db_connect(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    result = []
    for a in actors:
        if a not in [name1, name2]:
            if actors.count(a) > 2:
                result.append(a)  # чтобы избежать дублирования
        result = set(result)
        print(result)


def get_movies(type_movie='Movie', release_year=2016, genre='Dramas'):
    query = ("SELECT title, description, 'type' FROM netflix "
             f"WHERE 'type' = '{type_movie}'"
             f"AND release_year = {release_year} "
             f"AND listed_in LIKE '%{genre}%' ")
    response = db_connect(query)
    response_json = []
    for movie in response:
        response_json.append({
            'title': movie[0],
            'description': movie[1],
            'type': movie[2],
        })
    return response_json


print(get_movies())  # (type_movie='Movie', release_year=2016, genre='Dramas')

if __name__ == '__main__':
    app.run()

# main()
