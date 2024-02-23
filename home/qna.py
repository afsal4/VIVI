from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, SystemMessage, HumanMessage
from  .audio_transcription import A_t

a_t = A_t()

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



from .text_to_speech import TTS

tts = TTS()


from .score import Score




class Assistance:
    
    def __init__(self, job_description):
        self.chat = ChatOpenAI(temperature=1)
        self.job_description = job_description
        self.messages = [
            SystemMessage(content=f"""you are a job interviewer and your job is to interview candidate according to company's need
                        
                        At the start of the interview welcome the candidate once and only once
                        
                        Company's job description: {job_description}
                        
                        questions that should be asked in the interview:
                        (
                            * should only ask 2 question total and the 3rd reply should end the session
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



class Q_and_A():
    
    def __init__(self,job_description):
        self.assist = Assistance(job_description)
        self.jb = job_description
        self.curent_question=''
        self.current_answer = ''
        self.qna_data = []


        
    def ask_quesiton(self, repeat=0):
        
        selected_voice,selected_model = "nova","tts-1-hd"
        
        if repeat == 1:
            ai_question = self.curent_question
        else:
            ai_question = self.assist.get_question()
            self.curent_question = ai_question
             
        
        
       
        ret = tts.ask_question_and_play(selected_voice, selected_model, ai_question)
        return ret,ai_question
        
    def speak_answer(self):
        
        # answer = a_t.record_and_transcribe()
        
        answer = """Thanks for your ML question! While I don't have the specifics at the moment, I'm intrigued by the topic and will dig in to provide a better response soon. Your curiosity fuels our collective learning.
        Feel free to share any ML insights you come across in the meantime. Let's explore this together!"""
        
        print(answer, '\n\n\n\n\n\n')
        
        self.assist.answer_question(answer=answer)
        
        return answer
    
    def question_answer_score(self, db, job_description):
        score = Score()
        for row in db:
            question = row['question']
            answer = row['answer']
            answer_score = score.answer_score(question, answer, job_description)
            
            self.qna_data.append({
                'question':question,
                "answer":answer,
                "q_a_score": answer_score
            }
        )
        
        return score.overall_total
    
    
if __name__ == "__main__":
    qa = Q_and_A("This is for a machine learning interview")
    qa.ask_quesiton(0)
    qa.speak_answer()

        
        
        
        

        
        