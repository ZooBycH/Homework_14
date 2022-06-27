import json
import sqlite3
from pprint import pprint as pp


def get_value_from_db(sql):
    """Функция извлекает данные из БД по запросу"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()
        return result


def search_by_title(title):
    """поиск в БД по названию фильма"""
    sql = f"""
    select title, country, release_year,listed_in as genre, description
    from netflix
    where title = '{title}'
    order by release_year DESC
    limit 1
    """
    result = get_value_from_db(sql)

    for item in result:
        return dict(item)


def search_by_release_year(year1, year2):
    """поиск в БД по диапазону лет выпуска"""
    sql = f"""
    SELECT title, release_year
    from netflix
    WHERE release_year BETWEEN {year1} and {year2}
    LIMIT 100
    """
    result = get_value_from_db(sql)

    response = [dict(item) for item in result]
    return response


def get_by_rating(rating):
    """Принимает  список допустимых рейтингов и возвращала данные """
    rating_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""
    SELECT title, rating, description
    FROM netflix
    WHERE rating in {rating_dict.get(rating)}
    """
    result = get_value_from_db(sql)
    response = [dict(item) for item in result]
    return response


def get_by_genre(genre):
    """Получает данные из БД по жанру"""

    sql = f"""
    SELECT title, description
    FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY listed_in DESC 
    LIMIT 10
    """
    result = get_value_from_db(sql)
    response = [dict(item) for item in result]
    return response


def get_double_actors(actor1, actor2):
    """
    получает в качестве аргумента имена двух актеров,
    возвращает список тех, кто играет с ними в паре больше 2 раз.
    """
    sql = f"""
        SELECT netflix.cast , COUNT(netflix.cast) 
        FROM netflix
        WHERE netflix.cast LIKE '%{actor1}%' AND netflix.cast LIKE '%{actor2}%' 
        GROUP BY  netflix.cast
        """
    result = []

    names_dict = {}
    for item in get_value_from_db(sql):
        names = set(dict(item).get('cast').split(", ")).difference({actor1, actor2})
        for name in names:
            names_dict[name] = names_dict.get(name, 0) + 1

    for key, value in names_dict.items():
        if value >= 2:
            result.append(key)

    return result


def get_title_for_tyl(movie_type, year, genre):
    """
    Принимает тип картины (фильм или сериал), год выпуска и ее жанр и
    получает на выходе список названий картин с их описаниями в JSON
    """

    sql = f"""
    SELECT title, description
    FROM netflix
    WHERE netflix.type = '{movie_type}'
    AND release_year = '{year}'
    AND listed_in LIKE '%{genre}%'
    """

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)
