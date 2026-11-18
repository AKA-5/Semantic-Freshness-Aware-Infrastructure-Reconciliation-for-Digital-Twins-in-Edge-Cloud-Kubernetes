import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# Set a clean, academic style
plt.style.use('ggplot')

# --- PLOT 1: Standalone Mathematical Simulation ---
df = pd.read_csv("results/preliminary_results.csv")
colors = ['#7f8c8d', '#e74c3c', '#3498db'] # Grey, Red, Blue

# Plot Reconciliations
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df['Policy'], df['Reconciliations'], color=colors, width=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontweight='bold')
ax.set_title('Phase 1: Reconciliations (Standalone Math Model)', fontsize=14, fontweight='bold')
ax.set_ylabel('Reconciliation Count', fontsize=12)
ax.set_xlabel('Policy', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("results/plot_reconciliations.png", dpi=300)
plt.close()

# Plot Overhead
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df['Policy'], df['Total Overhead'], color=colors, width=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha='center', va='bottom', fontweight='bold')
ax.set_title('Phase 1: Total Operational Overhead (Standalone Math Model)', fontsize=14, fontweight='bold')
ax.set_ylabel('Overhead (Arbitrary Units)', fontsize=12)
ax.set_xlabel('Policy', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("results/plot_overhead.png", dpi=300)
plt.close()

# --- PLOT 2: EdgeSimPy Real Dataset Simulation ---
# We record the actual EdgeSimPy output here
edgesimpy_data = {
    'Metric': ['Total Evaluations', 'Reconciliations (Migrations)'],
    'Count': [20, 10]
}
df_edge = pd.DataFrame(edgesimpy_data)

fig, ax = plt.subplots(figsize=(6, 5))
colors_edge = ['#2ecc71', '#9b59b6'] # Green, Purple
bars = ax.bar(df_edge['Metric'], df_edge['Count'], color=colors_edge, width=0.5)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontweight='bold')
ax.set_title('Phase 2: EdgeSimPy Integration (100 Ticks)', fontsize=14, fontweight='bold')
ax.set_ylabel('Count', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
ax.set_ylim(0, 25) # Gives extra room at the top
plt.savefig("results/plot_edgesimpy.png", dpi=300)
plt.close()

print("All 3 plots successfully saved to results/ folder.")