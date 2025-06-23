import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl,openai
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
from agents.run import RunConfig


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Chainlit application for Gemini AI Assistant
# This application uses the Gemini API to create an AI assistant that can respond to user queries.
@cl.on_chat_start
async def start():
    # Check if the API key is present; if not, raise an error
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
# Initialize the OpenAIChatCompletionsModel with the external client
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
# Create a RunConfig with the model and external client
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
# Create an Agent instance with the model and instructions
    agent: Agent = Agent(name="Assistant",
                         instructions="You are a helpful assistant.",
                         model=model
    )
    cl.user_session.set("agent", agent)
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I assist you today?").send()

# This function is called when a new message is received in the chat.
# It processes the message, runs the agent with the provided context, and sends a response back
# to the user. It also handles any exceptions that may occur during processing.
# The chat history is maintained in the user session, allowing the agent to have context for the
# conversation.
# The response is sent as a message in the chat, and any errors are caught and displayed
# to the user.
# The agent uses the Gemini API to generate responses based on the user's input and the chat history
# The agent is initialized with a set of instructions and a model, which is used to generate
# responses to user queries. The chat history is stored in the user session, allowing the agent
@cl.on_message
async def main(message: cl.Message):
        history = cl.user_session.get("chat_history") or []
        history.append({"role": "user", "content": message.content})



        msg = cl.Message(content="")
        await msg.send()

        agent: Agent = cast(Agent, cl.user_session.get("agent"))
        config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
        try:
              
            print("\n [CALLING _AGENT_WITH_CONTEXT] \n", history, "\n")
            result=Runner.run_streamed(agent, history, run_config=config)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                    token = event.data.delta
                    await msg.stream_token(token)


            history.append({"role": "assistant", "content": msg.content})
            cl.user_session.set("chat_history", history)        


            print(f"User: {message.content}")
            print(f"Assistant: {msg.content}")
        except Exception as e:
           
           
           await msg.update(content=f"Error: {str(e)}")
           print(f"Error : {str(e)}")