import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data (211111 setting)
# data = {
#     'Model': ['o1', 'o1-preview', 'DeepSeek-R1', 'GPT-4o', 'GPT-4-turbo', 'haiku'],
#     'Unit': [1.00,0.96,1.0,0.88,0.79,0.19],
#     'Influence': [0.99,0.96,0.84,0.90,0.73,0.70],
#     'Adjacent': [0.99,0.98,1.00,0.96,0.97,0.85],
#     'Attackable': [0.24,0.32,0.27,0.38,0.38,0.39],
#     'Attack Analysis': [0.11,0.24,0.14,0.29,0.23,0.28]
# }
data = {
    'Model': ['o1', 'o1-preview', 'DeepSeek-R1', 'GPT-4o', 'GPT-4-turbo'],
    'Unit': [1.00,0.96,1.0,0.88,0.79],
    'Influence': [0.99,0.96,0.84,0.90,0.73],
    'Adjacent': [0.99,0.98,1.00,0.96,0.97],
    'Attackable': [0.24,0.32,0.27,0.38,0.38],
    'Attack Analysis': [0.11,0.24,0.14,0.29,0.23]
}

df = pd.DataFrame(data).set_index('Model')

# Scale everything up
sns.set_context("talk", font_scale=1.5)

plt.figure(figsize=(10, 6))
ax = sns.heatmap(
    df,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    cbar=True,
    annot_kws={"size": 22}
)

# Title & axis labels
ax.set_title('F1 score heat map', fontsize=28, pad=10)
ax.set_xlabel('Category', fontsize=24)
ax.set_ylabel('Model', fontsize=24)

# Tick labels
ax.set_xticklabels(ax.get_xticklabels(), fontsize=20, rotation=30, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)

# Colorbar tweaks
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)
cbar.set_label('F1 Score', fontsize=20)

plt.tight_layout()
plt.savefig('factual-heat-211111.pdf')