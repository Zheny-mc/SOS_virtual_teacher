import json
from flask import Flask, request, Response
from AdapterBD.connectDB import DataBase

app = Flask(__name__)
db = DataBase(url="mongodb://localhost:27017")

@app.route("/get_question", methods=["POST"])
def get_question():
    id = request.get_json()
    question = db.get_question(id)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')

@app.route("/create_question", methods=["POST"])
def create_question():
    question = request.get_json()
    db.create_question(question)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')


@app.route("/delete_question", methods=["POST", "DELETE"])
def delete_question():
    id_question = request.get_json()
    question = db.delete_question(id_question)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')

@app.route("/count_question", methods=["POST"])
def get_count_question():
    count = {"count": db.get_count_question()}
    return Response(response=json.dumps(count),
                    status=200,
                    mimetype='application/json')
# ---------------------- user ------------------------
@app.route("/get_user", methods=["POST"])
def get_user():
    chat_id = request.get_json()
    user = db.get_user(chat_id)
    del user["_id"]
    return Response(response=json.dumps(user),
                    status=200,
                    mimetype='application/json')


@app.route("/get_all_user", methods=["POST"])
def get_all_user():
    # chat_id = request.get_json()

    lst_user = [i for i in db.get_all_user()]
    for user in lst_user:
        del user["_id"]
    return Response(response=json.dumps(lst_user),
                    status=200,
                    mimetype='application/json')

@app.route("/update_user", methods=["POST"])
def update_user():
    new_user = request.get_json()
    id = new_user['chat_id']
    db.set_user(id, new_user)
    user = db.get_user(id)
    del user['_id']
    return Response(response=json.dumps(user),
                    status=200,
                    mimetype='application/json')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
