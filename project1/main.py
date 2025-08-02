from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user."""
    print("Tool 'say_hello' has been called.")
    return f"Hello {name}, nice to meet you! ❤️"

def main():
    model = ChatOpenAI(temperature=0)

    tool_list = [calculator, say_hello]
    agent_executor = create_react_agent(model, tool_list)

    print("Welcome! I'm your AI Assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYOU: ").strip()
        if user_input.lower() == "quit":
            break

        print("\nAssistant: ", end="")
        try:
            response = agent_executor.invoke(
                {"messages": [HumanMessage(content=user_input)]}
            )
            if "agent" in response and "messages" in response["agent"]:
                for message in response["agent"]["messages"]:
                    print(message.content, end="")
            else:
                print("Sorry, I didn't understand that.")
        except Exception as e:
            print(f"Error: {e}")
        print()

if __name__ == "__main__":
    main()
