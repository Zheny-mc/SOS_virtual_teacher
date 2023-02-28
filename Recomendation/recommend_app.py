from neo4j import GraphDatabase

def getConnect(file_path="cred.txt"):
    with open(file_path) as f:
        username, pwd, database, uri = f.readline().rstrip().split(',')
        # print(username, pwd, database, uri)
    return GraphDatabase.driver(uri=uri, auth=(username, pwd), database=database)

driver = getConnect()
session = driver.session()

def getListTest(courseName="Programming"):
    q1 = """
        match (test:TEST) - [] -> (:COURSE {name: $courseName}) return test 
        """
    dct = {"courseName": courseName}

    try:
        res = session.run(q1, dct).data()
        return {courseName: res}
    except Exception as e:
        print(str(e))
# print([i['test']['name'] for i in getListTest()])

def getQuestionForTest(testName="Ввод и Вывод", courseName="Programming"):
    q1 = """
        match (question:QUESTION) -[]-> (:TEST {name: "Ввод и Вывод"}) -[]-> (:COURSE {name: $courseName})
        match (ans:ANSWER) -[]-> (question)
        return question.name as name, collect(ans.name) AS answers
        """
    dct = {"courseName": courseName, "testName": testName}
    try:
        res = session.run(q1, dct).data()
        return res
    except Exception as e:
        print(str(e))

# print([i['question']['name'] for i in getQuestionForTest()])

def writeScoreTest(testName="Ввод и Вывод", studName="Vova", score=100):
    q1 = """
        match (test:TEST {name: $testName}) create (stud:STUDENT {name: $studName}), (test) -[:PASSED {score: $score}]-> (stud)
        """
    dct = {"testName": testName, "studName": studName, "score": score}
    try:
        return session.run(q1, dct).data()
    except Exception as e:
        print(str(e))

# writeScoreTest()

def writeResultTest(answers={"Что такое input?": True, "Что такое print?":False}, testName="Ввод и Вывод", studName="Vova"):
    getQuestionForTest()
    for quest, answer in answers.items():
        q1 = """
            match (quest:QUESTION {name: $quest}) -[]-> (test:TEST {name: $testName}), (stud:STUDENT {name: $studName})
            create (quest) - [:ANSWERED {isTrue: $answer}] -> (stud)
            """
        dct = {"testName": testName, "studName": studName, "quest": quest, "answer": answer}
        try:
            session.run(q1, dct)
        except Exception as e:
            print(str(e))

# writeResultTest()

def getTrueAnswers(testName="Ввод и Вывод"):
    q1 = """match (q:QUESTION) -[]-> (:TEST {name: $testName})
            match (q) <-[{flag: true}]- (ans:ANSWER)
            return q.name as question, ans.name as answer"""
    dct = {'testName': testName}
    try:
        return session.run(q1, dct).data()

    except Exception as e:
        print(str(e))


def getRecommendation(testName="Ввод и Вывод", studName="Vova"):
    q1 = """
        match (qs:QUESTION) -[]-> (:TEST {name: $testName}) -[]-> (stud:STUDENT {name: $studName})
        match (rec:RECOMMENDATION) -[]-> (qs) -[:ANSWERED {isTrue: true}]-> (stud)
        return rec.name as name
        """
    dct = {"testName": testName, "studName": studName}
    try:
        res = session.run(q1, dct).data()
        return res
    except Exception as e:
        print(str(e))

# print( ('\n').join([i['rec']['name'] for i in getRecommendation()]) )

def getGeneralRecommendation(testName="Ввод и Вывод", courseName="Programming"):
    q1 = """
        match (g_doc:GENERAL_RECOMMENDATION) - [] -> (:TEST {name: $testName}) - 
        [] -> (:COURSE {name: $courseName}) 
        return g_doc    
        """
    dct = {"testName": testName, "courseName": courseName}
    try:
        res = session.run(q1, dct).data()
        return res
    except Exception as e:
        print(str(e))

# print( ('\n').join([i['g_doc']['path'] for i in getRecommendation()]) )

def closeSession():
    session.close()
