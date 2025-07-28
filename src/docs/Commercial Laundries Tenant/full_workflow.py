#%%
import os
from rawlsian_agents.agents.arbitrator import Arbitrator
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.agents.drafter import Drafter
from rawlsian_agents.agents.reviewer import Reviewer
from rawlsian_agents.utils.commercial_lease_templates import BC_LEASE_TEMPLATE

# %%
### voy aqui
COMMERCIAL_LEASE_PROMPT = r"""
You are an AI representative assigned to analyze and prioritize the interests of {name} in the given scenario. Your primary responsibility is to identify and evaluate potential future risks that could impact {name} under the terms of the agreement, explicitly assessing whether the agreement is conscionable.

Consider both immediate and long-term risks, including financial, emotional, legal, and social factors. Assess how external influences, such as economic downturns, job loss, family expectations, or legal loopholes, could affect the agreement. Specifically evaluate whether any vulnerabilities—such as intellectual, economic, situational, emotional stress, or relationships of trust—were present and exploited during the negotiation process. Determine if any power imbalances exist or if certain clauses disproportionately benefit one party, raising concerns of unconscionability. Where relevant, suggest ways to rebalance the agreement to promote fairness.

For each identified risk or potential unconscionability, explore a counterfactual scenario by considering how the situation might change under different conditions, such as one party experiencing significant financial changes, unexpected health challenges, or legislative developments that could alter the effectiveness or fairness of the agreement. If applicable, propose specific strategies or alternative negotiation terms that could mitigate risks and address unconscionability concerns, preferably by editing and updating existing clauses rather than adding new ones.

Ensure your response is clear, structured, and provides a comprehensive and balanced assessment of potential risks and conscionability issues relevant to {name}. If the agreement already sufficiently addresses all concerns and is conscionable, indicate clearly that no additional risks or changes are necessary.

Current claims: {claims}
"""
#%%
folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"
input_file = "initial_conditions.txt"
output_file = "final_agreement.md"

# %%
with open(folder_path + input_file, "r") as file:
    free_text = file.read()

# %%
claims_processor = ClaimsProcessor()
claims_processor.load_free_text(free_text)
claims = claims_processor.process_claims()
print(claims)

with open(folder_path + "recovered_claims.txt", "w") as file:
    file.write(str(claims))

# %%
with open(folder_path + "initial_agreement.md", "r") as file:
    initial_agreement = file.read()
#%%
reviewer = Reviewer()
risks_A = reviewer.generate_risks(name="Partner 1", claims=initial_agreement)
risks_B = reviewer.generate_risks(name="Partner 2", claims=initial_agreement)
combined_risks = risks_A + risks_B

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
