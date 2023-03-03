import recommend_app as r

class TestingStudent:

    def __init__(self) -> None:
        self.studName = "Tanay"
        self.course_name = "Programming"
        lst_test = [i['test']['name'] for i in r.getListTest()[self.course_name]][::-1]
        self.dct_test = {t: f'/test/{t}' for t in lst_test}

    def question(self, test_name:str):
        quest = r.getQuestionForTest(testName=test_name)
        self.dct_question = {(q['name'], i): q['answers'] for i, q in enumerate(quest, 1)}
        return self.dct_question

    def check_test(self, dct_answers):
        # получение правильных ответов
        trueAns = {dct_i['question']: dct_i['answer'] for dct_i in r.getTrueAnswers()}
        # проверка
        dct_res_check = {}
        for q, a in dct_answers.items():
            if len(a) == 1:
                print(trueAns[q])
                print(a[0])
                dct_res_check[q] = (trueAns[q] == a[0])
            else:
                dct_res_check[q] = False

        # получаем оценку
        count = 0
        for is_ans in dct_res_check.values():
            if is_ans:
                count += 1
        self.score_test = int((count / len(trueAns)) * 100)

        # Записываем в БЗ
        r.writeScoreTest(score=self.score_test, studName=self.studName)
        r.writeResultTest(answers=dct_res_check, studName=self.studName)

        self.recom = [i['name'] for i in r.getRecommendation(studName=self.studName)]
        if len(self.recom) == 0:
            self.recom = ['Молодец, продолжайте в том же духе)']
        return {'score': self.score_test, 'recom': self.recom}



