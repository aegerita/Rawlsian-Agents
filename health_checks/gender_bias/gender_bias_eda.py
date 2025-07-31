import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy import stats  # Add this import for KS test

# Configure matplotlib to use T1 fonts for PDF compatibility
plt.rcParams['pdf.fonttype'] = 42  # Use T1 fonts instead of Type 3
plt.rcParams['ps.fonttype'] = 42   # Also for PostScript
plt.rcParams['font.family'] = 'serif'  # Use serif fonts (similar to LaTeX default)
plt.rcParams['font.serif'] = ['Computer Modern Roman', 'Times New Roman', 'DejaVu Serif']

# Read the CSV data
df = pd.read_csv('health_checks/gender_bias/gender_bias_outputs/gender_bias_results.csv')

# Debug: Check data
print("Data shape:", df.shape)
print("Column names:", df.columns.tolist())
print("Data range:", df.min().min(), "to", df.max().max())

# FIRST PLOT: CDF Analysis with KS tests
plt.figure(figsize=(14, 8))  # Slightly wider to accommodate KS test table

# Define colors - solid colors for lines
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
line_styles = ['-', '--', '-.', ':']
labels = []

# Extract column names and create labels
for i, col in enumerate(df.columns):
    parts = col.split('_')
    wealthy_party = parts[0]
    underprivileged_party = parts[1]
    labels.append(f'Wealthy Party (WP): {wealthy_party}, Underprivileged Party (UP): {underprivileged_party}')

    # Sort the data for CDF
    sorted_data = np.sort(df[col])
    # Create y-values: percentile ranks from 0 to 1
    y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    # Plot CDF
    plt.plot(sorted_data, y_values, color=colors[i], linewidth=2.5, 
             linestyle=line_styles[i], label=labels[i])

# Customize the plot
plt.xlabel('Score Values', fontsize=12, fontweight='bold')
plt.ylabel('Cumulative Probability', fontsize=12, fontweight='bold')
plt.title('Gender Bias Results - Cumulative Distribution Functions by Party Combinations', 
          fontsize=14, fontweight='bold', pad=20)

# Add legend inside the plot area
plt.legend(loc='lower right', fontsize=9, frameon=True, fancybox=True, shadow=True)

# Add grid for better readability
plt.grid(True, alpha=0.3, linestyle='--')

# Set axis limits
plt.xlim(df.min().min() - 0.01, df.max().max() + 0.01)
plt.ylim(0, 1)

# Add horizontal lines at key percentiles for reference
plt.axhline(y=0.25, color='gray', linestyle=':', alpha=0.5, linewidth=1)
plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, linewidth=1)
plt.axhline(y=0.75, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# Create statistics table
table_data = []
for i, col in enumerate(df.columns):
    parts = col.split('_')
    wealthy = parts[0]
    underprivileged = parts[1]
    median = df[col].median()
    std = df[col].std()
    table_data.append([f'WP: {wealthy}, UP: {underprivileged}', f'{median:.4f}', f'{std:.4f}'])

# Add table to the plot
table = plt.table(cellText=table_data,
                 colLabels=['Party Combination', 'Median', 'Std Dev'],
                 cellLoc='center',
                 loc='upper left',
                 bbox=[0.02, 0.7, 0.35, 0.25])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.2)

# Color the table cells to match the line colors
for i in range(len(table_data)):
    table[(i+1, 0)].set_facecolor(colors[i])
    table[(i+1, 0)].set_alpha(0.3)

# Style header row
for j in range(3):
    table[(0, j)].set_facecolor('#f0f0f0')
    table[(0, j)].set_text_props(weight='bold')

# KOLMOGOROV-SMIRNOV TESTS
print("\n" + "="*60)
print("KOLMOGOROV-SMIRNOV TESTS")
print("="*60)

# Perform pairwise KS tests
ks_results = []
col_names = df.columns.tolist()
# Shorter labels for better table formatting
col_labels = col_names.copy()

