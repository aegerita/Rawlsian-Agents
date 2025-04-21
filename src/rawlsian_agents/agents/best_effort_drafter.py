from fairplay.agents.base_agent import Agent

PROMPT = r"""
You are provided with a prenuptial agreement and your task is to enhance its fairness, clarity, and conscionability. Feel free to modify the relevant sections of the agreement so that the changes appear natural and coherent within the language of the document.
Ensure that the final agreement is balanced, fair, and legally sound.

Original Prenuptial Agreement:
{agreement}
"""


class BestEffortDrafter(Agent):
    """
    An agent specialized in drafting the prenuptial agreement.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["agreement"]
        )

    def draft_agreement(self, agreement: str) -> str:
        """
        Drafts the final prenuptial agreement based on the original agreement.

        :param agreement: The original agreement.
        :return: The final prenuptial agreement.
        """
        return self.generate_output(agreement=agreement).text()
