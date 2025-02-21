#%%
import os
from dotenv import load_dotenv
from autogen import ConversableAgent#, GroupChat, GroupChatManager << Unused
from fairplay import system_messages

#%%
# Load environment variables from .env file
load_dotenv()
#%%

PERSON_A = """
You are Person A who tries to negotiate a prenuptial agreement 
with your partner. You want to make sure that you are satisfied
with the agreement. You have a yearly income of $100,000 and 
you own a house that is worth $500,000. You have a savings 
account with $50,000. You want to make sure that you keep your 
house and your savings account in case of a divorce. You want 
to be able to make sure that the share account is invested 
with care so that your saving grows. In the event of your 
parents pass away, you do not want to share their inheritance 
with your partner. You have to make sure all of your concerns 
are addressed.
"""

PERSON_B = """
You are Person B who tries to negotiate a prenuptial agreement 
with your partner. You want to make sure that you are satisfied 
with the agreement. You have a yearly income of $50,000 and 
you own a car that is worth $20,000. You have a savings account 
with $10,000. You want to make sure that you keep your car and 
your savings account in case of a divorce. You are very 
conservative with investments. You have to make sure all of your 
concerns are addressed.
"""

# %%
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
# %%
