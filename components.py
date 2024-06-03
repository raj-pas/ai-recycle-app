import requests
import json
from typing import (
    Any,
    Dict,
    List,
)

from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import Tool
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from openai import _exceptions as openai_exceptions

from settings import (
    LLM_MODEL,
)


# Build Recycle Product Search API Tool

def item_search_api(identified_item: str) -> List[Dict[str, str]]:
    # Define URL
    url = "https://api.recollect.net/api/areas/MMSM/services/1173/pages"

    # Define headers
    headers = {
        "Content-Type": "application/json"
    }

    # Define query parameters
    query_params = {
        "suggest": identified_item,
        "type": "material",
        "set": "winnipeg",
        "include_links": "true",
        "locale": "en",
        "accept_list": "true"
    }

    # Call API
    response = requests.get(url, params=query_params, headers=headers)

    try:
        # Parse JSON response
        result = [
            {
                "error": "NoResultsFound",
                "message": f"No results found for identified_item: {identified_item}",
            },
        ]
        response_json = json.loads(response.text)
        if response_json:
            result = [
                {
                    "item_name": element["title"],
                    "item_synonym": element["synonym"],
                    "item_id": element["id"],
                }
                for element in response_json
            ]
        return result
    except requests.exceptions.JSONDecodeError as e:
        return [
            {
                "error": "JSONDecodeError",
                "message": "Could not parse JSON response",
                "response": response.text
            }
        ]


class ItemSearchApiInput(BaseModel):
    identified_item: str = Field(description="Identified item name from image recognition to search for in Recycle Product Search API to get the item_name, item_synonym, and item_id")


item_search_tool_description = """Search for identified_item in Recycle Product Search API to get the item name, synonym, and id.
Use this tool after identifying the item in an image using the Model/LLM.
Always use this tool before call item_detail_tool to verify the item_name, item_synonym, and item_id. Verify the item_id is correct by comparing the item_name against identified_item before calling the item_detail_tool.
"""

item_search_tool = Tool(
    name="item_search_tool",
    func=item_search_api,
    description=item_search_tool_description,
    args_schema=ItemSearchApiInput,
    handle_tool_error=True,
    handle_validation_error=True,
)


# Build Recycle Product Detail API Tool

def item_detail_api(item_id: str) -> Dict[str, Any]:
    # Build URL
    url = f"https://api.recollect.net/api/areas/MMSM/services/1173/pages/en/{item_id}.json"

    # Define headers
    headers = {
        "Content-Type": "application/json"
    }

    # Call API
    response = requests.get(url, headers=headers)

    try:
        # Parse JSON response
        response_json = json.loads(response.text)
        if response_json and response_json.get("sections"):
            return response_json["sections"]
        return {
            "error": "NoResultsFound",
            "message": f"No results found for item_id: {item_id}",
        }
    except requests.exceptions.JSONDecodeError as e:
        return {
            "error": "JSONDecodeError",
            "message": "Could not parse JSON response",
            "response": response.text
        }


class ItemDetailApiInput(BaseModel):
    item_id: str = Field(description="Item id from Recycle Product Search API to get the item details")


item_detail_tool_description = """Get the item details from Recycle Product Detail API using the item_id.
Use this tool after calling item_search_tool to get the item_id.
Always use this tool after calling item_search_tool to get the item details.
Parse the details provided as JSON to let user know if they can recycle the item? And any additional details
"""

item_detail_tool = Tool(
    name="item_detail_tool",
    func=item_detail_api,
    description=item_detail_tool_description,
    args_schema=ItemDetailApiInput,
    handle_tool_error=True,
    handle_validation_error=True,
)

# Setup LLM
llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0,
    streaming=True,
)


# Build Identify Image Tool
@tool(infer_schema=True)
def identify_image(image_url: str) -> str:
    """
    Identify the main item in the given image.
    Pass image url to get the main item in the image.
    return: main item in the image
    Always call this tool before calling item_search_tool.
    """
    human_message = HumanMessage(content=[
        { "type": "text", "text": "What is the main item in the image in maximum 2 words" },
        { "type": "image_url", "image_url": { "url": image_url }}
    ])
    try:
        output = llm.invoke([human_message])
        return output.content
    except openai_exceptions.BadRequestError as e:
        return "Could not identify the item in the image due to BadRequestError"

# Build Agent and Executor
prompt = hub.pull("hwchase17/openai-tools-agent")
tools=[
    item_search_tool,
    item_detail_tool,
    identify_image,
]

agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)


