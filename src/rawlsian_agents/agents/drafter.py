from rawlsian_agents.agents.base_agent import Agent
from rawlsian_agents.utils.prompts import PRENUPTIAL_PROMPT

class Drafter(Agent):
    """
    An agent specialized in drafting the prenuptial agreement.
    """
    def __init__(self, prompt_template: dict = PRENUPTIAL_PROMPT) -> None:
        super().__init__(
            prompt_template=prompt_template["drafter"],
            input_variables=["claims", "edits"]
        )

    def draft_agreement(self, agreement: str, edits: str) -> str:
        """
        Drafts the final prenuptial agreement based on the claims and proposed edits.

        :param claims: The final claims or terms to be included in the agreement.
        :param edits: The proposed edits to enhance the agreement.
        :return: The final prenuptial agreement.
        """
        return self.generate_output(agreement=agreement, edits=edits).text()
