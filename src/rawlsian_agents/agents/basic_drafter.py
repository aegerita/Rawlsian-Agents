from rawlsian_agents.agents.base_agent import Agent
from rawlsian_agents.utils.prompts import PRENUPTIAL_PROMPT_CATALOGUE

class BasicDrafter(Agent):
    """
    A non rawlsian agent who takes claims and free text as input and drafts a contract based on a template.
    """
    def __init__(self, prompt_catalogue: dict = PRENUPTIAL_PROMPT_CATALOGUE) -> None:
        super().__init__(
            prompt_template=prompt_catalogue["basic_drafter"],
            input_variables=["template", "claims"],
        )

    def draft_agreement(self, template: str, claims: list[str]) -> str:
        """
        Drafts the final prenuptial agreement based on the claims and free text.

        :param template: The template to use for the prenuptial agreement.
        :param claims: The list of factual claims to include in the agreement.
        :return: The final prenuptial agreement.
        """
        return self.generate_output(template=template, claims=claims).text()
