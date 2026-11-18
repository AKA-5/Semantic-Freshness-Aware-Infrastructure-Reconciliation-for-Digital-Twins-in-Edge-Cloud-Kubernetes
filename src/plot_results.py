import pandas as pd
import matplotlib.pyplot as plt

# Load the results
df = pd.read_csv("results/preliminary_results.csv")

# Set a clean, academic style
plt.style.use('ggplot')

# --- Plot 1: Reconciliations ---
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#7f8c8d', '#e74c3c', '#3498db'] # Grey, Red, Blue
bars = ax.bar(df['Policy'], df['Reconciliations'], color=colors, width=0.6)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontweight='bold')

ax.set_title('Number of Reconciliations by Policy', fontsize=14, fontweight='bold')
ax.set_ylabel('Reconciliation Count', fontsize=12)
ax.set_xlabel('Policy', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("results/plot_reconciliations.png", dpi=300)
plt.close()

# --- Plot 2: Total Overhead ---
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df['Policy'], df['Total Overhead'], color=colors, width=0.6)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha='center', va='bottom', fontweight='bold')

ax.set_title('Total Operational Overhead by Policy', fontsize=14, fontweight='bold')
ax.set_ylabel('Overhead (Arbitrary Units)', fontsize=12)
ax.set_xlabel('Policy', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("results/plot_overhead.png", dpi=300)
plt.close()

print("Plots successfully saved to results/ folder.")