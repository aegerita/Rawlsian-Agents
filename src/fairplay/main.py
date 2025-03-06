#%%
from fairplay.agents.arbitrator import Arbitrator
from fairplay.agents.drafter import Drafter
from fairplay.agents.reviewer import Reviewer
from argparse import ArgumentParser

#%%
parser = ArgumentParser()
parser.add_argument("-fp", "--folder_path", default="src/docs/LeVan vs LeVan/", dest="folder_path", help="Folder path for relevant documents.")

args = parser.parse_args()
folder_path = args.folder_path
input_file = "initial_agreement.md"
output_file = "final_agreement.md"

with open(folder_path + input_file, "r") as file:
    initial_agreement = file.read()

#%%
reviewer = Reviewer()
risks_A = reviewer.generate_risks(name="Husband", claims=initial_agreement)
risks_B = reviewer.generate_risks(name="Wife", claims=initial_agreement)
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
#%%
print("\n")
for edit in edits:
    print(edit)

#%%
drafter = Drafter()
final_agreement = drafter.draft_agreement(agreement=initial_agreement, edits=edits)
print("\nFinal agreement:")
print(final_agreement)

# %%

with open(folder_path + output_file, 'w') as file:
    file.write(final_agreement)