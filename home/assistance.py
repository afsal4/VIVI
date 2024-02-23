from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, SystemMessage, HumanMessage


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class Assistance:

	def __init__(self, job_description) -> None:
		self.chat = ChatOpenAI(temperature=1)
		self.job_description = job_description
		self.messages = [
			SystemMessage(content=f"""you are a job interviewer and your job is to interview candidate according to company's need
						
						At the start of the interview welcome the candidate once and only once
						
						Company's job description: {job_description}
						
						questions that should be asked in the interview:
						(
							* should ask at least 12 questions
							* welcome the candidate at the start of the interview
							* ask questions about personal information
							* ask questions about how to handle certain cituations in the company
							* ask about 6 or more questions according to the job description,
							* you should always ask one question at a time and wait for his/her reply and ask again,
							* say the conclusion and finish the interview and at the end say "the interview is finished you can exit now",

						)
						
						You should only ask questions and nothing else
						
						"""), 
			
				SystemMessage(content="""
							Rules that should not be broken while having a conversation:
							(
								dont ask questions repeatedly,
								no questions for other jobs,
								ask questions one by one only after the candidate messages,
								should not give any information at the end whether candidate has passed or failed the interview
								)
								
								These rules are strict and should not be broken
								""")
		]

	def get_question(self):
		ai_question = self.chat.invoke(input=self.messages).content
		self.messages.append(AIMessage(ai_question))
		return ai_question

	def answer_question(self, answer):
		self.messages.append(HumanMessage(answer))





# for i in range(13):
#     ai = chat.invoke(input=messages_history).content
#     print(ai)

#     chats = input('your chats: ')
#     messages_history.append(AIMessage(ai))
    
#     messages_history.append(HumanMessage(chats))
    



