import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

print("Skript gestartet")

# Daten
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

# 2. Radar-Diagramm
plt.figure(figsize=(10, 10))
angles = np.linspace(0, 2 * np.pi, len(studies), endpoint=False)

bart_times_closed = np.concatenate((bart_times, [bart_times[0]]))
pegasus_times_closed = np.concatenate((pegasus_times, [pegasus_times[0]]))
gpt_times_closed = np.concatenate((gpt_times, [gpt_times[0]]))
angles = np.concatenate((angles, [angles[0]]))

ax = plt.subplot(111, polar=True)
ax.plot(angles, bart_times_closed, "o-", linewidth=2, label="BART", color=bart_color)
ax.fill(angles, bart_times_closed, alpha=0.25, color=bart_color)
ax.plot(angles, pegasus_times_closed, "o-", linewidth=2, label="PEGASUS", color=pegasus_color)
ax.fill(angles, pegasus_times_closed, alpha=0.25, color=pegasus_color)
ax.plot(angles, gpt_times_closed, "o-", linewidth=2, label="GPT-4o", color=gpt_color)
ax.fill(angles, gpt_times_closed, alpha=0.25, color=gpt_color)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(studies)
ax.set_ylim(0, max(pegasus_times) * 1.1)
ax.set_ylabel("Verarbeitungszeit (Sekunden)")
ax.set_title("Vergleich der Verarbeitungszeiten über alle Studien")

plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
plt.tight_layout()
plt.savefig("2_verarbeitungszeit_radar_diagramm.png")
plt.close()

print("2. Radar-Diagramm gespeichert")

# 3. Liniendiagramm
plt.figure(figsize=(12, 6))
plt.plot(studies, bart_times, marker="o", label="BART", color=bart_color)
plt.plot(studies, pegasus_times, marker="s", label="PEGASUS", color=pegasus_color)
plt.plot(studies, gpt_times, marker="^", label="GPT-4o", color=gpt_color)

plt.xlabel("Studien")
plt.ylabel("Zeit in Sekunden")
plt.title("Verarbeitungszeiten der Modelle über alle Studien")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("3_verarbeitungszeit_linien_diagramm.png")
plt.close()

print("3. Liniendiagramm gespeichert")

# 4. Heatmap
plt.figure(figsize=(12, 8))
data = [bart_times, pegasus_times, gpt_times]
sns.heatmap(
    data,
    annot=True,
    fmt="d",
    cmap="YlOrRd",
    xticklabels=studies,
    yticklabels=["BART", "PEGASUS", "GPT-4o"],
)
plt.xlabel("Studien")
plt.ylabel("Modelle")
plt.title("Heatmap der Verarbeitungszeiten")

plt.tight_layout()
plt.savefig("4_verarbeitungszeit_heatmap.png")
plt.close()

print("4. Heatmap gespeichert")

print("Alle Diagramme wurden erfolgreich erstellt und gespeichert.")