import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess data
df = pd.read_csv("results.csv")
df['level'] = df['level'].astype(str)

# Group by method
grouped = df.groupby(['ai_method']).agg({
    'steps': 'mean',
    'time_ms': 'mean',
    'cost': 'mean',
    'success': 'mean',
    'replans': 'mean'
}).reset_index()

# Calculate success rate
grouped['success_rate'] = (grouped['success'] * 100).round(1)

# Tag noise and clean method names
grouped['Noise'] = grouped['ai_method'].str.contains('_noise')
grouped['Method'] = grouped['ai_method'].str.replace('_noise', '', regex=False)
grouped['Method'] = grouped['Method'].str.replace('_fallback', '', regex=False)

#  Plotting function (full dataset)
def plot_metric(metric, ylabel, title, filename, data=grouped):
    pivot = data.pivot_table(index='Method', columns='Noise', values=metric)
    
    # Automatically rename columns based on what's present
    col_labels = []
    if True in pivot.columns:
        col_labels.append("Noise")
    if False in pivot.columns:
        col_labels.insert(0, "No Noise")
    pivot.columns = col_labels

    pivot = pivot.sort_index()
    
    pivot.plot(kind='bar', figsize=(10, 6), color=['#4CAF50', '#FF7043'][:len(pivot.columns)])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Algorithm")
    plt.xticks(rotation=0)
    if metric == 'success_rate':
        plt.ylim(0, 110)
    plt.legend(title="Condition")
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


# (includes everything)
plot_metric('time_ms', 'Time (μs)', 'Execution Time per Algorithm: Noise vs No Noise', 'time_noise.png')
plot_metric('success_rate', 'Success Rate (%)', 'Success Rate per Algorithm: Noise vs No Noise', 'success_rate_noise.png')
plot_metric('steps', 'Average Steps', 'Steps per Algorithm: Noise vs No Noise', 'steps_noise.png')
plot_metric('cost', 'Path Cost', 'Path Cost per Algorithm: Noise vs No Noise', 'cost_noise.png')
plot_metric('replans', 'Average Replans', 'Replans due to Noise per Algorithm', 'replans_noise.png')

# excluding random
exclude_random = ['random', 'random_noise', 'random_noise_fallback']
grouped_no_random = grouped[~grouped['ai_method'].isin(exclude_random)]

plot_metric('time_ms', 'Time (μs)', 'Execution Time: Noise vs No Noise (Excluding Random)', 'time_excl_random.png', data=grouped_no_random)
plot_metric('cost', 'Path Cost', 'Path Cost: Noise vs No Noise (Excluding Random)', 'path_cost_excl_random.png', data=grouped_no_random)
plot_metric('steps', 'Average Steps', 'Steps: Noise vs No Noise (Excluding Random)', 'steps_excl_random.png', data=grouped_no_random)

# Only No-Noise Runs (excluding randoms)
exclude_random = ['random', 'random_noise', 'random_noise_fallback']
grouped_no_noise = grouped[
    (grouped['Noise'] == False) & (~grouped['ai_method'].isin(exclude_random))
]
plot_metric('time_ms', 'Time (μs)', 'Execution Time (No Noise Only)', 'time_no_noise_only.png', data=grouped_no_noise)
plot_metric('steps', 'Average Steps', 'Steps (No Noise Only)', 'steps_no_noise_only.png', data=grouped_no_noise)
plot_metric('cost', 'Path Cost', 'Path Cost (No Noise Only)', 'cost_no_noise_only.png', data=grouped_no_noise)

# Only Noise Runs (excluding random)
grouped_noise_only = grouped[
    (grouped['Noise'] == True) & (~grouped['ai_method'].isin(['random_noise', 'random_noise_fallback']))
]
plot_metric('time_ms', 'Time (μs)', 'Execution Time (Noise Only)', 'time_noise_only.png', data=grouped_noise_only)
plot_metric('steps', 'Average Steps', 'Steps (Noise Only)', 'steps_noise_only.png', data=grouped_noise_only)
plot_metric('cost', 'Path Cost', 'Path Cost (Noise Only)', 'cost_noise_only.png', data=grouped_noise_only)
