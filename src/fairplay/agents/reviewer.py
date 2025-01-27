from fairplay.agents.base_agent import Agent
from fairplay.models import Risks


PROMPT = r"""
You are an AI representative who has been specifically assigned the important and significant task of considering and prioritizing the interests of {name} within the context of the specified scenario that has been presented to you. In this particular situation, your primary responsibility is to ensure that you thoroughly concern yourself with {name}'s interests and that you can raise every possible situation that may pertain to {name}'s interests.

Your response should be formatted in point form, with each point describing a possible future risk that {name} might be taking. Additionally, please rate each risk using an evaluation from a scale of 1-5 regarding how much {name}'s interest is at stake in this particular situation.

Current clauses: {clauses}
"""

class Reviewer(Agent):
    """
    An agent specialized in generating risk scenarios.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["name", "scenario"],
            output_model=Risks,
        )

    def generate_risks(self, name: str, clauses: str) -> Risks:
        """
        Generates risks given a name and scenario.

        :param name: The name/key associated with the risk generation context.
        :param clauses: The current clauses or terms to be considered.
        :return: A structured output conforming to the `Risks` Pydantic model.
        """
        return self.generate_output(name=name, clauses=clauses).risks
