"""This script processes a commercial lease agreement workflow, including claims processing, risk assessment, and drafting a final agreement. The initial stages were run in the `initial_draft.py` file, and this script continues from there."""
#%%
import os
from rawlsian_agents.agents.arbitrator import Arbitrator
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.agents.drafter import Drafter
from rawlsian_agents.agents.reviewer import Reviewer
from rawlsian_agents.utils.commercial_lease_templates import BC_LEASE_TEMPLATE

# %%
COMMERCIAL_LEASE_PROMPT = r"""
You are legal assistant assigned to analyze and prioritize the interests of {name}, a corporation. Your primary responsibility is to identify and evaluate potential future risks that could impact {name} under the terms of the agreement, explicitly assessing whether the agreement is conscionable and all conditions are clearly defined.

Consider both immediate and long-term risks, including financial, legal, and business factors. Assess how external influences, such as economic downturns, contract ambiguity, undefined terms and procedures, or legal loopholes, could affect the agreement. Determine if any power imbalances exist or if certain clauses disproportionately benefit one party. Where relevant, suggest ways to rebalance the agreement to promote fairness.

For each identified risk, explore a counterfactual scenario by considering how the situation might change under different conditions, such as one company experiencing  financial distress, business challenges, or legislative developments that could alter the effectiveness or fairness of the agreement. If applicable, propose specific strategies or alternative negotiation terms that could mitigate risks. Address concerns by editing and updating existing clauses rather than adding new ones.

Ensure your response is clear, structured, and provides a comprehensive and balanced assessment of potential risks and issues relevant to {name}. If the agreement already sufficiently addresses all concerns, indicate clearly that no additional risks or changes are necessary.

Keep in mind that you are representing a corporation, and your analysis should reflect the interests and conditions of a corporate entity.

Current claims: {claims}
"""

COMMERCIAL_LEASE_ARBITRATOR_PROMPT = r"""
You have a detailed commercial lease agreement outlining specific terms and conditions. Each party has raised their concerns about a potential future risk that could significantly affect both individuals. Your task is to comprehensively assess this risk, explicitly evaluating whether the agreement remains conscionable, clear, and if necessary, suggest precise strategies or edits to existing clauses to mitigate it.

Power imbalances in commercial lease agreements may result from factors such as financial disparities, legal knowledge gaps, or outdated regulation. Evaluate how these factors might affect the fairness, ethical integrity, and conscionability of the agreement over time.

Conduct a balanced analysis from multiple perspectives:

- **Legal & Financial**: Identify if disparities in financial knowledge, transparency, or access to legal counsel have created or could create unfair advantages or unconscionable circumstances.
- **Adaptive Solutions**: Suggest ways the agreement can remain fair, conscionable, and flexible under changing circumstances (e.g., financial shifts, legal loopholes, undetermined procedures, ambiguity or significant natural events).

For each identified risk, propose a specific and concise single-sentence edit to existing contractual clauses or safeguards that will help prevent power imbalances, promote fairness, ensure ethical negotiation, and maintain conscionability. Clearly describe counterfactual scenarios if relevant, such as the impact of refusal to mediate, exploitation of financial disclosure, or challenges to the fairness and conscionability of the agreement.

Your response must reflect John Rawls' principle of the "veil of ignorance," ensuring fairness regardless of either party's future status. If a risk is already sufficiently covered by existing clauses, explicitly state that no additional edits are necessary.

Current claims for the commercial lease agreement:
{claims}

Identified risk:
{risk}
"""

#%%
folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"
output_file = "final_agreement.md"

# %%
with open(folder_path + "initial_agreement.md", "r") as file:
    initial_agreement = file.read()
#%%
reviewer = Reviewer()
reviewer.set_prompt(
    COMMERCIAL_LEASE_PROMPT,
    reviewer.input_variables,
    reviewer.partial_variables,
)
reviewer.set_chain()
risks_landlord = reviewer.generate_risks(name="landlord", claims=initial_agreement)
risks_tenant = reviewer.generate_risks(name="tenant", claims=initial_agreement)
combined_risks = risks_landlord + risks_tenant

with open(folder_path + "combined_risks.md", "w") as file:
    file.write("## Combined Risks Identified\n")
    for risk in combined_risks:
        file.write(f"{risk}\n\n")

#%%
edits = ["Proposed edits to the agreement:"]
arbitrator = Arbitrator()
arbitrator.set_prompt(
    COMMERCIAL_LEASE_ARBITRATOR_PROMPT,
    arbitrator.input_variables,
    arbitrator.partial_variables,
)
arbitrator.set_chain()
print("Arbitrator's analysis of risks and proposed edits:")
print("\n")
with open(folder_path + "risks_and_mitigations.md", "w") as file:
    for risk in combined_risks:
        print(risk)
        file.write(f"{risk}\n")
        arbitration = arbitrator.propose_clause(claims=initial_agreement, risk=risk)
        print(arbitration)
        edits.append(arbitration.edit)
        file.write(f"Arbitrator's POV:\n {arbitration}\n\n")
print("\n")
for edit in edits:
    print(edit)

#%%
drafter = Drafter()
final_agreement = drafter.draft_agreement(agreement=initial_agreement, edits=edits)
print("\nFinal agreement:")
print(final_agreement)
with open(folder_path + output_file, 'w') as file:
    file.write(final_agreement)
