import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create necessary directories if they don't exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("images", exist_ok=True)

# Load the CSV file
csv_file_path = "input/data_real.csv"
data = pd.read_csv(csv_file_path, delimiter=';')

# Combine all necessary data into a single output file
combined_data = data[['mouse_ID', 'treatment', 'experimental_day', 'counts_live_bacteria_per_wet_g',
                      'sample_type', 'mouse_sex']]
combined_output_path = os.path.join("output", "combined_data.csv")
combined_data.to_csv(combined_output_path, index=False)

# 1. Generate multi-line graph for fecal live bacteria over time
fecal_data = combined_data[combined_data['sample_type'] == 'fecal']

plt.figure(figsize=(10, 6))
colors = {"ABX": "orange", "placebo": "blue"}
for treatment in fecal_data['treatment'].unique():
    subset = fecal_data[fecal_data['treatment'] == treatment]
    for mouse_id in subset['mouse_ID'].unique():
        mouse_data = subset[subset['mouse_ID'] == mouse_id]
        plt.plot(mouse_data['experimental_day'], 
                 mouse_data['counts_live_bacteria_per_wet_g'], 
                 label=treatment if mouse_id == subset['mouse_ID'].unique()[0] else "",
                 color=colors[treatment], alpha=0.7)

plt.yscale("log")
plt.xlabel("Washout day")
plt.ylabel("log10(live bacteria/wet g)")
plt.title("Fecal live bacteria")
plt.legend(title="Treatment")
plt.grid(True)
plt.savefig("images/fecal_live_bacteria.png")
plt.close()

# Debug unique experimental_day values for cecal and ileal data
print("Unique experimental_day values for cecal samples:")
print(combined_data[combined_data['sample_type'] == 'cecal']['experimental_day'].unique())

print("Unique experimental_day values for ileal samples:")
print(combined_data[combined_data['sample_type'] == 'ileal']['experimental_day'].unique())

# 2. Generate violin plot for cecal live bacteria
cecal_data = combined_data[(combined_data['sample_type'] == 'cecal')]

if cecal_data.empty:
    print("No data available for cecal live bacteria plot.")
else:
    plt.figure(figsize=(8, 6))
    sns.violinplot(x='treatment', y='counts_live_bacteria_per_wet_g', data=cecal_data, palette={"ABX": "orange", "placebo": "blue"})
    plt.yscale("log")
    plt.xlabel("Treatment")
    plt.ylabel("log10(live bacteria/wet g)")
    plt.title("Cecal live bacteria")
    plt.savefig("images/cecal_live_bacteria.png")
    plt.close()

# 3. Generate violin plot for ileal live bacteria
ileal_data = combined_data[(combined_data['sample_type'] == 'ileal')]

if ileal_data.empty:
    print("No data available for ileal live bacteria plot.")
else:
    plt.figure(figsize=(8, 6))
    sns.violinplot(x='treatment', y='counts_live_bacteria_per_wet_g', data=ileal_data, palette={"ABX": "orange", "placebo": "blue"})
    plt.yscale("log")
    plt.xlabel("Treatment")
    plt.ylabel("log10(live bacteria/wet g)")
    plt.title("Ileal live bacteria")
    plt.savefig("images/ileal_live_bacteria.png")
    plt.close()

print("Graphs and single combined output file have been successfully generated.")
