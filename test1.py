
import flask
from flask import request
app = flask.Flask(__name__)
data = {}


@app.route("/api/post-user/", method=['GET', "POST"])
def PostUser(user):
    if request.method == 'POST':
        data = {"USER": user}
    return data


@app.route("/api/<int:user_id>", method=['GET', "POST"])
def GetDetails(user_id):
    if request.method == 'GET':
        return data[user_id]


if __name__ == '__main__':
    app.run(debug=True)
