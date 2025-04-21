from rawlsian_agents.agents.base_agent import Agent

PROMPT = r"""
You are provided with a detailed prenuptial agreement and a list of proposed edits from the legal team intended to enhance its fairness, clarity, and conscionability. Your task is to produce a final version of the prenuptial agreement that fully incorporates each proposed edit into the text. Do not simply insert the edit instructions verbatim; instead, feel free to modify the relevant sections of the agreement so that the changes appear natural and coherent within the language of the document.
Do not hesitate to remove contradicting clauses from the original agreement and replace them by the proposed edits. Ensure that the final agreement is balanced, fair, and legally sound, reflecting the interests and rights of both parties.

Below are the proposed edits and the current agreement:

Proposed Edits:
{edits}

Original Prenuptial Agreement:
{agreement}

Instructions:
- Review the proposed edits carefully, ensuring each revision addresses any identified vulnerabilities, power imbalances, or unconscionable circumstances.
- Modify the corresponding sections in the agreement clearly and effectively to reflect the intended changes, preserving the document's overall coherence and readability.
- Do not include residual instructional language such as “Add a clause…” or “Insert text…” in the final document.
- Ensure the final agreement reads as an integrated, fair, and conscionable legal document, explicitly promoting balanced treatment and protection for both parties.
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
