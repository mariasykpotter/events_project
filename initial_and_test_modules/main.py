from flask import Flask, render_template
from config import Configuration
from initial_and_test_modules.app import Map, factory

Map("red", 12).draw(factory())

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route("/")
def index():
    return render_template("map.html")


if __name__ == '__main__':
    app.run()
