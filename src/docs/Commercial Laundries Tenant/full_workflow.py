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
You are legal assistant assigned to analyze and prioritize the interests of {name}, a corporation. Your primary responsibility is to identify and evaluate potential future risks that could impact {name} under the terms of the agreement, explicitly assessing whether the agreement is conscionable.

Consider both immediate and long-term risks, including financial, legal, and business factors. Assess how external influences, such as economic downturns, contract clarity, or legal loopholes, could affect the agreement. Determine if any power imbalances exist or if certain clauses disproportionately benefit one party. Where relevant, suggest ways to rebalance the agreement to promote fairness.

For each identified risk, explore a counterfactual scenario by considering how the situation might change under different conditions, such as one company experiencing  financial distress, business challenges, or legislative developments that could alter the effectiveness or fairness of the agreement. If applicable, propose specific strategies or alternative negotiation terms that could mitigate risks. Address concerns by editing and updating existing clauses rather than adding new ones.

Ensure your response is clear, structured, and provides a comprehensive and balanced assessment of potential risks and issues relevant to {name}. If the agreement already sufficiently addresses all concerns, indicate clearly that no additional risks or changes are necessary.

Keep in mind that you are representing a corporation, and your analysis should reflect the interests and conditions of a corporate entity.

Current claims: {claims}
"""
#%%
folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"
output_file = "final_agreement.md"

# %%
with open(folder_path + "initial_agreement.md", "r") as file:
    initial_agreement = file.read()
#%%
reviewer = Reviewer()
reviewer.prompt_template = COMMERCIAL_LEASE_PROMPT
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