for i in range(len(col_names)):
    for j in range(i+1, len(col_names)):
        # Perform two-sample KS test
        ks_stat, p_value = stats.ks_2samp(df[col_names[i]], df[col_names[j]])
        
        # Determine significance
        significance = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
        
        ks_results.append([
            f'{col_labels[i]} vs {col_labels[j]}',
            f'{ks_stat:.4f}',
            f'{p_value:.6f}',
            significance
        ])
        
        print(f"{col_labels[i]} vs {col_labels[j]}: KS={ks_stat:.4f}, p={p_value:.6f} {significance}")

# Remove KS table from the main CDF plot - just save the CDF
plt.tight_layout()

# Save CDF plot without KS table
output_path = Path('health_checks/gender_bias/gender_bias_outputs/gender_bias_cdf.png')
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')

pdf_path = Path('health_checks/gender_bias/gender_bias_outputs/gender_bias_cdf.pdf')
plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white', format='pdf')

eps_path = Path('health_checks/gender_bias/gender_bias_outputs/gender_bias_cdf.eps')
plt.savefig(eps_path, dpi=300, bbox_inches='tight', facecolor='white', format='eps')

plt.show()

# CREATE SEPARATE KS TEST RESULTS TABLE
fig_ks, ax_ks = plt.subplots(figsize=(10, 6))
ax_ks.axis('tight')
ax_ks.axis('off')

# Create the KS results table as a standalone figure
ks_table = ax_ks.table(cellText=ks_results,
                      colLabels=['Comparison', 'KS Statistic', 'p-value', 'Significance'],
                      cellLoc='center',
                      loc='center',
                      colWidths=[0.4, 0.2, 0.25, 0.25])

# Style the KS table
ks_table.auto_set_font_size(False)
ks_table.set_fontsize(12)
ks_table.scale(1.2, 2.0)  # Make table larger and taller

# Color code significance levels
for i, (_, _, p_val, sig) in enumerate(ks_results):
    if sig == '***':
        ks_table[(i+1, 3)].set_facecolor('#ffcccc')  # Light red for highly significant
    elif sig == '**':
        ks_table[(i+1, 3)].set_facecolor('#ffe6cc')  # Light orange for very significant
    elif sig == '*':
        ks_table[(i+1, 3)].set_facecolor('#ffffcc')  # Light yellow for significant
    else:
        ks_table[(i+1, 3)].set_facecolor('#f0f0f0')  # Light gray for non-significant

# Style KS table header
for j in range(4):
    ks_table[(0, j)].set_facecolor('#e0e0e0')
    ks_table[(0, j)].set_text_props(weight='bold', fontsize=14)

# Style all cells for better readability
for i in range(len(ks_results) + 1):
    for j in range(4):
        ks_table[(i, j)].set_edgecolor('black')
        ks_table[(i, j)].set_linewidth(1)

# Add title to the KS table
plt.title('Kolmogorov-Smirnov Test Results\nGender Bias Analysis', 
          fontsize=16, fontweight='bold', pad=20)

# Add significance legend
legend_text = ("Significance levels:\n"
               "*** p < 0.001 (highly significant)\n"
               "**  p < 0.01 (very significant)\n"
               "*   p < 0.05 (significant)\n"
               "ns  p ≥ 0.05 (not significant)")

plt.figtext(0.02, 0.02, legend_text, fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))

plt.tight_layout()

# Save KS table as separate files
ks_output_path = Path('health_checks/gender_bias/gender_bias_outputs/ks_test_results.png')
plt.savefig(ks_output_path, dpi=300, bbox_inches='tight', facecolor='white')

ks_pdf_path = Path('health_checks/gender_bias/gender_bias_outputs/ks_test_results.pdf')
plt.savefig(ks_pdf_path, dpi=300, bbox_inches='tight', facecolor='white', format='pdf')

ks_eps_path = Path('health_checks/gender_bias/gender_bias_outputs/ks_test_results.eps')
plt.savefig(ks_eps_path, dpi=300, bbox_inches='tight', facecolor='white', format='eps')

plt.show()

# SECOND PLOT: Standard Deviation Across Combinations per Experiment
print("\n" + "="*60)
print("CROSS-COMBINATION STANDARD DEVIATION ANALYSIS")
print("="*60)

