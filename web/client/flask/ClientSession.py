from flask import Flask, render_template_string, request, redirect, url_for

from movielist.common.Movie import Movie, MovieEntry, MovieEntryData
from movielist.server.MovieCacheManager import MovieCacheManager

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Cache Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h1, h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { background: #f4f4f4; margin: 8px 0; padding: 10px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        form.inline { display: inline; }
        input[type="text"] { padding: 8px; width: 70%; margin-right: 10px; }
        button { padding: 8px 12px; cursor: pointer; border: none; border-radius: 4px; }
        .btn-add { background-color: #28a745; color: white; }
        .btn-delete { background-color: #dc3545; color: white; }
    </style>
</head>
<body>
    <h1>Movie Cache</h1>
    
    <h2>Add New Movie</h2>
    <form action="/add" method="POST">
        <input type="text" name="title" placeholder="Enter movie title..." required>
        <button type="submit" class="btn-add">Add Movie</button>
    </form>

    <h2>Current Movies</h2>
    <ul>
        {% for movie in movies %}
        <li>
            <span>{{ movie.get_name() }}</span>
            <form action="/remove" method="POST" class="inline">
                <input type="hidden" name="title" value="{{ movie.get_name() }}">
                <button type="submit" class="btn-delete">Remove</button>
            </form>
        </li>
        {% else %}
        <li>No movies in cache.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

class MovieServer:
    def __init__(self, cache_manager: MovieCacheManager, host="127.0.0.1", port=5000, debug=True):
        self.cache_manager: MovieCacheManager = cache_manager
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            movies = self.cache_manager.get_movies()
            return render_template_string(INDEX_TEMPLATE, movies=movies)

        @self.app.route("/add", methods=["POST"])
        def add_movie():
            title = request.form.get("title", "").strip()
            if title:
                self.cache_manager.add_entry(MovieEntry(MovieEntryData(Movie(title), "Xavi")))
            return redirect(url_for("index"))

        @self.app.route("/remove", methods=["POST"])
        def remove_movie():
            title = request.form.get("title", "").strip()
            if title:
                self.cache_manager.remove_entry_by_name(title)
            return redirect(url_for("index"))

    def run(self):
        """Starts the Flask development server."""
        self.app.run(host=self.host, port=self.port, debug=self.debug)


# Example usage
if __name__ == "__main__":
    # Instantiate your existing movie cache manager
    cache = MovieCacheManager()

    # Pass the manager instance into the server class and run
    server = MovieServer(cache_manager=cache)
    server.run()