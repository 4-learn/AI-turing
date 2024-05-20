import requests
import json
from langchain.agents import tool, load_tools, initialize_agent, AgentType
from langchain_openai import OpenAI

@tool
def device_info(text: str) -> str:
    """Return device's status."""
    url = "http://211.21.113.190:8155/api/states/switch.mqtt_ntnu_1_2_sw_2"

    payload = ""
    headers = {
        'Content-type': 'application/json ',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.request("GET", url, headers = headers, data = payload)

    return json.dumps(response.text)

def chat(text):
    llm = OpenAI(temperature=0)

    # Load the tools
    tools = load_tools([], llm=llm)

    # Initialize the agent with the specific tool
    agent = initialize_agent(
        tools + [device_info],
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