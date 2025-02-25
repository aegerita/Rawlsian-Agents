from fairplay.agents.base_agent import Agent
from fairplay.models import Risks


PROMPT = r"""
You are an AI representative assigned to analyze and prioritize the interests of {name} in the given scenario. Your primary responsibility is to identify and evaluate potential future risks that could impact {name} under the terms of the agreement. 

Consider both immediate and long-term risks, including financial, emotional, legal, and social factors. Assess how external influences, such as economic downturns, job loss, family expectations, or legal loopholes, could affect the agreement. Analyze whether any power imbalances exist in the negotiation process and determine if certain clauses disproportionately benefit one party. Where relevant, suggest ways to rebalance the agreement to promote fairness.

For each risk, explore a counterfactual scenario by considering how the situation might change under different conditions, such as one party experiencing a significant financial shift, unexpected health challenges, or legislative changes that could alter the effectiveness of the agreement. If applicable, propose strategies or alternative negotiation terms that could mitigate risks while maintaining fairness for both parties. Edit and update current clauses are prefered over adding new ones.

Ensure your response is clear, structured, and provides a well-rounded assessment of potential risks to {name}. If the agreement already sufficiently addresses all concerns, return no additional risks.

Current claims: {claims}
"""

class Reviewer(Agent):
    """
    An agent specialized in generating risk scenarios.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["name", "claims"],
            output_model=Risks,
        )

    def generate_risks(self, name: str, claims: str) -> Risks:
        """
        Generates risks given a name and scenario.

        :param name: The name/key associated with the risk generation context.
        :param claims: The current claims or terms to be considered.
        :return: A structured output conforming to the `Risks` Pydantic model.
        """
        return self.generate_output(name=name, claims=claims).risks
