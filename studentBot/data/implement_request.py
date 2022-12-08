import requests

URLS = {
    'get_question':     "/get_question",
    'count_question':   "/count_question",
    'get_user':         "/get_user",
    'update_user':      "/update_user",
    'get_all_question': "/get_all_question"
}

def impl_request(type_url, dict_data={}):
    url = URLS[type_url]
    BASE_URL = "http://localhost:5000"
    r = requests.post(f"{BASE_URL}{url}", json=dict_data)
    if (r.status_code == 200):
        return r.json()
    else:
        # бросить исключение
        print(r.text)
        print(r.status_code)

# id = 0
# data = {
#     "id": id
# }
# type_URL = 'get_question'
#
# print( impl_request(type_URL, data) )

