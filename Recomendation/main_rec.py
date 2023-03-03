from flask import Flask, render_template, request, redirect

from Recomendation.TestingStudent import TestingStudent

app = Flask(__name__)
test = TestingStudent()

@app.route('/')
def index():
    return render_template('index.html',
                           course_name=test.course_name,
                           lst_test=test.dct_test)


@app.route('/test/<test_name>', methods=['POST', 'GET'])
def testing(test_name):
    quest_data=test.question(test_name)
    if request.method == "POST":
        dct_answers = { q[0]: request.form.getlist(q[0]) for q in quest_data }
        res_dct = test.check_test(dct_answers)
        return render_template('recommend.html',
                           course_name=test.course_name,
                           lst_test=test.dct_test,
                           score=res_dct['score'],
                           rec=res_dct['recom'])

    return render_template('testing.html',
                           course_name=test.course_name,
                           lst_test=test.dct_test,
                           test_name=test_name,
                           data=quest_data)


if __name__ == "__main__":
    app.run(debug=True)