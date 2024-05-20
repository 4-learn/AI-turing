from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os

def chat(text):
    llm = OpenAI()
    prompt = PromptTemplate(
        input_variables=["question"],
        template = "你是 " + os.getenv("BOT_NAME") + ", 是我的數位助手，現在有個問題想請教你: {question}",
    )

    # Response
    try:
        return llm.invoke(prompt.format(question=text))
    except Exception as e:
        print(str(e))
        return os.getenv("BOT_NAME") + " 壞掉了，趕快請人類來修理: " + str(e)

