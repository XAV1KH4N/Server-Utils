from flask import Flask

from movielist.client.flask.MovieWebClient import MovieWebClient

app = Flask(__name__)

MovieWebClient.register(app,route_base = '/')

if __name__ == '__main__':
    app.run(debug=False) 
