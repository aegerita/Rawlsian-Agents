# %%
import os
from rawlsian_agents.agents.arbitrator import Arbitrator
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.agents.reviewer import Reviewer
from rawlsian_agents.utils.prenup_templates import PRENUP_TEMPLATE
from evaluate import load
import json

def run_gender_bias_experiment(run_num: int = 1) -> dict:
    """Run a single iteration of the gender bias experiment and return scores"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(script_dir, "gender_bias_inputs/")
    OUTPUT_DIR = os.path.join(script_dir, "gender_bias_outputs/")
    
    input_files = os.listdir(INPUT_DIR)

    for input_file in input_files:
        with open(INPUT_DIR + input_file, "r") as file:
            free_text = file.read()
        claims_processor = ClaimsProcessor()
        claims_processor.load_free_text(free_text)
        claims = claims_processor.process_claims()

        basic_drafter = BasicDrafter()
        initial_agreement = basic_drafter.draft_agreement(PRENUP_TEMPLATE, claims)
        
        reviewer = Reviewer()
        risks_A = reviewer.generate_risks(name="Partner 1", claims=initial_agreement)
        risks_B = reviewer.generate_risks(name="Partner 2", claims=initial_agreement)
        combined_risks = risks_A + risks_B

        edits = ["Proposed edits to the agreement:"]
        arbitrator = Arbitrator()
        suffix = input_file.split("__")[-1].replace(".txt", "") + f"__run_{run_num}"
        with open(OUTPUT_DIR + f"risks_and_mitigations__{suffix}.md", "w") as file:
            for risk in combined_risks:
                file.write(f"{risk}\n")
                arbitration = arbitrator.propose_clause(claims=initial_agreement, risk=risk)
                edits.append(arbitration.edit)
                file.write(f"Arbitrator's POV:\n {arbitration}\n\n")

    bertscore = load("bertscore")
    risks_and_mitigations_dict = {}
    # Use absolute path for the reference file
    reference_file = os.path.join(script_dir, "../../src/docs/LeVan vs LeVan/risks_and_mitigations.md")
    with open(reference_file, "r") as file:
        risks_and_mitigations_dict["original"] = file.read()
    suffixes = []
    for input_file in input_files:
        suffix = input_file.split("__")[-1].replace(".txt", "") + f"__run_{run_num}"
        suffixes.append(suffix)
        with open(OUTPUT_DIR + f"risks_and_mitigations__{suffix}.md", "r") as file:
            risks_and_mitigations_dict[suffix] = file.read()

    scores = {}
    for suffix in suffixes:
        scores[suffix] = bertscore.compute(
            predictions=[risks_and_mitigations_dict["original"]],
            references=[risks_and_mitigations_dict[suffix]],
            lang="en",
        )["f1"][0]

    return scores

# %%
# Original script execution (when run directly)
if __name__ == "__main__":
    scores = run_gender_bias_experiment()
    OUTPUT_DIR = "./gender_bias_outputs/"
    with open(OUTPUT_DIR + "scores.json", "w") as file:
        json.dump(scores, file)
