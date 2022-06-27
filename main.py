import json

from flask import Flask
import utils

app = Flask(__name__)


@app.get('/movie/<title>')
def get_by_title_view(title):
    result = utils.search_by_title(title)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get('/movie/<int:year1>/to/<int:year2>')
def search_by_release_year_view(year1, year2):
    result = utils.search_by_release_year(year1, year2)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get('/rating/<rating>')
def get_by_rating_view(rating):
    result = utils.get_by_rating(rating)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )

@app.get('/genre/<genre>')
def get_by_genre_view(genre):
    result = utils.get_by_genre(genre)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    app.run(debug=True)
