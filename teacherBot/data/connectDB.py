from pymongo import MongoClient

from teacherBot.data.implement_request import impl_request


class DataBase:
	def __init__(self):
		cluster = MongoClient("mongodb://localhost:27017")
		self.db = cluster["LocalQuestion"]
		self.current_question = self.db["CurrentQuestion"]

	# ---------------------- user ------------------------
	def get_user(self, chat_id):
		data = { "id": chat_id }
		return impl_request(type_url='get_question', data=data)

	def get_all_user(self):
		return impl_request(type_url='get_all_user')

	def set_user(self, chat_id, update: dict):
		data = { key: val for key, val in update.items() }
		data["chat_id"] = chat_id
		impl_request(type_URL='update_user', data=data)

	# ---------------------- question ------------------------
	def get_count_question(self):
		res = impl_request(type_url='count_question')
		return res['count']

	def get_question(self, id: int):
		data = {"id": id}
		return impl_request('get_question', data)

	def create_question(self, question):
		impl_request('create_question', question)

	def delete_question(self, id):
		data = {"id": id}
		impl_request('delete_question', data)

	# ------------------ current question --------------------
	def get_current_question(self, id):
		cur_question = self.current_question.find_one({"id": id})

		if cur_question is not None:
			return cur_question

		cur_question = {
			"id": id,
			"text": "",
			"answers": [],
			"correct": None
		}

		self.current_question.insert_one(cur_question)

		return cur_question

	def create_current_question(self, question):
		self.current_question.insert_one(question)

	def delete_current_question(self, id):
		question = self.current_question.find_one({"id": id})
		if question is not None:
			self.current_question.delete_many(question)
		else:
			print(f"Error delete question with {id}")

	def update_current_question(self, id, kwargs):
		self.current_question.update_one({"id": id}, {'$set': kwargs})

db = DataBase()
# db.create_question(id=5, text="2+50", answers=["4","2","52"], correct=2)
# db.update_question(id=5, answers=["1", "2", "52"], correct=1)
# db.delete_question(5)