from fairplay.agents.base_agent import Agent

PROMPT = r"""
You are provided with a detailed prenuptial agreement and a list of proposed edits from the legal team intended to improve its fairness and clarity. Your task is to produce a final version of the prenuptial agreement that fully incorporates each proposed edit into the text. Do not simply insert the edit instructions verbatim; instead, seamlessly modify the relevant sections of the agreement so that the changes appear as part of the natural language of the document.

Below are the proposed edits and the current agreement:

Proposed Edits:
{edits}

Original Prenuptial Agreement:
{agreement}

Instructions:
- Review the proposed edits carefully.
- For each edit, modify the corresponding section in the agreement to reflect the intended change.
- Do not include any residual language such as “Add a clause…” in the final document.
- Ensure that the final agreement reads as a coherent, integrated legal document with all changes incorporated.
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
