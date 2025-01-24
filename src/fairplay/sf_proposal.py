#%%
import os
from dotenv import load_dotenv
from autogen import ConversableAgent, AssistantAgent, GroupChat, GroupChatManager
from fairplay import system_messages

#%%
# Load environment variables from .env file
load_dotenv()
#%%

draft_creator = AssistantAgent(
    name="draft_creator",
    system_message=system_messages.DRAFT_CREATOR,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"], "response_format": "json_object"}]},
)

###https://microsoft.github.io/autogen/0.2/docs/notebooks/JSON_mode_example#defining-allowed-speaker-transitions

reviewer = ConversableAgent(
    name="reviewer",
    system_message=system_messages.REVIEWER,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
)

arbitreur = ConversableAgent(
    name="arbitreur",
    system_message=system_messages.ARBITREUR,
    llm_config={"config_list": [{"model": os.environ["MODEL"], "api_key": os.environ["OPENAI_API_KEY"]}]},
)

allowed_transitions = {
    draft_creator: [reviewer],
    reviewer: [arbitreur],
    arbitreur: [reviewer],
}

group_chat = GroupChat(
    agents=(draft_creator, reviewer, arbitreur),
    messages=[],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    max_round=10,
)

manager = GroupChatManager(
    groupchat=group_chat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

chat_result = arbitreur.initiate_chat(manager, message="Get an agreement on a prenuptial contract.")
# %%
