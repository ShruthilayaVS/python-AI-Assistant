from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b:float) ->str:
    """usefull for perofroming baisc arithmetic calculation with number"""
    print("here is the calculator") 
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name:str)->str:
    #useful for greeting a user
    print("tool has been called")
    return f"hello {name}, Nice to meet you <3"


def main():
    model = ChatOpenAI(temperature=0)

    tools=[calculator, say_hello]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI Assistant. Type 'quit to exit.")
    print("You can ask me to perfrom calculation or caht with me.")

    while True:
        user_input = input("\nYOU: ").strip()
        if user_input=="quit":
            break
        print("\nAssistant: ",end="")
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        print()

if __name__ == "__main__":
    main()
           
