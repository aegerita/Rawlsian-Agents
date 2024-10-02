import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from autogen import ConversableAgent, GroupChat, GroupChatManager

agent_a = ConversableAgent(
    name="Person_A",
    system_message="You are Person A. You answer questions and only answer questions based on Person A. Person A must act like a normal person with actual opinions. Person A has a yearly income of $100,000 and you own a house that is worth $500,000. Person A has a savings account with $50,000. Person A wants to make sure that you keep your house and your savings account in case of a divorce. Person A wants to be able to make sure that the share account is invested with care so that your savings grows. In the event of Person A's parents passing away, Person A does not want to share their inheritance with their partner. When the agreement is provided, you should give your feedback on each point of the agreement. You should always provide your feedback to any suggestion on the agreement based on Person A's interest.",
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="ALWAYS",
)
agent_b = ConversableAgent(
    name="Person_B",
    system_message="You are Person B. You answer questions and only answer questions based on Person B. Person B must act like a normal person with actual opinions. Person B has a yearly income of $50,000 and you own a car that is worth $20,000. Person B has a savings account with $10,000. Person B wants to make sure that you keep your car and your savings account in case of a divorce. Person B is very conservative with investment. When the agreement is provided, you should give your feedback on each point of the agreement. You should always provide your feedback to any suggestion on the agreement based on Person B's interest.",
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="ALWAYS",
)

lawyer = ConversableAgent(
    name="lawyer",
    system_message="You are a lawyer who tries to help a couple negotiate a prenuptial agreement. You want to make sure that both parties are satisfied with the agreement. You want to make sure that the agreement is fair to both parties. You also want to make sure that the agreement is legally binding, and that it will hold up in court. You need to provide legal advice to both parties. You need to make sure that the agreement is thorough and covers all possible scenarios. When faced with request to change the current agreement, you should propose potential clauses to the problem, and ask for opinion on this matter for a compromising solution. When both parties are satisfied with the agreement, you can conclude the meeting with the phrase 'thank you for your time'. But before you say that, you will have to provide a summary of the agreement to both parties in point form, and ask them both for their opinion.",
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="ALWAYS",
)

allowed_transitions = {
    agent_a: [lawyer],
    agent_b: [lawyer],
    lawyer: [agent_a, agent_b],
}

constrained_group_chat = GroupChat(
    agents=[agent_a, agent_b, lawyer],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    max_round=100,
    messages=[],
    send_introductions=False,   # vail of ignorance
)

constrained_group_chat_manager = GroupChatManager(
    groupchat=constrained_group_chat,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
    # is_termination_msg=lambda msg: "thank you for your time" in msg["content"].lower() or "thank you both for your time" in msg["content"].lower(),
    human_input_mode="ALWAYS",
)

chat_result = lawyer.initiate_chat(
    constrained_group_chat_manager,
    message="Thank you for meeting with me. A prenuptial agreement is a proactive way to ensure both of your financial interests are clearly outlined and protected before marriage. We'll go over your individual assets, debts, and expectations, then craft an agreement tailored to your needs, ensuring transparency and fairness for both parties. Let us start with person A. A, can you summarize your assets and expectations?",
    summary_method="reflection_with_llm",
)
    
