from rawlsian_agents.agents.base_agent import Agent
from rawlsian_agents.models import Arbitration

PROMPT = r"""
You have a detailed prenuptial agreement outlining specific terms and conditions agreed upon by both parties. One party has raised concerns about a potential future risk that could significantly affect both individuals. Your task is to comprehensively assess this risk, explicitly evaluating whether the agreement remains conscionable, and if necessary, suggest precise strategies or edits to existing clauses to mitigate it.

Power imbalances in prenuptial agreements may result from factors such as financial disparities, emotional leverage, legal knowledge gaps, or external pressures from family or social expectations. Evaluate how these factors might affect the fairness, ethical integrity, and conscionability of the agreement over time.

Conduct a balanced analysis from multiple perspectives:

- **Legal & Financial**: Identify if disparities in financial knowledge, transparency, or access to legal counsel have created or could create unfair advantages or unconscionable circumstances.
- **Emotional & Psychological**: Evaluate the potential impact of emotional coercion, implicit pressure, or fears influencing decision-making processes and assess if vulnerabilities have been exploited.
- **Social & External Influences**: Consider whether family expectations, cultural norms, or social pressures could amplify power imbalances, unfairness, or unconscionability.
- **Adaptive Solutions**: Suggest ways the agreement can remain fair, conscionable, and flexible under changing circumstances (e.g., financial shifts, legal loopholes, or significant life events).

For each identified risk, propose a specific and concise single-sentence edit to existing contractual clauses or safeguards that will help prevent power imbalances, promote fairness, ensure ethical negotiation, and maintain conscionability. Clearly describe counterfactual scenarios if relevant, such as the impact of refusal to mediate, exploitation of financial disclosure, or challenges to the fairness and conscionability of the agreement.

Your response must reflect John Rawls' principle of the "veil of ignorance," ensuring fairness regardless of either party's future status. If a risk is already sufficiently covered by existing clauses, explicitly state that no additional edits are necessary.

Current claims for the prenuptial agreement:
{claims}

Identified risk:
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
