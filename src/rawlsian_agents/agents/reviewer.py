from rawlsian_agents.agents.base_agent import Agent
from rawlsian_agents.models import Risks
from rawlsian_agents.utils.prompts import PRENUPTIAL_PROMPT_CATALOGUE


class Reviewer(Agent):
    """
    An agent specialized in generating risk scenarios.
    """
    def __init__(self, prompt_catalogue: dict = PRENUPTIAL_PROMPT_CATALOGUE) -> None:
        super().__init__(
            prompt_template=prompt_catalogue["reviewer"],
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
