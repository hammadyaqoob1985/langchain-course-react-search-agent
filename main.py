from dotenv import load_dotenv
from langchain_core import output_parsers
from langchain_core.output_parsers import format_instructions

load_dotenv()

from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse



tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4")
structured_llm = llm.with_structured_output(AgentResponse)
react_prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt=react_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

extract_output = RunnableLambda(lambda x: x["output"])


chain = agent_executor | extract_output | structured_llm

def main():
    print("Hello from langchain-course-react-search-agent!")
    result = chain.invoke({"input": "Return 3 stocks that are recommended for the next 3 months 2025?"})
    print(result)

if __name__ == "__main__":
    main()
