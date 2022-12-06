from pymongo import MongoClient

class DataBase:
	def __init__(self):
		cluster = MongoClient("mongodb://localhost:27017")

		self.db = cluster["QuizBot"]
		self.users = self.db["Users"]
		self.current_question = self.db["CurrentQuestion"]
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

	def get_all_users(self):
		return self.users.find({})

	def set_user(self, chat_id, update):
		self.users.update_one({"chat_id": chat_id}, {"$set": update})

	def get_count_question(self):
		return self.questions.count_documents({})

	# ---------------------- question ------------------------
	def get_question(self, index):
		return self.questions.find_one({"id": index})

	def create_question(self, question):
		self.questions.insert_one(question)

	def delete_question(self, id):
		question = self.questions.find_one({"id": id})
		if question is not None:
			self.questions.delete_many(question)
		else:
			print(f"Error delete question with {id}")

	def update_question(self, id, kwargs):
		self.questions.update_one({"id": id}, {'$set': kwargs})

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