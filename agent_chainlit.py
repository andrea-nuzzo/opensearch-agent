import chainlit as cl
import re
from typing import List
from agent import agent_factory
from langchain.agents.agent import AgentExecutor

KEY_AGENT = "agent"
KEY_USER_QUESTIONS = "user_questions"

@cl.on_chat_start
async def on_chat_start():
    agent = agent_factory()
    cl.user_session.set(KEY_AGENT, agent)
    cl.user_session.set(KEY_USER_QUESTIONS, [])
    await cl.Message(content="OpenSearch Agent started").send()

@cl.on_message
async def on_message(message: cl.Message):
    
    agent: AgentExecutor = cl.user_session.get(KEY_AGENT)
    cb = cl.AsyncLangchainCallbackHandler()
    user_questions: List = cl.user_session.get(KEY_USER_QUESTIONS)
    user_questions = user_questions[-3:]
    joined_questions = '\n'.join(user_questions)
    
    memory_questions = f"""
        Here are some previous questions that you do not need to answer but consider in relationship to the actual question:
        ```
        {joined_questions}
        ```
        """ if len(joined_questions) else ""
    
    prompt = f"""
    Make sure that you query first the indices in the OpenSearch database.
    Make sure that after querying the indices you query the field names.

    {memory_questions}

    Then answer this question:
    {message.content}
    """
    
    response = await cl.make_async(agent.run)(input=prompt, callbacks=[cb])
    
    if "graph" in response:
        img_path_match = re.search(r"\(sandbox:(.*?)\)", response)
        if img_path_match:
            img_path = img_path_match.group(1).strip()

            image = cl.Image(path=img_path, name="plot_image", display="inline")

            response_text = response.split("\n\n")[0]

            await cl.Message(content=response_text, elements=[image]).send()
    else:
        await cl.Message(content=response).send()
        user_questions.append(prompt)
        cl.user_session.set(KEY_USER_QUESTIONS, user_questions)
