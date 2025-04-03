#%%
from fairplay.agents.arbitrator import Arbitrator
from fairplay.agents.basic_drafter import BasicDrafter
from fairplay.agents.claims_processor import ClaimsProcessor
from fairplay.agents.drafter import Drafter
from fairplay.agents.reviewer import Reviewer
from fairplay.utils.prenup_templates import PRENUP_TEMPLATE
from argparse import ArgumentParser

#%%
parser = ArgumentParser()
parser.add_argument("-fp", "--folder_path", default="src/docs/LeVan vs LeVan/", dest="folder_path", help="Folder path for relevant documents.")

args = parser.parse_args()
folder_path = args.folder_path
input_file = "initial_conditions_free_text.txt"
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
basic_drafter = BasicDrafter()
initial_agreement = basic_drafter.draft_agreement(PRENUP_TEMPLATE, claims)
print(initial_agreement)

with open(folder_path + "initial_agreement.md", 'w') as file:
    file.write(initial_agreement)

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
