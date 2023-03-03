from Recomendation.recommend_app import *

# просмотр тестов курса
course_name = "Programming"
lst_test = [i['test']['name'] for i in getListTest()[course_name]]
print(lst_test[::-1])

# ввод желаемого теста
test_name = "Ввод и Вывод" # input()
# Получение теста
print(f'Прохожение теста \'{test_name}\'')
question = getQuestionForTest()
dct_q = { (q['name'], i): q['answers'] for i, q in enumerate(question, 1) }

for q, a in dct_q.items():
    print(q[1], q[0])
    for j, val in enumerate(a, 1):
        print(f'\t{j} {val}')

# Получение ответов на тест
dct_answers = { 'Что такое input?': ['ввод с экрана'], 'Что такое print?': ['ввод с экрана'] }
print(*dct_answers.items(), sep='\n')

# получение правильных ответов
trueAns = { dct_i['question']: dct_i['answer'] for dct_i in getTrueAnswers()}
# проверка
dct_res_check = { }
for q, a in dct_answers.items():
    if len(a) == 1:
        dct_res_check[q] = trueAns[q] == a[0]
    else:
        dct_res_check[q] = False

# получаем оценку
count = 0
for is_ans in dct_res_check.values():
    if is_ans:
        count += 1
score_test = int( (count / len(question)) * 100)


# Записываем в БЗ
writeScoreTest(score=score_test, studName="Tanay")
writeResultTest(answers=dct_res_check, studName="Tanay")

recom = [i['name'] for i in getRecommendation(studName="Tanay")]

print(f'Оценка = {score_test}')
print(*recom, sep='\n')
