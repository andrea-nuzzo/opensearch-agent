from langchain.agents.agent import AgentExecutor
from langchain.schema import SystemMessage
from tools.list_indices_tool import ListIndicesTool
from tools.index_details_tool import IndexDetailsTool
from tools.index_data_tool import IndexShowDataTool
from tools.plot_data_tool import create_plot_tool
from tools.index_search_tool import create_search_tool
from langchain_openai import ChatOpenAI
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from dotenv import load_dotenv
import os

load_dotenv()

apy_key = os.getenv("OPENAI_API_KEY")

def agent_factory() -> AgentExecutor:
    
    llm = ChatOpenAI(
        openai_api_key=apy_key,
        model="gpt-4-0125-preview",
        temperature=0,
        verbose=False
    )
    
    tools = [ListIndicesTool(), IndexDetailsTool(),IndexShowDataTool(),create_search_tool(), create_plot_tool()]

    agent_obj = OpenAIFunctionsAgent.from_llm_and_tools(
        llm, tools,
        system_message=SystemMessage(content="You are a helpful AI Opensearch Expert Assistant"),
    )
    
    return AgentExecutor.from_agent_and_tools(
        agent=agent_obj, tools=tools, verbose=True
    )

