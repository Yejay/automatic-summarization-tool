import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

print("Skript gestartet")

# Daten für die Verarbeitungszeiten
studies = ["Studie1", "Studie2", "Studie3", "Studie4", "Studie5", "Studie6", "Studie7"]
bart_times = [57, 61, 58, 59, 67, 58, 59]
pegasus_times = [187, 111, 150, 135, 177, 129, 161]
gpt_times = [19, 10, 10, 8, 19, 19, 26]

# Einheitliches Farbschema
bart_color = '#8884d8'  # Blau
pegasus_color = '#ffc658'  # Gelb
gpt_color = '#82ca9d'  # Grün

print("Daten geladen")

# 1. Balkendiagramm
plt.figure(figsize=(12, 6))
bar_width = 0.25
r1 = np.arange(len(studies))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
plt.bar(r1, bart_times, color=bart_color, width=bar_width, label="BART")
plt.bar(r2, pegasus_times, color=pegasus_color, width=bar_width, label="PEGASUS")
plt.bar(r3, gpt_times, color=gpt_color, width=bar_width, label="GPT-4o")
plt.xlabel("Studien")
plt.ylabel("Zeit in Sekunden")
plt.title("Absolute Verarbeitungszeiten der Modelle für jede Studie")
plt.xticks([r + bar_width for r in range(len(studies))], studies)
plt.legend()
plt.ylim(0, max(pegasus_times) * 1.1)
plt.tight_layout()
plt.savefig("1_verarbeitungszeit_balken_diagramm.png")
plt.close()
print("1. Balkendiagramm gespeichert")


# Neue Daten für die quantitative Analyse
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

# 2. Balkendiagramme für Precision, Recall und F1
fig, axs = plt.subplots(3, 1, figsize=(12, 18))
fig.suptitle('Vergleich der Modelle nach Metriken')

def create_bar_plot(ax, data, title):
    x = np.arange(len(metrics))
    width = 0.25
    
    ax.bar(x - width, data[0], width, label=models[0], color=bart_color)
    ax.bar(x, data[1], width, label=models[1], color=pegasus_color)
    ax.bar(x + width, data[2], width, label=models[2], color=gpt_color)
    
    ax.set_ylabel('Score')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()

create_bar_plot(axs[0], precision, 'Precision')
create_bar_plot(axs[1], recall, 'Recall')
create_bar_plot(axs[2], f1, 'F1-Score')

plt.tight_layout()
plt.savefig('2_model_comparison_detailed.png')
plt.close()
print("2. Detailliertes Modellvergleichsdiagramm gespeichert")

print("Alle Diagramme wurden erfolgreich erstellt und gespeichert.")