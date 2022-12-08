from pymongo import MongoClient

from studentBot.data.implement_request import impl_request


class DataBase:
	# ---------------------- user ------------------------
	def get_user(self, chat_id):
		data = { "chat_id": chat_id }
		return impl_request('get_user', data)

	def set_user(self, chat_id, update: dict):
		data = { key: val for key, val in update.items() }
		data["chat_id"] = chat_id
		impl_request('update_user', data)

	# ---------------------- question ------------------------
	def get_count_question(self):
		res = impl_request(type_url='count_question')
		return res['count']

	def get_question(self, id: int):
		data = {"id": id}
		return impl_request('get_question', data)

	def get_all_question(self):
		return impl_request(type_url='get_all_question')

db = DataBase()
# db.create_question(id=5, text="2+50", answers=["4","2","52"], correct=2)
# db.update_question(id=5, answers=["1", "2", "52"], correct=1)
# db.delete_question(5)