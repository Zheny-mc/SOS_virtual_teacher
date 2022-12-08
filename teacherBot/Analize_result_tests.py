import pandas as pd
import matplotlib.pyplot as plt
import os
import traceback
import logging

from teacherBot.data.connectDB import db

def get_df_from_db():
    lst_users = db.get_all_user()
    data_c = [user for user in lst_users]
    df = pd.DataFrame.from_records(data_c)
    return df

#  круговая схема
# сколько пользователей (завершило / не завершило) тест
def graph1(df):
    sr = df.groupby('is_passed')['chat_id'].count()
    sr.index = ['не прошел', 'прошел']
    sr.name = 'Круговая диаграмма'

    title = 'Cколько пользователей\n(завершило / не завершило) тест'
    sr.plot(title=title, kind='pie', subplots=True, figsize=(8, 5))
    # plt.show()
    # save image
    plt.savefig('./analize/graphics/graph1.png')

#  круговая схема
# сколько пользователей (прошло / не прошло) тест
def graph2(df):
    min_percentages = 80
    count_test_pass = df[df['percentages'] >= min_percentages]['chat_id'].count()
    count_test_failed = df[df['percentages'] < min_percentages]['chat_id'].count()
    data = pd.DataFrame({'Круговая диаграмма': [count_test_pass, count_test_failed]},
                        index=['сдали тест', 'провалили тест'])

    title = 'Cколько пользователей\n(прошло / не прошло) тест'
    data.plot(title=title, kind='pie', subplots=True, figsize=(8, 5))
    plt.legend(loc="right", prop={'size': 10 })
    # plt.show()
    # save image
    plt.savefig('./analize/graphics/graph2.png')


#  гистограмма
# Уровень правильного прохождения теста каждым студентов
def graph3(df):
    df = df[['chat_id', 'true_count', 'false_count']]
    df['chat_id'] %= 100

    # plotting false_count
    ax = df.plot(x="chat_id", y="false_count", kind="bar", color="maroon")
    # plotting true_count
    df.plot(x="chat_id", y="true_count", kind="bar", ax=ax, color="green", rot=45)

    plt.legend(['не верно', 'верно'])
    plt.title("Уровень правильного прохождения теста каждым студентов")
    plt.ylim(0, max(df['false_count'])+1)
    # plt.show()
    # save image
    plt.savefig('./analize/graphics/graph3.png')

graphics = {
    1: lambda df: graph1(df),
    2: lambda df: graph2(df),
    3: lambda df: graph3(df)
}

def get_one_graphic(num_graph):
    history_df = get_df_from_db()
    graphics[num_graph](history_df)
    return f'./analize/graphics/graph{num_graph}.png'

def get_all_graphics():
    history_df = get_df_from_db()
    file_names = []
    for i in graphics.keys():
        graphics[i](history_df)
        file_names.append(f'./analize/graphics/graph{i}.png')
    return file_names

def drop_grapics():
    try:
        mydir = './analize/graphics/'
        filelist = [f for f in os.listdir(mydir)]
        for f in filelist:
            os.remove(os.path.join(mydir, f))
    except Exception as e:
        logging.error(traceback.format_exc())

# print(get_one_graphic(1))
# print(get_one_graphic(2))
# print(get_one_graphic(3))

# print(get_all_graphics())
# drop_grapics()




