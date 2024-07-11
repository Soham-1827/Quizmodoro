from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

load_dotenv()
class Question:
    def __init__(self, prompt, options, answer):
        self.prompt = prompt
        self.options = options
        self.answer = answer
        
# def generate_questions(text):
#     chunks = get_text_chunks(text)
#     response = query_llm("\n".join(chunks))
#     # print(response) Use this for Debugging
#     questions = []
#
#     question_answer_pairs = response.split("**Questions:**")[1].split("**Answers:**")
#     questions_text = question_answer_pairs[0].strip().split('\n\n')
#     answers_text = question_answer_pairs[1].strip().split('\n')
#
#     for i, question_text in enumerate(questions_text):
#         question_parts = question_text.strip().split('\n')
#         if len(question_parts) >= 2:
#             question_prompt = question_parts[0]  # Question prompt
#             options = [option.strip()[4:] for option in question_parts[1:]]
#             correct_answer = answers_text[i].split(' ')[1]
#             questions.append(Question(question_prompt, options, correct_answer))
#
#     return questions
def generate_questions(text):
    chunks = get_text_chunks(text)
    response = query_llm("\n".join(chunks))
    questions = []

    question_answer_pairs = response.split("**Questions:**")[1].split("**Answers:**")
    questions_text = question_answer_pairs[0].strip().split('\n\n')
    answers_text = question_answer_pairs[1].strip().split('\n')

    for i, question_text in enumerate(questions_text):
        question_parts = question_text.strip().split('\n')
        if len(question_parts) >= 2:
            question_prompt = question_parts[0]  # Question prompt
            options = [option.strip()[4:] for option in question_parts[1:]]
            correct_answer_letter = answers_text[i].split(' ')[1]
            correct_answer_index = ord(correct_answer_letter) - ord('A')  # Convert letter to index (0-based)
            questions.append(Question(question_prompt, options, correct_answer_index))

    return questions



def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000,
                                              chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks  # list of strings


def query_llm(context):
    prompt_template = f"""
    Generate 10 multiple-choice questions with 4 options based on the given context and after all the questions and options are done , tell the correct answers(capital) for all the questions.\n\n
    Context:\n {context}\n
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3
    )
    return model.invoke(prompt_template).content
    # prompt = PromptTemplate(template=prompt_template,
    #                         input_variables=["context"])
    # chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    # return chain
