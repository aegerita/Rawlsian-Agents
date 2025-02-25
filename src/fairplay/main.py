#%%
from fairplay.agents.arbitrator import Arbitrator
from fairplay.agents.drafter import Drafter
from fairplay.agents.reviewer import Reviewer


with open("src/docs/LeVan vs LeVan initial agreement.md", 'r') as file:
    case_file = file.read()

#%%
reviewer = Reviewer()
risks_A = reviewer.generate_risks(name="Husband", claims=case_file)
risks_B = reviewer.generate_risks(name="Wife", claims=case_file)
combined_risks = risks_A + risks_B

#%%
edits = ["Proposed edits to the agreement:"]
arbitrator = Arbitrator()
for risk in combined_risks:
    print(risk)
    arbitration = arbitrator.propose_clause(claims=case_file, risk=risk)
    print(arbitration)
    edits.append(arbitration.edit)
    
#%%
print("\n")
for edit in edits:
    print(edit)

#%%
drafter = Drafter()
final_agreement = drafter.draft_agreement(agreement=case_file, edits=edits)
print("\nFinal agreement:")
print(final_agreement)

# %%

with open("../docs/LeVan vs LeVan final agreement.md", 'w') as file:
    file.write(final_agreement)

# %%
