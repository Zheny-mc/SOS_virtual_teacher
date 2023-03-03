from Recomendation.TestingStudent import TestingStudent

test = TestingStudent()
print(test.course_name)
print(test.dct_test)

test_name = "Ввод и Вывод"
print(test.question(test_name))

dct_answers = { 'Что такое input?': ['вывод на экран'], 'Что такое print?': ['ввод с экрана'] }
print(test.check_test(dct_answers))