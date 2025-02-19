from fairplay.agents.base_agent import Agent
from fairplay.models import Claims

PROMPT = r"""
Provide a structured case summary with a focus on the original provisions of the prenuptial agreement. Organize the output into the following sections:

\#\#\# Key Terms of Original Prenuptial Agreement
- List and summarize the primary provisions of the original prenuptial agreement as agreed upon by both parties prior to the marriage, detailing the essential financial and legal protections specified in the contract.
- Use clear bullet points to outline each clause, ensuring they reflect the intentions of both parties without any influence from subsequent court rulings.
- Include any particular conditions concerning property division, spousal support, and debt responsibilities.
- Ensure the bullet points reflect the essential elements of a prenuptial agreement, including clauses related to property division, spousal support, and any other relevant provisions.

\#\#\# Legal Issues Identified
- Explain why the agreement was contested in court, providing context for the disagreement.
- Identify any misrepresentations, non-disclosures, or unjust provisions that were noted in the case.

\#\#\# Court’s Findings and Decision
- Summarize the trial court's ruling on the validity and enforceability of the agreement.
- Detail how the appellate court ruled on the appeal, including any modifications made to the initial ruling.
- Include relevant legal principles and how they were applied in this case.

Ensure the output adheres to a structured, professional case summary format with bolded section headings, bullet points, and concise legal analysis. Aim for clarity and precision in your summaries to enhance understanding of the case's implications.

"""


class Case_Processor(Agent):
    """
    An agent specialized in analyzing and proposing claims for identified risks.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["case_file"],
        )

    def summarize_case(self, file_name: str) -> str:
        """
        Summarizes the case file into initial terms, legal issues, and court findings.
        """
        with open(file_name, 'r') as file:
            case_file = file.read()
        return self.generate_output(case_file=case_file)
