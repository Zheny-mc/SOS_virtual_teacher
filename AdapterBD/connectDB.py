from pymongo import MongoClient

class DataBase:
	def __init__(self, url):
		cluster = MongoClient(url)

		self.db = cluster["QuizBot"]
		self.users = self.db["Users"]
		self.questions = self.db["Questions"]

		self.questions_count = self.questions.count_documents({})

	def get_user(self, chat_id):
		user = self.users.find_one({"chat_id": chat_id})

		if user is not None:
			return user

		user = {
			"chat_id": chat_id,
			"is_passing": False,
			"is_passed": False,
			"question_index": None,
			"answers": []
		}

		self.users.insert_one(user)
		return user

	def get_all_user(self):
		return self.users.find({})

	def set_user(self, chat_id, update):
		self.users.update_one({"chat_id": chat_id}, {"$set": update})

	# ---------------------- question ------------------------
	def get_count_question(self):
		return self.questions.count_documents({})


	def get_question(self, index):
		return self.questions.find_one(index)

	def create_question(self, question):
		self.questions.insert_one(question)

	def delete_question(self, id):
		question = self.questions.find_one(id)
		if question is None:
			print(f"Error delete question with {id}")
		else:
			self.questions.delete_many(question)
			return question

	def get_all_question(self):
		return self.questions.find({})

	def update_question(self, id, kwargs):
		self.questions.update_one({"id": id}, {'$set': kwargs})

# db = DataBase()
# db.create_question(id=5, text="2+50", answers=["4","2","52"], correct=2)
# db.update_question(id=5, answers=["1", "2", "52"], correct=1)
# db.delete_question(5)