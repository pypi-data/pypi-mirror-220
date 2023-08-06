from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentType,initialize_agent
from langchain.utilities import SerpAPIWrapper

from weathon.dl.utils.constants.default_constant import OPENAI_API_BASE,OPENAI_API_KEY, SERPAPI_API_KEY

import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE


def chatbot():


    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("下述是一段人类与AI的友好对话，AI很健谈且能针对内容提供许多关键细节信息。当AI对一个问题不知道答案是什么，它会诚实的说不知道。"),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    llm = ChatOpenAI(temperature=0)

    # 定义历史记忆的类型
    memory = ConversationBufferMemory(return_messages=True)
    # 定义chain类型
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    assistant_chat = "你好，我是你的智能助理，现在我们可以对话啦~"
    while True:
        user_input = input(assistant_chat)
        assistant_chat = conversation.predict(input=user_input)


def chatbot_agent():
    # 从官网获取serpapi key,填入serpapi_api_key中，如果使用其他tool则不需要设置
    search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
    tools = [
        Tool(name="Current Search",func=search.run,description="useful for when you need to answer questions about current events or the current state of the world"), 
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = ChatOpenAI(temperature=0)

    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,memory=memory,handle_parsing_errors=True )

    assistant_chat = "你好，我是你的智能助理，现在我们可以对话啦~"
    while True:
        user_input = input(assistant_chat)
        assistant_chat = agent_chain.run(input=user_input)

