from rawlsian_agents.agents.base_agent import Agent
from rawlsian_agents.models import Arbitration
from rawlsian_agents.utils.prompts import PRENUPTIAL_PROMPT_CATALOGUE


class Arbitrator(Agent):
    """
    An agent specialized in analyzing and proposing claims for identified risks.
    """
    def __init__(self, prompt_catalogue: dict = PRENUPTIAL_PROMPT_CATALOGUE) -> None:
        super().__init__(
            prompt_template=prompt_catalogue["arbitrator"],
            input_variables=["claims", "risk"],
            output_model=Arbitration,
        )

    def propose_clause(self, claims: str, risk: str) -> Arbitration:
        """
        Analyzes risks and proposes claims given existing claims and a risk.

        :param claims: The claims or terms to be considered or enhanced.
        :param risk: The specific risk scenario to analyze.
        :return: A structured output conforming to the `CLAIMS` Pydantic model.
        """
        return self.generate_output(claims=claims, risk=risk)
