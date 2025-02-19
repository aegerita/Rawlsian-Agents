from fairplay.agents.base_agent import Agent
from fairplay.models import Claims

PROMPT = r"""
You have a detailed prenuptial agreement that outlines the specific terms and conditions both parties have agreed upon. One of the clients has raised a concern about a potential future risk that could have serious implications for both individuals. If necessary, suggest adding specific claims to the agreement that address this identified risk and help prevent any negative consequences. It is essential not to repeat any claims that are already included in the agreement or to introduce any redundant claims. In the case that the risk is sufficiently resolved by the agreement, return nothing in the list of claims. Be clear and concise in your language to ensure understanding. 

You should analyze this situation using John Rawls' concept of the "veil of ignorance," which highlights the importance of fairness and an unbiased perspective in decision-making. It is vital to thoroughly assess ethical considerations to ensure that the proposed solution benefits both clients involved in this prenuptial agreement.

Current claims for the prenuptial agreement:
{claims}

The identified risk:
{risk}
"""


class Arbitrator(Agent):
    """
    An agent specialized in analyzing and proposing claims for identified risks.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["claims", "risk"],
            output_model=Claims,
        )

    def propose_clause(self, claims: str, risk: str) -> Claims:
        """
        Analyzes risks and proposes claims given existing claims and a risk.

        :param claims: The claims or terms to be considered or enhanced.
        :param risk: The specific risk scenario to analyze.
        :return: A structured output conforming to the `CLAIMS` Pydantic model.
        """
        return self.generate_output(claims=claims, risk=risk).claims
