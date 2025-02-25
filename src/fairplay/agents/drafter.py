from fairplay.agents.base_agent import Agent

PROMPT = r"""
You have a detailed prenuptial agreement that outlines the specific terms and conditions both parties have agreed upon. 
The legal team have proposed the following edits to enhance the agreement:
{edits}

Your task is to draft the final prenuptial agreement based on the following agreement and proposed edits. All edits should be incorporated into the final agreement.

Current agreement:
{agreement}
"""


class Drafter(Agent):
    """
    An agent specialized in drafting the prenuptial agreement.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
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
