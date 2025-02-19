#%%
import os
from dotenv import load_dotenv
from autogen import ConversableAgent#, GroupChat, GroupChatManager << Unused
from fairplay import system_messages

#%%
# Load environment variables from .env file
load_dotenv()
#%%

agent_a = ConversableAgent(
    name="Person_A",
    system_message=system_messages.PERSON_A,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
)
agent_b = ConversableAgent(
    name="Person_B",
    system_message=system_messages.PERSON_B,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
)

chat_result = agent_a.initiate_chat(
    agent_b,
    message="Hello, I am Person A. I want to make sure that we are both satisfied with the prenuptial agreement. You should start by summarizing your assets and expectations.",
    summary_method="reflection_with_llm",
    max_turns=20,
)
    
### This is a good start but does not provide a legal document. It also fails to work under a veil of ignorance, as each party knows its role, initial conditions and constraints and pushes only for themselves. 