# Calculate standard deviation across all combinations for each experiment (row)
cross_combination_stds = []
for index, row in df.iterrows():
    # Calculate std dev across the 4 combinations for this experiment
    std_across_combinations = row.std()
    cross_combination_stds.append(std_across_combinations)

# Convert to numpy array for easier handling
cross_combination_stds = np.array(cross_combination_stds)

# Create second figure for cross-combination standard deviation distribution
plt.figure(figsize=(10, 6))

# Create histogram with probabilities (density=False, weights to normalize)
weights = np.ones_like(cross_combination_stds) / len(cross_combination_stds)
plt.hist(cross_combination_stds, bins=25, weights=weights,
         edgecolor='#2E8B57', facecolor='none', linewidth=2.5, 
         histtype='stepfilled', label='Cross-Combination Standard Deviation')

# Customize the plot
plt.xlabel('Standard Deviation Across Gender Combinations', fontsize=12, fontweight='bold')
plt.ylabel('Probability', fontsize=12, fontweight='bold')
plt.title('Distribution of Standard Deviation Across Gender Combinations per Experiment', 
          fontsize=14, fontweight='bold', pad=20)

# Add legend
plt.legend(loc='upper right', fontsize=10, frameon=True, fancybox=True, shadow=True)

# Add grid for better readability
plt.grid(True, alpha=0.3, linestyle='--')

# Add statistics table for cross-combination analysis
cross_stats = {
    'Mean': np.mean(cross_combination_stds),
    'Median': np.median(cross_combination_stds),
    'Std Dev': np.std(cross_combination_stds),
    'Min': np.min(cross_combination_stds),
    'Max': np.max(cross_combination_stds)
}

# Create statistics table
stats_data = [[f'{value:.6f}'] for value in cross_stats.values()]
stats_table = plt.table(cellText=stats_data,
                       rowLabels=list(cross_stats.keys()),
                       colLabels=['Value'],
                       cellLoc='center',
                       loc='upper left',
                       bbox=[0.08, 0.65, 0.15, 0.30])

# Style the statistics table
stats_table.auto_set_font_size(False)
stats_table.set_fontsize(8)
stats_table.scale(1, 1.2)

# Style header
stats_table[(0, 0)].set_facecolor('#f0f0f0')
stats_table[(0, 0)].set_text_props(weight='bold')

# Color row labels
for i in range(1, len(cross_stats) + 1):
    stats_table[(i, -1)].set_facecolor('#e8f4f8')
    stats_table[(i, -1)].set_text_props(weight='bold')

plt.tight_layout()

# Save cross-combination standard deviation plot
output_path_cross = Path('health_checks/gender_bias/gender_bias_outputs/cross_combination_std.png')
plt.savefig(output_path_cross, dpi=300, bbox_inches='tight', facecolor='white')

pdf_path_cross = Path('health_checks/gender_bias/gender_bias_outputs/cross_combination_std.pdf')
plt.savefig(pdf_path_cross, dpi=300, bbox_inches='tight', facecolor='white', format='pdf')

eps_path_cross = Path('health_checks/gender_bias/gender_bias_outputs/cross_combination_std.eps')
plt.savefig(eps_path_cross, dpi=300, bbox_inches='tight', facecolor='white', format='eps')

plt.show()

# Print comprehensive statistics
print("Dataset Statistics:")
print(f"Total experiments: {len(df)}")
print(f"Total combinations per experiment: {len(df.columns)}")

print("\nMean scores by combination:")
for col in df.columns:
    print(f"{col}: {df[col].mean():.4f} (±{df[col].std():.4f})")

print("\nCross-combination standard deviation statistics:")
for key, value in cross_stats.items():
    print(f"{key}: {value:.6f}")

print(f"\nInterpretation:")
print(f"- Lower cross-combination std dev indicates more consistent scores across gender combinations")
print(f"- Higher cross-combination std dev indicates more bias/variation between gender combinations")
print(f"- Mean cross-combination std dev: {cross_stats['Mean']:.6f}")