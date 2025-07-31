"""This script processes a commercial lease agreement workflow, including claims processing, risk assessment, and drafting a final agreement. The initial stages were run in the `initial_draft.py` file, and this script continues from there."""
#%%
import os
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.agents.reviewer import Reviewer
from rawlsian_agents.agents.arbitrator import Arbitrator
from rawlsian_agents.agents.drafter import Drafter
from rawlsian_agents.utils.commercial_lease_templates import BC_LEASE_TEMPLATE
from rawlsian_agents.utils.prompts import COMMERCIAL_LEASE_PROMPT_CATALOGUE

# %%
folder_path = os.path.dirname(os.path.abspath(__file__))

# %%
bd = BasicDrafter(COMMERCIAL_LEASE_PROMPT_CATALOGUE)
# %%
with open(f"{folder_path}/initial_conditions.txt", "r") as file:
    free_text = file.read()

# %%
cp = ClaimsProcessor(COMMERCIAL_LEASE_PROMPT_CATALOGUE)
cp.load_free_text(free_text)
claims = cp.process_claims()
print(claims)

with open(f"{folder_path}/recovered_claims.txt", "w") as file:
    file.write(str(claims))

# %%
draft = bd.draft_agreement(BC_LEASE_TEMPLATE, claims)
print(draft)

with open(f"{folder_path}/initial_agreement.md", 'w') as file:
    file.write(draft)

# %%
with open(folder_path + "initial_agreement.md", "r") as file:
    initial_agreement = file.read()
#%%
reviewer = Reviewer(COMMERCIAL_LEASE_PROMPT_CATALOGUE)
risks_landlord = reviewer.generate_risks(name="landlord", claims=initial_agreement)
risks_tenant = reviewer.generate_risks(name="tenant", claims=initial_agreement)
combined_risks = risks_landlord + risks_tenant

if not os.path.exists(folder_path + "combined_risks.md"):
    with open(folder_path + "combined_risks.md", "w") as file:
        file.write("## Combined Risks Identified\n")
        for risk in combined_risks:
            file.write(f"{risk}\n\n")
else:
    with open(folder_path + "combined_risks.md", "r") as file:
        combined_risks = file.read().split("\n\n")

#%%
edits = ["Proposed edits to the agreement:"]
arbitrator = Arbitrator(COMMERCIAL_LEASE_PROMPT_CATALOGUE)
print("Arbitrator's analysis of risks and proposed edits:")
print("\n")
if not os.path.exists(folder_path + "risks_and_mitigations.md"):
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
else:
    with open(folder_path + "risks_and_mitigations.md", "r") as file:
        risks_and_mitigations = file.read().split("\n\n")
    for risk in risks_and_mitigations:
        print(risk)
        arbitration = arbitrator.propose_clause(claims=initial_agreement, risk=risk)
        print(arbitration)
        edits.append(arbitration.edit)
#%%
drafter = Drafter(COMMERCIAL_LEASE_PROMPT_CATALOGUE)
final_agreement = drafter.draft_agreement(agreement=initial_agreement, edits=edits)
print("\nFinal agreement:")
print(final_agreement)
with open(folder_path + "final_agreement.md", 'w') as file:
    file.write(final_agreement)