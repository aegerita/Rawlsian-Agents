#!/usr/bin/env python3
"""
Gender Bias Experiment Runner - 100 iterations
Runs the gender bias experiment 100 times and saves results to CSV
"""

import csv
import os
from gender_bias import run_gender_bias_experiment

def main():
    # Configuration
    num_runs = 98
    csv_filename = "./gender_bias_outputs/gender_bias_results.csv"
    
    print(f"Starting {num_runs} runs of gender bias experiment...")
    print(f"Results will be saved to: {csv_filename}")
    
    # Since CSV already has data, just append new rows
    fieldnames = ['man_man', 'man_woman', 'woman_man', 'woman_woman']
    
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Run all iterations
        for run_num in range(num_runs):
            try:
                scores = run_gender_bias_experiment()
                print(f"Run {run_num + 1}/{num_runs} scores: {scores}")
                writer.writerow(scores)
                csvfile.flush()  # Ensure data is written immediately
                
            except Exception as e:
                print(f"Error in run {run_num}: {e}")
                print("Continuing with next run...")
                continue
    
    print(f"\nCompleted! Results saved to {csv_filename}")
    print(f"You can now analyze the data with pandas, Excel, or any CSV reader.")

if __name__ == "__main__":
    main()
