import matplotlib.pyplot as plt
import numpy as np

models = ['BART', 'PEGASUS', 'OpenAI']
metrics = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L', 'BERTScore']

# Daten für Precision, Recall und F1
precision = [
    [0.384, 0.114, 0.228, 0.821],  # BART
    [0.366, 0.076, 0.216, 0.804],  # PEGASUS
    [0.280, 0.134, 0.190, 0.859]   # OpenAI
]

recall = [
    [0.366, 0.110, 0.218, 0.817],  # BART
    [0.270, 0.056, 0.159, 0.801],  # PEGASUS
    [0.825, 0.394, 0.560, 0.858]   # OpenAI
]

f1 = [
    [0.371, 0.111, 0.221, 0.819],  # BART
    [0.301, 0.062, 0.177, 0.802],  # PEGASUS
    [0.404, 0.193, 0.273, 0.858]   # OpenAI
]

# Erstellen der Subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 18))
fig.suptitle('Vergleich der Modelle nach Metriken')

# Funktion zum Erstellen der Balkendiagramme
def create_bar_plot(ax, data, title):
    x = np.arange(len(metrics))
    width = 0.25
    
    for i, model_data in enumerate(data):
        ax.bar(x + i*width, model_data, width, label=models[i])
    
    ax.set_ylabel('Score')
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics)
    ax.legend()

# Erstellen der einzelnen Plots
create_bar_plot(axs[0], precision, 'Precision')
create_bar_plot(axs[1], recall, 'Recall')
create_bar_plot(axs[2], f1, 'F1-Score')

plt.tight_layout()
plt.savefig('model_comparison_detailed.png')
plt.close()