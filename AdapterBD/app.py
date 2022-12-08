import json
from flask import Flask, request, Response
from AdapterBD.connectDB import DataBase

from flasgger import Swagger
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder

from AdapterBD.swagger_conf.swagger import swagger_config

app = Flask(__name__)
db = DataBase(url="mongodb://localhost:27017")

# --------------------- swagger --------------------------
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)

# --------------------- Controllers --------------------------
@app.route("/get_question", methods=["POST"])
@swag_from("./swagger_conf/swagger_get_question.yml")
def get_question():
    id = request.get_json()
    question = db.get_question(id)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')

@app.route("/create_question", methods=["POST"])
@swag_from("./swagger_conf/swagger_create_question.yml")
def create_question():
    question = request.get_json()
    db.create_question(question)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')


@app.route("/delete_question", methods=["POST"])
@swag_from("./swagger_conf/swagger_delete_question.yml")
def delete_question():
    id_question = request.get_json()
    question = db.delete_question(id_question)
    del question["_id"]
    return Response(response=json.dumps(question),
                    status=200,
                    mimetype='application/json')

@app.route("/count_question", methods=["POST"])
@swag_from("./swagger_conf/swagger_count_question.yml")
def get_count_question():
    count = {"count": db.get_count_question()}
    return Response(response=json.dumps(count),
                    status=200,
                    mimetype='application/json')

@app.route("/get_all_question", methods=["POST"])
@swag_from("./swagger_conf/swagger_get_all_question.yml")
def get_all_question():
    questions = []
    for q in db.get_all_question():
        del q['_id']
        questions.append(q)

    return Response(response=json.dumps(questions),
                    status=200,
                    mimetype='application/json')
# ---------------------- user ------------------------
@app.route("/get_user", methods=["POST"])
@swag_from("./swagger_conf/swagger_get_user.yml")
def get_user():
    chat_id = request.get_json()['chat_id']
    user = db.get_user(chat_id)
    del user["_id"]
    return Response(response=json.dumps(user),
                    status=200,
                    mimetype='application/json')


@app.route("/get_all_user", methods=["POST"])
@swag_from("./swagger_conf/swagger_get_all_user.yml")
def get_all_user():
    # chat_id = request.get_json()

    lst_user = [i for i in db.get_all_user()]
    for user in lst_user:
        del user["_id"]
    return Response(response=json.dumps(lst_user),
                    status=200,
                    mimetype='application/json')

@app.route("/update_user", methods=["POST"])
@swag_from("./swagger_conf/swagger_update_user.yml")
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
