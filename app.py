
import sys

from langchain_core.messages import HumanMessage

from components import executor

def main(arg):
    print(f'Argument received: {arg}')
    human_message = HumanMessage(content=[
        { "type": "text", "text": "Can I recycle it? Also any additional information if available would be helpful" },
        { "type": "image_url", "image_url": { "url": arg }}
    ])
    response = executor.invoke({"input": human_message})
    print(response["output"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide an argument.")
