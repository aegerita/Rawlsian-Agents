#!/usr/bin/env python3
"""
Gender Bias Experiment Runner - 100 iterations (Parallel)
Runs the gender bias experiment in parallel to speed up execution
"""

import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from gender_bias import run_gender_bias_experiment

def run_single_experiment(run_num):
    """Run a single experiment and return the result with run number"""
    try:
        scores = run_gender_bias_experiment(run_num)
        return run_num, scores
    except Exception as e:
        print(f"Error in run {run_num}: {e}")
        return run_num, None

def main():
    # Configuration
    num_runs = 81  # Start with just 5 runs to test
    max_workers = 3  # Use only 1 worker initially to test CSV writing
    csv_filename = "./gender_bias_outputs/gender_bias_results.csv"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filepath = os.path.join(script_dir, csv_filename)

    print(f"Starting {num_runs} runs of gender bias experiment with {max_workers} parallel workers...")
    print(f"Results will be saved to: {csv_filename}")
    
    # Run experiments in parallel and write results immediately
    completed_count = 0
    with open(csv_filepath, 'a', newline='') as csvfile:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            futures = [executor.submit(run_single_experiment, i+1) for i in range(19, 100)]
            
            # Collect and write results as they complete
            for future in as_completed(futures):
                run_num, scores = future.result()
                if scores is not None:
                    # Write scores to CSV
                    writer = csv.DictWriter(csvfile, fieldnames=scores.keys())
                    writer.writerow(scores)
                    completed_count += 1
                    print(f"Run {run_num} completed and saved ({completed_count}/{num_runs}) with scores: {scores}")
    
    print(f"\nCompleted! {completed_count} successful runs saved to {csv_filename}")

if __name__ == "__main__":
    main()
