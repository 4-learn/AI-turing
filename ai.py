import os
import json
from langchain_core.tools import Tool
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import OpenAI
from utils.module_tools import get_functions_from_files, import_function_from_file

def load_rag_tools(prompt):
    list_arg_tools = []
    directory = os.getenv("PATH_RAG_TOOLS")
    functions_dict = get_functions_from_files(directory)

    for file_path, functions in functions_dict.items():
        for function_name in functions:
            function = import_function_from_file(file_path, function_name)
            wrapped_function = lambda input_data, func=function, params=json.dumps(prompt, ensure_ascii=False): func(params)

            tool = Tool(
                name = function_name,
                func = wrapped_function,
                description = f"Wrapped function {function_name} with custom message"
            )
            list_arg_tools.append(tool)

    return list_arg_tools


def chat(text):
    llm = OpenAI(temperature=0)

    list_rag_tools = load_rag_tools(text)

    # Load the tools
    tools = load_tools([], llm=llm)

    # Initialize the agent with the specific tool
    agent = initialize_agent(
        tools + list_rag_tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        max_execution_time=30,
        verbose=False
    )

    try:
        # Ensure to pass a parameter when calling the agent
        result = agent({"input": text})
        return result['output']
    except Exception as e:
        print(str(e))