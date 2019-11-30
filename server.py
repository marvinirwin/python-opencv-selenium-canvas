# serve.py

from flask import Flask

# creates a Flask application, named app
app = Flask(__name__, static_folder="www")


# a route where we will display a welcome message via an HTML template
@app.route("/")
def default():
    return app.send_static_file('index.html')


@app.route("/www/")
def serve(path):
    print(path)
    return app.send_static_file(path)


# run the application
if __name__ == "__main__":
    app.run(debug=True)
