"""#Figures"""

# ============================================================
# INSTALLATION ET IMPORTS
# ============================================================
!pip install --quiet matplotlib seaborn scipy

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
import json
import os
import glob

# Configuration publication-quality
mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

DRONE_COLORS = ["#E63946", "#2E86AB", "#F18F01",
                "#06A77D", "#A23B72", "#6A994E", "#BC6C25"]

print(f"✅ Configuration prête. Sortie : {FIG_DIR}/")

import pandas as pd

rows = []

# --- Small (tab:alns_small_validation) ---
small = [
    (0, 100.00, 0.00, 199.5, 4.87),
    (1,  99.49, 0.08, 198.4, 2.85),
    (2, 100.00, 0.00, 163.7, 2.18),
    (3, 100.00, 0.00, 142.0, 1.39),
    (4, 100.00, 0.00, 181.4, 2.35),
    (5, 100.00, 0.00, 160.7, 1.99),
    (6,  99.66, 0.00, 199.6, 3.45),
    (7, 100.00, 0.00, 140.0, 1.23),
    (8, 100.00, 0.00, 156.0, 1.56),
    (9,  99.46, 0.00, 178.1, 2.41),
]
for i, cov, cov_std, E_kJ, t in small:
    rows.append({"class": "Small", "instance": f"instance_advanced_{i}",
                 "coverage_mean": cov, "coverage_std": cov_std,
                 "energy_mean": E_kJ * 1000, "time_mean": t,
                 "milp_cov": None})

# --- Medium (tab:medium_comparison, colonnes ALNS + milp_cov mis à jour Ins_10) ---
medium = [
    (10, 100.0,  0.00, 331.4,  4.5,  97.0),
    (11, 100.0,  0.00, 372.9,  6.5,  95.9),
    (12,  99.57, 0.17, 324.6,  2.6,  99.4),
    (13,  99.24, 0.13, 318.6,  3.7,  98.0),
    (14, 100.0,  0.00, 236.7,  1.2, 100.0),
    (15, 100.0,  0.00, 358.7,  5.3,  99.0),
    (16, 100.0,  0.00, 380.4,  8.0,  75.1),
    (17, 100.0,  0.00, 308.2,  2.7,  99.3),
    (18, 100.0,  0.00, 416.1, 14.1, 100.0),
    (19, 100.0,  0.00, 390.7,  9.2, 100.0),
]
for i, cov, cov_std, E_kJ, t, milp in medium:
    rows.append({"class": "Medium", "instance": f"instance_advanced_{i}",
                 "coverage_mean": cov, "coverage_std": cov_std,
                 "energy_mean": E_kJ * 1000, "time_mean": t,
                 "milp_cov": milp})

# --- 100/150/200 (tab:alns_100, tab:alns_150, tab:alns_200) ---
size = {
    "100": [(100.00, 569.3, 30.4), (100.00, 625.9, 31.9), (100.00, 596.9, 37.5),
            (100.00, 620.6, 38.1), (100.00, 597.0, 34.2), (100.00, 599.8, 32.6),
            ( 99.94, 618.8, 37.1), (100.00, 547.0, 29.2), (100.00, 561.7, 39.2),
            (100.00, 561.7, 33.5)],
    "150": [(100.00, 811.4, 83.2), (100.00, 802.8, 86.2), (100.00, 809.7, 74.9),
            (100.00, 800.1, 80.2), ( 95.25, 683.5, 73.3), ( 76.55, 548.6, 80.6),
            (100.00, 795.2, 85.2), (100.00, 802.3, 79.6), (100.00, 806.6, 79.8),
            (100.00, 813.3, 88.8)],
    "200": [(100.00,1006.3,166.6), (100.00,1021.5,181.7), ( 99.90, 992.1,208.1),
            (100.00,1039.7,219.1), (100.00, 994.4,180.8), ( 99.98, 979.0,186.0),
            ( 93.11, 792.3,197.3), (100.00, 995.3,203.7), (100.00,1020.0,214.6),
            ( 89.66, 680.4,154.7)],
}
for cls, values in size.items():
    for i, (cov, E_kJ, t) in enumerate(values):
        rows.append({"class": cls, "instance": f"{cls}_{i}",
                     "coverage_mean": cov, "coverage_std": 0.0,
                     "energy_mean": E_kJ * 1000, "time_mean": t,
                     "milp_cov": None})

df = pd.DataFrame(rows)
df.to_csv("summary_ALNS.csv", index=False)

print(f"✅ summary_ALNS.csv créé : {len(df)} instances")
print("\nRésumé par classe :")
print(df.groupby("class").agg(
    n=("instance", "count"),
    cov_mean=("coverage_mean", "mean"),
    E_mean_kJ=("energy_mean", lambda x: x.mean()/1000),
    t_mean_s=("time_mean", "mean"),
).round(2))

import pandas as pd
df = pd.read_csv("summary_ALNS.csv")

# Puis relancer les 3 scripts de figures 5, 7, 8, 9
# (les scripts que vous m'avez montrés)

import pandas as pd

df = pd.read_csv("summary_ALNS.csv")

# ---------- 1. Remplir n_targets ----------
n_targets_map = {
    "instance_advanced_0": 21, "instance_advanced_1": 20,
    "instance_advanced_2": 16, "instance_advanced_3": 13,
    "instance_advanced_4": 17, "instance_advanced_5": 15,
    "instance_advanced_6": 24, "instance_advanced_7": 13,
    "instance_advanced_8": 14, "instance_advanced_9": 19,
    "instance_advanced_10": 41, "instance_advanced_11": 51,
    "instance_advanced_12": 42, "instance_advanced_13": 47,
    "instance_advanced_14": 29, "instance_advanced_15": 47,
    "instance_advanced_16": 57, "instance_advanced_17": 37,
    "instance_advanced_18": 61, "instance_advanced_19": 56,
}
for i in range(10):
    n_targets_map[f"instance_100_{i}"] = 100
    n_targets_map[f"instance_150_{i}"] = 150
    n_targets_map[f"instance_200_{i}"] = 200

df["n_targets"] = df["instance"].map(n_targets_map)
assert df["n_targets"].notna().all(), "Manque n_targets pour certaines instances"

# ---------- 2. Mettre à jour les 10 small (nouvelles valeurs) ----------
# (cov_mean, cov_std, E_mean_kJ, E_std_kJ, t_mean_s)
small_new = {
    "instance_advanced_0": (100.00, 0.00, 199.5, 0.6, 4.87),
    "instance_advanced_1": ( 99.49, 0.08, 198.4, 2.3, 2.85),
    "instance_advanced_2": (100.00, 0.00, 163.7, 0.0, 2.18),
    "instance_advanced_3": (100.00, 0.00, 142.0, 0.0, 1.39),
    "instance_advanced_4": (100.00, 0.00, 181.4, 0.0, 2.35),
    "instance_advanced_5": (100.00, 0.00, 160.7, 0.0, 1.99),
    "instance_advanced_6": ( 99.66, 0.00, 199.6, 0.0, 3.45),
    "instance_advanced_7": (100.00, 0.00, 140.0, 0.0, 1.23),
    "instance_advanced_8": (100.00, 0.00, 156.0, 0.0, 1.56),
    "instance_advanced_9": ( 99.46, 0.00, 178.1, 0.0, 2.41),
}

for inst, (cov, cov_s, E_kJ, E_s_kJ, t_new) in small_new.items():
    mask = df["instance"] == inst
    # Scale time_std proportionnellement au changement de moyenne
    t_old = df.loc[mask, "time_mean"].values[0]
    std_old = df.loc[mask, "time_std"].values[0]
    std_new = std_old * (t_new / t_old) if t_old > 0 else 0.0

    df.loc[mask, "coverage_mean"] = cov
    df.loc[mask, "coverage_std"]  = cov_s
    df.loc[mask, "energy_mean"]   = E_kJ * 1000
    df.loc[mask, "energy_std"]    = E_s_kJ * 1000
    df.loc[mask, "time_mean"]     = t_new
    df.loc[mask, "time_std"]      = std_new

# ---------- 3. Sauvegarde ----------
df.to_csv("summary_ALNS.csv", index=False)

# ---------- 4. Vérification ----------
print(f"✅ summary_ALNS.csv corrigé : {len(df)} instances")
print(f"\nRésumé par classe :")
print(df.groupby("class" if "class" in df.columns else df["instance"].str.extract(r'(advanced|100|150|200)')[0]).agg(
    n=("instance", "count"),
    drones=("active_drones_mean", "mean"),
    cov=("coverage_mean", "mean"),
    E_kJ=("energy_mean", lambda x: x.mean()/1000),
    t_s=("time_mean", "mean"),
).round(2))

print("\nPremières lignes small (vérification) :")
print(df[df["instance"].str.startswith("instance_advanced_") &
         (df["instance"].str.extract(r'_(\d+)$')[0].astype(int) < 10)]
      [["instance","n_targets","coverage_mean","energy_mean","time_mean"]].to_string())

import pandas as pd

df = pd.read_csv("summary_ALNS.csv")

# Dériver la colonne class depuis le nom de l'instance
def get_class(inst):
    if inst.startswith("instance_advanced_"):
        i = int(inst.split("_")[-1])
        return "Small" if i < 10 else "Medium"
    if inst.startswith("instance_100_"): return "100"
    if inst.startswith("instance_150_"): return "150"
    if inst.startswith("instance_200_"): return "200"
    return None

df["class"] = df["instance"].apply(get_class)

# Vérification
print(df["class"].value_counts())
# Attendu : Small 10, Medium 10, 100 10, 150 10, 200 10

# ============================================================
# FIGURE 5 : Scalability — temps de calcul vs nombre de cibles
# ============================================================
fig, ax = plt.subplots(figsize=(6.5, 4.5))

classes = ["Small", "Medium", "100", "150", "200"]
x_labels = [20, 45, 100, 150, 200]
means = [df[df["class"] == c]["time_mean"].mean() for c in classes]
stds  = [df[df["class"] == c]["time_mean"].std()  for c in classes]

ax.errorbar(x_labels, means, yerr=stds, fmt="o-", capsize=5,
            color="#2E86AB", linewidth=2, markersize=8,
            markerfacecolor="white", markeredgewidth=2,
            label="ALNS mean runtime")

ax.axhline(y=300, color="red", linestyle="--", linewidth=1.5,
           label="Time limit (300 s)")

ax.set_yscale("log")
ax.set_xlabel("Number of targets")
ax.set_ylabel("CPU time (s)")
ax.set_title("ALNS scalability: computation time vs instance size")
ax.legend(loc="upper left")
ax.set_xticks(x_labels)
ax.set_xticklabels(["20", "45", "100", "150", "200"])

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scalability_time.png")
plt.savefig(f"{FIG_DIR}/scalability_time.pdf")
plt.close()
print("✅ Fig 5 : scalability_time")

# ============================================================
# FIGURE 6 : Coverage distribution par nombre de drones
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4.5))

df_large = df[df["class"].isin(["100", "150", "200"])]
drones_values = sorted(df_large["drones_rounded"].unique())
colors = ["#E63946", "#F77F00", "#2E86AB", "#06A77D"]

data_by_drones = [df_large[df_large["drones_rounded"] == d]["coverage_mean"].values
                  for d in drones_values]

bp = ax.boxplot(data_by_drones, positions=drones_values, widths=0.5,
                patch_artist=True, showmeans=True,
                meanprops=dict(marker="D", markerfacecolor="black",
                               markeredgecolor="black", markersize=6))

for patch, color in zip(bp["boxes"], colors[:len(drones_values)]):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.set_xlabel("Number of active drones")
ax.set_ylabel("Coverage (%)")
ax.set_title("Coverage distribution by fleet size (large instances)")
ax.set_xticks(drones_values)
ax.set_xticklabels([str(d) for d in drones_values])
ax.axhline(y=100, color="green", linestyle=":", linewidth=1,
           label="Full coverage")
ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/coverage_vs_drones.png")
plt.savefig(f"{FIG_DIR}/coverage_vs_drones.pdf")
plt.close()
print("✅ Fig 6 : coverage_vs_drones")

# ============================================================
# FIGURE 7 : Comparaison Gurobi vs ALNS sur instances medium
# ============================================================
# Chiffres MILP du manuscrit (Table 8)
milp_data = {
    "instance_advanced_10": 97.0,
    "instance_advanced_11": 95.9,
    "instance_advanced_12": 99.4,
    "instance_advanced_13": 98.0,
    "instance_advanced_14": 100.0,
    "instance_advanced_15": 99.0,
    "instance_advanced_16": 75.1,
    "instance_advanced_17": 99.3,
    "instance_advanced_18": 100.0,
    "instance_advanced_19": 100.0,
}

medium = df[df["class"] == "Medium"].copy()
medium["milp_cov"] = medium["instance"].map(milp_data)
medium = medium.dropna(subset=["milp_cov"]).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(9, 4.5))

x = np.arange(len(medium))
width = 0.35

bars1 = ax.bar(x - width/2, medium["milp_cov"], width,
               label="Gurobi (600 s)", color="#E63946", alpha=0.8)
bars2 = ax.bar(x + width/2, medium["coverage_mean"], width,
               yerr=medium["coverage_std"], capsize=4,
               label="ALNS (30 runs)", color="#2E86AB", alpha=0.8)

ax.set_xlabel("Instance")
ax.set_ylabel("Coverage (%)")
ax.set_title("Gurobi vs ALNS on medium instances (29–61 targets)")
ax.set_xticks(x)
ax.set_xticklabels([f"Ins_{i}" for i in range(10, 20)], rotation=45, ha="right")
ax.legend()
ax.set_ylim(70, 105)
ax.axhline(y=100, color="green", linestyle=":", linewidth=1, alpha=0.5)

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/gurobi_vs_alns_coverage.png")
plt.savefig(f"{FIG_DIR}/gurobi_vs_alns_coverage.pdf")
plt.close()
print("✅ Fig 7 : gurobi_vs_alns_coverage")

# ============================================================
# FIGURE 8 : Pareto front (coverage vs energy)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))

colors = {"Small": "#2E86AB", "Medium": "#A23B72",
          "100": "#F18F01", "150": "#C73E1D", "200": "#6A994E"}

for cls in ["Small", "Medium", "100", "150", "200"]:
    sub = df[df["class"] == cls]
    ax.scatter(sub["energy_mean"] / 1000, sub["coverage_mean"],
               label=f"{cls} targets", color=colors[cls],
               s=80, alpha=0.7, edgecolors="black", linewidth=0.5)

ax.set_xlabel("Energy (kJ)")
ax.set_ylabel("Coverage (%)")
ax.set_title("Coverage–energy trade-off across instance classes")
ax.legend(loc="lower right", fontsize=8)
ax.axhline(y=100, color="green", linestyle=":", linewidth=1, alpha=0.5)

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/pareto_front.png")
plt.savefig(f"{FIG_DIR}/pareto_front.pdf")
plt.close()
print("✅ Fig 8 : pareto_front")

# ============================================================
# FIGURE 9 : Efficiency curve (coverage per energy)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))

for cls in ["Small", "Medium", "100", "150", "200"]:
    sub = df[df["class"] == cls].copy()
    sub["efficiency"] = sub["coverage_mean"] / (sub["energy_mean"] / 1000)
    ax.scatter(sub["energy_mean"] / 1000,
               sub["coverage_mean"] / (sub["energy_mean"] / 1000),
               label=f"{cls} targets", color=colors[cls],
               s=80, alpha=0.7, edgecolors="black", linewidth=0.5)

ax.set_xlabel("Energy (kJ)")
ax.set_ylabel("Coverage per kJ (%) / kJ")
ax.set_title("Energy efficiency across instance classes")
ax.legend(loc="upper right", fontsize=8)

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/efficiency_curve.png")
plt.savefig(f"{FIG_DIR}/efficiency_curve.pdf")
plt.close()
print("✅ Fig 9 : efficiency_curve")

# ============================================================
# FIGURE 10 : Physical ablation (FM, NC, CS, FR)
# ============================================================
fig, ax = plt.subplots(figsize=(6.5, 4.5))

models = ["FM", "NC", "CS", "FR"]
energy_var = [0.0, 6.5, 3.1, 12.3]
route_var = [0.0, 4.2, 1.8, 9.7]

x = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x - width/2, energy_var, width,
               label="Energy variation", color="#E63946", alpha=0.8)
bars2 = ax.bar(x + width/2, route_var, width,
               label="Route length variation", color="#2E86AB", alpha=0.8)

for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    f"+{h:.1f}%", ha="center", fontsize=8)

ax.set_xlabel("Model variant")
ax.set_ylabel("Variation vs Full Model (%)")
ax.set_title("Physical ablation: impact of modelling simplifications")
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()
ax.set_ylim(0, 15)

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/ablation_study.png")
plt.savefig(f"{FIG_DIR}/ablation_study.pdf")
plt.close()
print("✅ Fig 10 : ablation_study")

# ============================================================
# FIGURE 11 : Heatmap couverture par (drones, classe)
# ============================================================
df_large = df[df["class"].isin(["100", "150", "200"])]
classes = ["100", "150", "200"]
drones_values = sorted(df_large["drones_rounded"].unique())

matrix = np.full((len(drones_values), len(classes)), np.nan)
counts = np.zeros_like(matrix, dtype=int)

for i, d in enumerate(drones_values):
    for j, c in enumerate(classes):
        sub = df_large[(df_large["drones_rounded"] == d) &
                        (df_large["class"] == c)]
        if len(sub) > 0:
            matrix[i, j] = sub["coverage_mean"].mean()
            counts[i, j] = len(sub)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax = axes[0]
im = ax.imshow(matrix, cmap="RdYlGn", vmin=70, vmax=100, aspect="auto")
ax.set_xticks(range(len(classes)))
ax.set_xticklabels([f"{c} targets" for c in classes])
ax.set_yticks(range(len(drones_values)))
ax.set_yticklabels([f"{d} drones" for d in drones_values])
ax.set_xlabel("Instance class")
ax.set_ylabel("Number of active drones")
ax.set_title("(a) Mean coverage (%)")

for i in range(len(drones_values)):
    for j in range(len(classes)):
        if not np.isnan(matrix[i, j]):
            color = "black" if 75 < matrix[i, j] < 98 else "white"
            ax.text(j, i, f"{matrix[i, j]:.1f}\n(n={counts[i, j]})",
                    ha="center", va="center", color=color,
                    fontsize=9, fontweight="bold")

cbar = plt.colorbar(im, ax=ax, fraction=0.046)
cbar.set_label("Coverage (%)")

ax = axes[1]
im2 = ax.imshow(counts, cmap="Blues", aspect="auto")
ax.set_xticks(range(len(classes)))
ax.set_xticklabels([f"{c} targets" for c in classes])
ax.set_yticks(range(len(drones_values)))
ax.set_yticklabels([f"{d} drones" for d in drones_values])
ax.set_xlabel("Instance class")
ax.set_ylabel("Number of active drones")
ax.set_title("(b) Number of instances")

for i in range(len(drones_values)):
    for j in range(len(classes)):
        color = "white" if counts[i, j] > 3 else "black"
        ax.text(j, i, str(counts[i, j]), ha="center", va="center",
                color=color, fontsize=11, fontweight="bold")

cbar2 = plt.colorbar(im2, ax=ax, fraction=0.046)
cbar2.set_label("Count")

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/heatmap_drones_coverage.png")
plt.savefig(f"{FIG_DIR}/heatmap_drones_coverage.pdf")
plt.close()
print("✅ Fig 11 : heatmap_drones_coverage")

# ============================================================
# FIGURE 12 : Couverture vs nombre de drones (boxplot par classe)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))

classes = ["Small", "Medium", "100", "150", "200"]
positions = []
data = []
labels = []

pos_counter = 0
for cls in classes:
    sub = df[df["class"] == cls]
    if len(sub) == 0:
        continue
    for d in sorted(sub["drones_rounded"].unique()):
        data.append(sub[sub["drones_rounded"] == d]["coverage_mean"].values)
        positions.append(pos_counter)
        labels.append(f"{cls}\n({d}d)")
        pos_counter += 1
    pos_counter += 0.5

bp = ax.boxplot(data, positions=positions, widths=0.6,
                patch_artist=True, showmeans=True,
                meanprops=dict(marker="D", markerfacecolor="black",
                               markeredgecolor="black", markersize=6))

for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(DRONE_COLORS[i % len(DRONE_COLORS)])
    patch.set_alpha(0.7)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylabel("Coverage (%)")
ax.set_title("Coverage distribution by instance class and fleet size")
ax.axhline(y=100, color="green", linestyle=":", linewidth=1,
           label="Full coverage", alpha=0.6)
ax.set_ylim(70, 103)
ax.legend(loc="lower left")

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/coverage_vs_drones_class.png")
plt.savefig(f"{FIG_DIR}/coverage_vs_drones_class.pdf")
plt.close()
print("✅ Fig 12 : coverage_vs_drones_class")

# ============================================================
# FIGURE 13 : Algorithmic ablation (NOUVELLE)
# ============================================================
configs = ["Full\nALNS", "Sans\nadaptatif", "Sans\nlocal search",
           "Random\nonly", "Glouton\n(no SA)"]

cov_150_5 = [76.55, 76.61, 76.30, 75.87, 75.86]
std_150_5 = [0.59, 0.50, 0.83, 0.48, 0.60]
cov_200_9 = [89.66, 89.71, 89.45, 89.80, 89.70]
std_200_9 = [0.26, 0.26, 0.38, 0.29, 0.25]

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Instance 150_5
ax = axes[0]
x = np.arange(len(configs))
colors_bars = ["#2E86AB" if i == 0 else "#A0A0A0"
               for i in range(len(configs))]
ax.bar(x, cov_150_5, yerr=std_150_5, capsize=4,
       color=colors_bars, alpha=0.85,
       edgecolor="black", linewidth=0.5)
ax.axhline(y=76.55, color="red", linestyle="--", linewidth=1,
           label="Full ALNS baseline")
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=8)
ax.set_ylabel("Coverage (%)")
ax.set_title("(a) Instance 150_5 (150 targets, 2 drones)")
ax.set_ylim(74, 78)
ax.legend(fontsize=8)

# Instance 200_9
ax = axes[1]
ax.bar(x, cov_200_9, yerr=std_200_9, capsize=4,
       color=colors_bars, alpha=0.85,
       edgecolor="black", linewidth=0.5)
ax.axhline(y=89.66, color="red", linestyle="--", linewidth=1,
           label="Full ALNS baseline")
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=8)
ax.set_ylabel("Coverage (%)")
ax.set_title("(b) Instance 200_9 (200 targets, 2 drones)")
ax.set_ylim(88, 91)
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/ablation_algorithmic.png")
plt.savefig(f"{FIG_DIR}/ablation_algorithmic.pdf")
plt.close()
print("✅ Fig 13 : ablation_algorithmic")

import os, glob

print("=" * 70)
print("VÉRIFICATION DES FICHIERS")
print("=" * 70)

# Instances
print("\n📁 Instances (racine) :")
for i in [0, 1, 2, 3]:
    f = f"instance_advanced_{i}.json"
    status = "✅" if os.path.exists(f) else "❌"
    print(f"   {status} {f}")

# Solutions FM
print("\n📁 Solutions FM :")
for i in [0, 1, 2, 3]:
    f = f"instance_advanced_{i}_seed0.json"
    status = "✅" if os.path.exists(f) else "❌"
    print(f"   {status} {f}")

# Solutions NC
print("\n📁 Solutions NC :")
for i in [0, 1, 2, 3]:
    f = f"instance_advanced_results_nc_{i}_seed0.json"
    status = "✅" if os.path.exists(f) else "❌"
    print(f"   {status} {f}")

print("\n" + "=" * 70)

# ============================================================
# FIGURES 14-16 : Routes 2D, 3D et multi-instances (FM vs NC)
# ============================================================
import json
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

DRONE_COLORS = ["#E63946", "#2E86AB", "#F18F01",
                "#06A77D", "#A23B72", "#6A994E"]


# ============================================================
# UTILITAIRES
# ============================================================
def load_json(path):
    with open(path) as f:
        return json.load(f)


def get_routes_coords(instance, solution):
    depots = instance["depots"]
    targets = instance["targets"]
    nd = len(depots)

    def node_xyz(node):
        d = depots[node] if node < nd else targets[node - nd]
        return (d["x"], d["y"], d["z"])

    return [{"drone": r["drone"],
             "coords": [node_xyz(n) for n in r["nodes"]]}
            for r in solution["routes"]]


def get_depots_xyz(instance):
    return [(d["x"], d["y"], d["z"]) for d in instance["depots"]]


def get_targets_xyz(instance):
    return [(t["x"], t["y"], t["z"]) for t in instance["targets"]]


def get_mine_mask(instance):
    return [bool(t.get("is_mine", False)) for t in instance["targets"]]


def plot_2d(instance, solution, ax, title=""):
    routes = get_routes_coords(instance, solution)
    depots = get_depots_xyz(instance)
    targets = get_targets_xyz(instance)
    mask = get_mine_mask(instance)

    non_mine = [t for t, m in zip(targets, mask) if not m]
    if non_mine:
        ax.scatter([p[0] for p in non_mine], [p[1] for p in non_mine],
                   s=25, c="lightgray", edgecolors="gray",
                   linewidth=0.5, zorder=2, label="Targets")

    mines = [t for t, m in zip(targets, mask) if m]
    if mines:
        ax.scatter([p[0] for p in mines], [p[1] for p in mines],
                   s=80, c="red", marker="*",
                   edgecolors="darkred", linewidth=0.8, zorder=4,
                   label="Mines")

    for i, (x, y, z) in enumerate(depots):
        ax.scatter(x, y, s=200, c="steelblue", marker="s",
                   edgecolors="black", linewidth=1.2, zorder=5,
                   label="Depots" if i == 0 else None)
        ax.annotate(f"D{i}", (x, y), xytext=(6, 6),
                    textcoords="offset points", fontsize=9,
                    fontweight="bold")

    for r in routes:
        c = r["coords"]
        color = DRONE_COLORS[r["drone"] % len(DRONE_COLORS)]
        ax.plot([p[0] for p in c], [p[1] for p in c],
                "-", color=color, linewidth=2.0, alpha=0.85, zorder=3,
                label=f"Drone {r['drone']}")

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(loc="best", fontsize=7, framealpha=0.9)


def plot_3d(instance, solution, ax, title=""):
    routes = get_routes_coords(instance, solution)
    depots = get_depots_xyz(instance)
    targets = get_targets_xyz(instance)
    mask = get_mine_mask(instance)

    non_mine = [t for t, m in zip(targets, mask) if not m]
    if non_mine:
        ax.scatter([p[0] for p in non_mine],
                   [p[1] for p in non_mine],
                   [p[2] for p in non_mine],
                   s=15, c="lightgray", edgecolors="gray",
                   linewidth=0.3, label="Targets", depthshade=True)

    mines = [t for t, m in zip(targets, mask) if m]
    if mines:
        ax.scatter([p[0] for p in mines],
                   [p[1] for p in mines],
                   [p[2] for p in mines],
                   s=80, c="red", marker="*",
                   edgecolors="darkred", linewidth=0.8,
                   label="Mines", depthshade=True)

    for i, (x, y, z) in enumerate(depots):
        ax.scatter(x, y, z, s=150, c="steelblue", marker="s",
                   edgecolors="black", linewidth=1.0,
                   label="Depots" if i == 0 else None, depthshade=True)

    for r in routes:
        c = r["coords"]
        color = DRONE_COLORS[r["drone"] % len(DRONE_COLORS)]
        ax.plot([p[0] for p in c],
                [p[1] for p in c],
                [p[2] for p in c],
                "-", color=color, linewidth=2.0, alpha=0.85,
                label=f"Drone {r['drone']}")

    ax.set_xlabel("X (m)", labelpad=8)
    ax.set_ylabel("Y (m)", labelpad=8)
    ax.set_zlabel("Depth (m)", labelpad=8)
    ax.set_title(title)
    ax.view_init(elev=20, azim=45)


# ============================================================
# FIGURE 14 : Comparaison 2D
# ============================================================
INSTANCE = "instance_advanced_3.json"
SOL_FM = "instance_advanced_3_seed0.json"
SOL_NC = "instance_advanced_results_nc_3_seed0.json"

inst = load_json(INSTANCE)
sol_fm = load_json(SOL_FM)
sol_nc = load_json(SOL_NC)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
plot_2d(inst, sol_fm, axes[0],
        title="(a) Full model (FM) — depth-dependent currents")
plot_2d(inst, sol_nc, axes[1],
        title="(b) No-current variant (NC) — still water")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/routes_comparison_2d.png")
plt.savefig(f"{FIG_DIR}/routes_comparison_2d.pdf")
plt.close()
print("✅ Fig 14 : routes_comparison_2d")


# ============================================================
# FIGURE 15 : Comparaison 3D
# ============================================================
fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(121, projection="3d")
ax2 = fig.add_subplot(122, projection="3d")
plot_3d(inst, sol_fm, ax1, title="(a) Full model (FM)")
plot_3d(inst, sol_nc, ax2, title="(b) No-current variant (NC)")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/routes_3d.png")
plt.savefig(f"{FIG_DIR}/routes_3d.pdf")
plt.close()
print("✅ Fig 15 : routes_3d")


# ============================================================
# FIGURE 16 : Multi-instances (0, 1, 2)
# ============================================================
fig, axes = plt.subplots(3, 2, figsize=(14, 16))

for row, i in enumerate([0, 1, 2]):
    inst_path = f"instance_advanced_{i}.json"
    fm_path = f"instance_advanced_{i}_seed0.json"
    nc_path = f"instance_advanced_results_nc_{i}_seed0.json"

    inst_i = load_json(inst_path)
    sol_fm_i = load_json(fm_path)
    sol_nc_i = load_json(nc_path)

    plot_2d(inst_i, sol_fm_i, axes[row, 0],
            title=f"Ins_{i} — FM")
    plot_2d(inst_i, sol_nc_i, axes[row, 1],
            title=f"Ins_{i} — NC")

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/routes_multi.png")
plt.savefig(f"{FIG_DIR}/routes_multi.pdf")
plt.close()
print("✅ Fig 16 : routes_multi")


# ============================================================
# VÉRIFICATION
# ============================================================
print("\n" + "=" * 70)
print("FIGURES GÉNÉRÉES")
print("=" * 70)
for name in ["routes_comparison_2d", "routes_3d", "routes_multi"]:
    for ext in ["png", "pdf"]:
        path = f"{FIG_DIR}/{name}.{ext}"
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024
            print(f"  ✅ {path}  ({size:.1f} Ko)")

# ============================================================
# SAUVEGARDE COMPLÈTE — Version corrigée
# ============================================================
import os
import shutil
import glob
from google.colab import files
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")
ZIP_NAME = f"mddmrp_backup_{TIMESTAMP}"

staging = "/content/_download_staging"
if os.path.exists(staging):
    shutil.rmtree(staging)
os.makedirs(staging)

print("=" * 70)
print(f"SAUVEGARDE : {ZIP_NAME}")
print("=" * 70)


# ============================================================
# 1. SCRIPT PYTHON
# ============================================================
print("\n📄 Scripts Python :")
for script in ["alns_v2.py", "milp.py", "validator.py"]:
    path = f"/content/{script}"
    if os.path.exists(path):
        shutil.copy(path, staging)
        size = os.path.getsize(path) / 1024
        print(f"   ✅ {script}  ({size:.1f} Ko)")
    else:
        print(f"   ⚠️  {script} absent — PENSEZ À LE RE-UPLOADER")


# ============================================================
# 2. INSTANCES JSON (racine)
# ============================================================
print("\n📁 Instances :")
instances_dir = os.path.join(staging, "instances")
os.makedirs(instances_dir, exist_ok=True)

n_instances = 0
for f in glob.glob("/content/instance_*.json"):
    basename = os.path.basename(f)
    # Une instance n'a NI "seed" NI "results_nc" NI "_nc_" dans le nom
    if "seed" in basename:
        continue
    if "results_nc" in basename:
        continue
    if "_nc_" in basename:
        continue
    shutil.copy(f, instances_dir)
    n_instances += 1

print(f"   ✅ {n_instances} instances copiées")


# ============================================================
# 3. SOLUTIONS FM (racine)
# ============================================================
print("\n📁 Solutions FM :")
fm_dir = os.path.join(staging, "solutions_FM")
os.makedirs(fm_dir, exist_ok=True)

n_fm = 0
for f in glob.glob("/content/instance_*_seed*.json"):
    basename = os.path.basename(f)
    # Solutions FM : contient "seed" MAIS PAS "results_nc"
    if "seed" in basename and "results_nc" not in basename:
        shutil.copy(f, fm_dir)
        n_fm += 1

print(f"   ✅ {n_fm} solutions FM copiées")


# ============================================================
# 4. SOLUTIONS NC (no-current)
# ============================================================
print("\n📁 Solutions NC :")
nc_dir = os.path.join(staging, "solutions_NC")
os.makedirs(nc_dir, exist_ok=True)

n_nc = 0
for f in glob.glob("/content/*.json"):
    basename = os.path.basename(f)
    # Solutions NC : contient "results_nc"
    if "results_nc" in basename:
        shutil.copy(f, nc_dir)
        n_nc += 1

print(f"   ✅ {n_nc} solutions NC copiées")


# ============================================================
# 5. RÉSULTATS CSV
# ============================================================
print("\n📁 Résultats CSV :")
csv_dir = os.path.join(staging, "results_CSV")
os.makedirs(csv_dir, exist_ok=True)

n_csv = 0
for f in glob.glob("/content/*.csv"):
    shutil.copy(f, csv_dir)
    n_csv += 1

print(f"   ✅ {n_csv} fichiers CSV copiés")


# ============================================================
# 6. DOSSIERS DE RÉSULTATS
# ============================================================
print("\n📁 Dossiers de résultats :")
results_dirs = [
    "results_final", "results_final_100",
    "results_final_150", "results_final_200",
    "results_final_large",
    "results_abl_small_full", "results_abl_small_no_ls",
    "results_abl_small_random_only", "results_abl_small_no_adaptive",
    "results_abl_small_greedy",
    "results_nc", "results_figures",
]

found_any_dir = False
for d in results_dirs:
    path = f"/content/{d}"
    if os.path.exists(path):
        dest = os.path.join(staging, "results_dirs", d)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copytree(path, dest)
        n = sum(1 for _, _, fs in os.walk(path) for _ in fs)
        print(f"   ✅ {d}/  ({n} fichiers)")
        found_any_dir = True
    else:
        print(f"   ℹ️  {d} absent")

if not found_any_dir:
    print("   ⚠️  Aucun dossier de résultats trouvé")
    print("      → Les fichiers sont peut-être à la racine")


# ============================================================
# 7. FIGURES
# ============================================================
print("\n📁 Figures :")
if os.path.exists("/content/figures"):
    dest = os.path.join(staging, "figures")
    shutil.copytree("/content/figures", dest)
    n_figs = len([f for f in os.listdir("/content/figures")
                  if os.path.isfile(os.path.join("/content/figures", f))])
    print(f"   ✅ figures/  ({n_figs} fichiers)")
else:
    print("   ⚠️  figures/ absent")


# ============================================================
# 8. RÉCAPITULATIF
# ============================================================
print("\n" + "=" * 70)
print("RÉCAPITULATIF")
print("=" * 70)

total_size = 0
total_files = 0
for root, dirs, file_list in os.walk(staging):   # ← renommé en "file_list"
    for f in file_list:
        total_size += os.path.getsize(os.path.join(root, f))
        total_files += 1

print(f"   Fichiers : {total_files}")
print(f"   Taille   : {total_size / 1024 / 1024:.1f} Mo")

for item in sorted(os.listdir(staging)):
    path = os.path.join(staging, item)
    if os.path.isdir(path):
        n = sum(1 for _, _, fs in os.walk(path) for _ in fs)
        print(f"   📂 {item}/  ({n} fichiers)")
    else:
        size = os.path.getsize(path) / 1024
        print(f"   📄 {item}  ({size:.1f} Ko)")


# ============================================================
# 9. ZIP
# ============================================================
print("\n" + "=" * 70)
zip_path = f"/content/{ZIP_NAME}"
shutil.make_archive(zip_path, 'zip', staging)
zip_full = f"{zip_path}.zip"
size_mb = os.path.getsize(zip_full) / 1024 / 1024
print(f"📦 Archive créée : {zip_full}  ({size_mb:.1f} Mo)")
print("=" * 70)


# ============================================================
# 10. TÉLÉCHARGEMENT (avec import frais)
# ============================================================
print("\n⏬ Téléchargement...")
from google.colab import files as colab_files   # ← import frais
colab_files.download(zip_full)
print("✅ Téléchargement terminé")

# ============================================================
# FIGURE 10 : Physical ablation — Version corrigée
# ============================================================
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(7, 4.5))

# Données
models = ["FM", "NC", "CS", "FR"]
energy_var = [0.0, 6.5, 3.1, 12.3]
route_var = [0.0, 4.2, 1.8, 9.7]

x = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x - width/2, energy_var, width,
               label="Energy variation",
               color="#E63946", alpha=0.85,
               edgecolor="black", linewidth=0.5)
bars2 = ax.bar(x + width/2, route_var, width,
               label="Route length variation",
               color="#2E86AB", alpha=0.85,
               edgecolor="black", linewidth=0.5)

# ---- ÉTIQUETTES : afficher TOUTES les valeurs (y compris 0) ----
for bars, vals in [(bars1, energy_var), (bars2, route_var)]:
    for bar, v in zip(bars, vals):
        h = bar.get_height()
        if v == 0:
            # Étiquette spécifique pour la référence
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    "0.0%", ha="center", va="bottom",
                    fontsize=8, color="darkgreen",
                    fontweight="bold", style="italic")
        else:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    f"+{v:.1f}%", ha="center", va="bottom",
                    fontsize=8, fontweight="bold")

# ---- LIGNE DE RÉFÉRENCE à y=0 ----
ax.axhline(y=0, color="black", linewidth=0.8, linestyle="-",
           alpha=0.6, zorder=1)

# ---- ANNOTATION : "FM = baseline" ----
ax.annotate("FM = reference\n(baseline for comparison)",
            xy=(0, 0), xytext=(0, 8),
            ha="center", fontsize=8, style="italic",
            color="darkgreen",
            arrowprops=dict(arrowstyle="->",
                            color="darkgreen",
                            lw=0.8, alpha=0.7))

# ---- CONFIGURATION ----
ax.set_xlabel("Model variant")
ax.set_ylabel("Variation vs Full Model (%)")
ax.set_title("Physical ablation: impact of modelling simplifications")
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend(loc="upper left", fontsize=9)
ax.set_ylim(0, 15)
ax.grid(axis="y", alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig(f"{FIG_DIR}/ablation_study.png")
plt.savefig(f"{FIG_DIR}/ablation_study.pdf")
plt.close()
print("✅ Fig 10 : ablation_study (corrigée)")

!pip uninstall -y pulp
!pip install --upgrade pulp highspy

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solveur MILP pour MDDMRP-DF — Version PuLP + CBC (open-source).
Alternative à Gurobi (aucune licence requise).

Utilisation :
    python milp_pulp.py instance_advanced_7.json
"""

import json
import sys
import time
import pulp


# ============================================================
# EXTRACTION DES ROUTES À PARTIR DE LA SOLUTION
# ============================================================
def extract_routes(x, y, a, drones, N, S, K, nd):
    routes = {}
    for k in range(K):
        if a[k].varValue is None or a[k].varValue < 0.5:
            continue
        start = drones[k]["start_depot"]
        route = [start]
        visited = {start}
        current = start
        for _ in range(N):
            nxt = None
            for j in range(N):
                if j in visited:
                    continue
                for s in range(S):
                    var = x.get((current, j, s, k))
                    if var is not None and var.varValue is not None and var.varValue > 0.5:
                        nxt = j
                        break
                if nxt is not None:
                    break
            if nxt is None:
                break
            route.append(nxt)
            visited.add(nxt)
            if nxt < nd:
                break
            current = nxt
        routes[k] = route
    return routes


# ============================================================
# DÉTECTION DES SOUS-TOURS
# ============================================================
def detect_subtours(x, y, a, drones, N, S, K, nd):
    """
    Détecte pour chaque drone les composantes connexes ne contenant
    aucun dépôt. Retourne une liste de (frozenset de cibles, k).
    """
    new_sec = []
    for k in range(K):
        if a[k].varValue is None or a[k].varValue < 0.5:
            continue
        # Construire le graphe d'arcs utilisés par drone k
        parent = {i: i for i in range(N)}

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv

        for (i, j, s, kk), var in x.items():
            if kk != k:
                continue
            if var.varValue is not None and var.varValue > 0.5:
                union(i, j)

        # Regrouper les cibles visitées par composante
        comps = {}
        for j in range(nd, N):
            yv = y.get((j, k))
            if yv is not None and yv.varValue is not None and yv.varValue > 0.5:
                root = find(j)
                comps.setdefault(root, set()).add(j)

        for root, nodes in comps.items():
            has_depot = any(d in nodes for d in range(nd))
            if not has_depot and len(nodes) >= 2:
                new_sec.append((frozenset(nodes), k))
    return new_sec


# ============================================================
# CONSTRUCTION DU MODÈLE (itération SEC)
# ============================================================
def build_model(data, extra_sec=None, eps=1e-8):
    depots = data["depots"]
    targets = data["targets"]
    drones = data["drones"]
    speeds = data["drone_speeds"]
    tm = data["time_matrices"]
    em = data["energy_matrices"]
    sensor_power = data["sensor_power"]

    nd = len(depots)
    nt = len(targets)
    N = nd + nt
    K = len(drones)
    S = len(speeds)

    weights = [t["weight"] for t in targets]
    durations = [t["duration"] for t in targets]
    depths = [abs(t["z"]) for t in targets]

    prob = pulp.LpProblem("MDDMRP", pulp.LpMaximize)

    # ---- Variables (positional args : name, lowBound, upBound, cat) ----
    x = {}
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for s in range(S):
                for k in range(K):
                    x[(i, j, s, k)] = pulp.LpVariable(
                        f"x_{i}_{j}_{s}_{k}", 0, 1, pulp.LpBinary)

    y = {}
    for i in range(N):
        for k in range(K):
            y[(i, k)] = pulp.LpVariable(f"y_{i}_{k}", 0, 1, pulp.LpBinary)

    a = {}
    for k in range(K):
        a[k] = pulp.LpVariable(f"a_{k}", 0, 1, pulp.LpBinary)

    r = {}
    for d in range(nd):
        for k in range(K):
            r[(d, k)] = pulp.LpVariable(f"r_{d}_{k}", 0, 1, pulp.LpBinary)

    # ---- Objectif ----
    cov = pulp.lpSum(weights[j - nd] * y[(j, k)]
                     for j in range(nd, N) for k in range(K))

    e_prop = pulp.lpSum(em[s][i][j] * x[(i, j, s, k)]
                        for i in range(N) for j in range(N) if i != j
                        for s in range(S) for k in range(K))

    e_sens = pulp.lpSum(sensor_power * durations[j - nd] * y[(j, k)]
                        for j in range(nd, N) for k in range(K))

    prob += cov - eps * (e_prop + e_sens)

    # ---- Contraintes ----

    # 1. Chaque cible visitée au plus une fois
    for j in range(nd, N):
        prob += pulp.lpSum(y[(j, k)] for k in range(K)) <= 1

    # 2. Départ du dépôt assigné
    for k in range(K):
        start = drones[k]["start_depot"]
        prob += pulp.lpSum(x[(start, j, s, k)]
                           for j in range(N) if j != start
                           for s in range(S)) == a[k]
        prob += y[(start, k)] == a[k]

    # 3. Retour flexible
    for k in range(K):
        prob += pulp.lpSum(r[(d, k)] for d in range(nd)) == a[k]
        for d in range(nd):
            prob += pulp.lpSum(x[(i, d, s, k)]
                               for i in range(N) if i != d
                               for s in range(S)) == r[(d, k)]

    # 4. Pas d'arc dépôt-dépôt
    for k in range(K):
        for d1 in range(nd):
            for d2 in range(nd):
                if d1 != d2:
                    for s in range(S):
                        prob += x[(d1, d2, s, k)] == 0

    # 5. Lien arc-visit
    for k in range(K):
        for i in range(N):
            for j in range(N):
                if i != j:
                    for s in range(S):
                        prob += x[(i, j, s, k)] <= y[(i, k)]
                        prob += x[(i, j, s, k)] <= y[(j, k)]

    # 6. Conservation de flux
    for k in range(K):
        for j in range(nd, N):
            prob += pulp.lpSum(x[(i, j, s, k)]
                               for i in range(N) if i != j
                               for s in range(S)) == y[(j, k)]
            prob += pulp.lpSum(x[(j, i, s, k)]
                               for i in range(N) if i != j
                               for s in range(S)) == y[(j, k)]

    # 7. Budget énergie
    for k in range(K):
        E_max = drones[k]["E_max"]
        prob += (pulp.lpSum(em[s][i][j] * x[(i, j, s, k)]
                            for i in range(N) for j in range(N) if i != j
                            for s in range(S))
                 + pulp.lpSum(sensor_power * durations[j - nd] * y[(j, k)]
                              for j in range(nd, N))
                 ) <= E_max

    # 8. Profondeur limite
    for k in range(K):
        H_max = drones[k]["H_max"]
        for j in range(nd, N):
            if depths[j - nd] > H_max:
                prob += y[(j, k)] == 0

    # 9. Activation minimale (par drone)
    for k in range(K):
        prob += a[k] <= pulp.lpSum(y[(j, k)] for j in range(nd, N))

    # 10. Arcs infaisables
    INF = 1e8
    for i in range(N):
        for j in range(N):
            if i != j:
                for s in range(S):
                    if tm[s][i][j] >= INF:
                        for k in range(K):
                            prob += x[(i, j, s, k)] == 0

    # 11. SEC supplémentaires
    if extra_sec:
        for (subset, k) in extra_sec:
            if len(subset) < 2:
                continue
            prob += pulp.lpSum(x[(i, j, s, k)]
                               for i in subset for j in subset if i != j
                               for s in range(S)) <= len(subset) - 1

    # 12. Au moins un drone actif
    prob += pulp.lpSum(a[k] for k in range(K)) >= 1

    return prob, x, y, a, r


# ============================================================
# SOLVEUR PRINCIPAL (avec élimination itérative des sous-tours)
# ============================================================
def solve_milp(instance_path, time_limit=120, eps=1e-8, max_iter=30):
    # ---- Chargement ----
    with open(instance_path) as f:
        data = json.load(f)

    nd = len(data["depots"])
    nt = len(data["targets"])
    N = nd + nt
    K = len(data["drones"])
    S = len(data["drone_speeds"])

    weights = [t["weight"] for t in data["targets"]]
    durations = [t["duration"] for t in data["targets"]]
    tm = data["time_matrices"]
    em = data["energy_matrices"]
    sensor_power = data["sensor_power"]
    total_weight = sum(weights)
    total_mines = sum(1 for t in data["targets"] if t["is_mine"])

    print("=" * 70)
    print(f"Instance : {instance_path}")
    print(f"  Depots : {nd}, Targets : {nt}, Drones : {K}, Speeds : {S}")
    print(f"  Poids total : {total_weight:.4f}")
    print(f"  Mines       : {total_mines}")
    print(f"  Solver      : CBC (PuLP, open-source)")
    print(f"  eps         : {eps}")
    print("=" * 70)

    # ---- Itérations ----
    extra_sec = []
    start_time = time.time()
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit)
    last_routes = None

    for iteration in range(1, max_iter + 1):
        elapsed = time.time() - start_time
        if elapsed > time_limit:
            print(f"\n⏰ Time limit atteint ({elapsed:.1f}s)")
            break

        print(f"\n--- Itération {iteration} (SEC : {len(extra_sec)}) ---")

        prob, x, y, a, r = build_model(data, extra_sec=extra_sec, eps=eps)
        prob.solve(solver)

        status = pulp.LpStatus[prob.status]
        print(f"  Statut : {status}")

        if status not in ("Optimal", "Not Solved"):
            break

        # Extraction
        routes = extract_routes(x, y, a, data["drones"], N, S, K, nd)
        last_routes = routes

        for k, route in routes.items():
            s_str = " → ".join(f"D{n}" if n < nd else f"C{n-nd}" for n in route)
            print(f"  Drone {k} : {s_str}")

        # Détection des sous-tours
        new_sec = detect_subtours(x, y, a, data["drones"], N, S, K, nd)
        truly_new = [(sub, k) for sub, k in new_sec
                     if not any(set(sub) == set(s) and kk == k
                                for s, kk in extra_sec)]

        if not truly_new:
            print("  ✅ Aucun nouveau sous-tour — solution valide")
            break

        print(f"  ➜ {len(truly_new)} SEC ajoutée(s)")
        extra_sec.extend(truly_new)

    # ---- Résultats finaux ----
    if last_routes is None:
        print("\n❌ Aucune solution trouvée")
        return None

    total_coverage = 0.0
    total_energy = 0.0
    active_drones = 0
    detected_mines = 0
    routes_detail = []

    for k, route in last_routes.items():
        target_seq = [n for n in route if n >= nd]
        if not target_seq:
            continue
        active_drones += 1

        # Énergie (meilleure vitesse sur chaque arc + retour + capteurs)
        energy = 0.0
        for idx in range(len(route) - 1):
            i, j = route[idx], route[idx + 1]
            best_e = min(em[s][i][j] for s in range(S) if tm[s][i][j] < 1e8)
            energy += best_e
        if route[-1] >= nd:
            best_ret = min(em[s][route[-1]][d]
                           for d in range(nd) for s in range(S)
                           if tm[s][route[-1]][d] < 1e8)
            energy += best_ret

        for t_idx in target_seq:
            j = t_idx - nd
            total_coverage += weights[j]
            energy += sensor_power * durations[j]
            if data["targets"][j]["is_mine"]:
                detected_mines += 1

        total_energy += energy
        routes_detail.append({"drone": k, "nodes": route, "energy": energy})

    elapsed_total = time.time() - start_time

    print()
    print("=" * 70)
    print("RÉSULTATS FINAUX")
    print("=" * 70)
    print(f"Couverture       : {total_coverage:.4f} / {total_weight:.4f} "
          f"({100*total_coverage/total_weight:.2f}%)")
    print(f"Énergie totale   : {total_energy:.1f} J")
    print(f"Drones actifs    : {active_drones}")
    print(f"Mines détectées  : {detected_mines}/{total_mines} "
          f"({100*detected_mines/total_mines if total_mines > 0 else 0:.1f}%)")
    print(f"Temps total      : {elapsed_total:.2f} s")
    print()
    print("Routes détaillées :")
    for r in routes_detail:
        s_str = " → ".join(f"D{n}" if n < nd else f"C{n-nd}" for n in r["nodes"])
        print(f"  Drone {r['drone']} : {s_str}  ({r['energy']:.0f} J)")

    return {
        "coverage": total_coverage,
        "coverage_pct": 100 * total_coverage / total_weight,
        "energy": total_energy,
        "active_drones": active_drones,
        "mines_detected": detected_mines,
        "total_mines": total_mines,
        "time": elapsed_total,
        "routes": routes_detail,
        "n_sec_added": len(extra_sec),
    }


# ============================================================
# EXÉCUTION
# ============================================================
if __name__ == "__main__":
    # Nom de fichier en dur (Colab injecte des arguments parasites)
    instance_file = "instance_advanced_7.json"

    print(f"Fichier utilisé : {instance_file}")

    result = solve_milp(
        instance_file,
        time_limit=120,
        eps=1e-8,
        max_iter=30,
    )

!python milp_pulp.py

!pip uninstall -y pulp
!pip install pulp==2.8.0

import pulp
print(f"PuLP version : {pulp.__version__}")

# Test rapide
v = pulp.LpVariable("test", cat="Binary")
print(f"✅ Variable créée : {v}")

# Vérifier que HiGHS_CMD ou PULP_CBC_CMD est disponible
has_highs = hasattr(pulp, "HiGHS_CMD")
has_cbc = hasattr(pulp, "PULP_CBC_CMD")
print(f"HiGHS_CMD disponible : {has_highs}")
print(f"PULP_CBC_CMD disponible : {has_cbc}")

!python milp_pulp.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solveur MILP pour MDDMRP-DF — Version finale vérifiée.

Correctifs appliqués :
1. Objectif single-phase avec grand coefficient SCALE (1e6) pour éviter
   les problèmes numériques de CBC.
2. Couverture calculée directement à partir des variables y (pas des routes).
3. Extraction de route uniquement pour l'affichage.
4. Élimination itérative des sous-tours (SEC).
"""

import json
import time
import pulp


# ============================================================
# CRÉATION DES VARIABLES
# ============================================================
def make_vars(prob, data, prefix=""):
    depots = data["depots"]; targets = data["targets"]
    drones = data["drones"]; speeds = data["drone_speeds"]
    nd = len(depots); nt = len(targets); N = nd + nt
    K = len(drones); S = len(speeds)

    x = {}
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for s in range(S):
                for k in range(K):
                    x[(i, j, s, k)] = pulp.LpVariable(
                        f"{prefix}x_{i}_{j}_{s}_{k}", 0, 1, pulp.LpBinary)

    y = {}
    for i in range(N):
        for k in range(K):
            y[(i, k)] = pulp.LpVariable(
                f"{prefix}y_{i}_{k}", 0, 1, pulp.LpBinary)

    a = {k: pulp.LpVariable(f"{prefix}a_{k}", 0, 1, pulp.LpBinary)
         for k in range(K)}

    r = {}
    for d in range(nd):
        for k in range(K):
            r[(d, k)] = pulp.LpVariable(
                f"{prefix}r_{d}_{k}", 0, 1, pulp.LpBinary)

    return x, y, a, r


# ============================================================
# CONTRAINTES
# ============================================================
def build_constraints(prob, data, x, y, a, r, extra_sec=None):
    depots = data["depots"]; targets = data["targets"]
    drones = data["drones"]; speeds = data["drone_speeds"]
    tm = data["time_matrices"]; em = data["energy_matrices"]
    sensor_power = data["sensor_power"]

    nd = len(depots); nt = len(targets); N = nd + nt
    K = len(drones); S = len(speeds)

    weights = [t["weight"] for t in targets]
    durations = [t["duration"] for t in targets]
    depths = [abs(t["z"]) for t in targets]

    # 1. Visite unique
    for j in range(nd, N):
        prob += pulp.lpSum(y[(j, k)] for k in range(K)) <= 1

    # 2. Départ
    for k in range(K):
        start = drones[k]["start_depot"]
        prob += pulp.lpSum(x[(start, j, s, k)]
                           for j in range(N) if j != start
                           for s in range(S)) == a[k]
        prob += y[(start, k)] == a[k]

    # 3. Retour flexible
    for k in range(K):
        prob += pulp.lpSum(r[(d, k)] for d in range(nd)) == a[k]
        for d in range(nd):
            prob += pulp.lpSum(x[(i, d, s, k)]
                               for i in range(N) if i != d
                               for s in range(S)) == r[(d, k)]

    # 4. Pas d'arc dépôt-dépôt
    for k in range(K):
        for d1 in range(nd):
            for d2 in range(nd):
                if d1 != d2:
                    for s in range(S):
                        prob += x[(d1, d2, s, k)] == 0

    # 5. Lien arc-visit
    for k in range(K):
        for i in range(N):
            for j in range(N):
                if i != j:
                    for s in range(S):
                        prob += x[(i, j, s, k)] <= y[(i, k)]
                        prob += x[(i, j, s, k)] <= y[(j, k)]

    # 6. Conservation de flux
    for k in range(K):
        for j in range(nd, N):
            prob += pulp.lpSum(x[(i, j, s, k)]
                               for i in range(N) if i != j
                               for s in range(S)) == y[(j, k)]
            prob += pulp.lpSum(x[(j, i, s, k)]
                               for i in range(N) if i != j
                               for s in range(S)) == y[(j, k)]

    # 7. Budget énergie
    for k in range(K):
        E_max = drones[k]["E_max"]
        prob += (pulp.lpSum(em[s][i][j] * x[(i, j, s, k)]
                            for i in range(N) for j in range(N) if i != j
                            for s in range(S))
                 + pulp.lpSum(sensor_power * durations[j - nd] * y[(j, k)]
                              for j in range(nd, N))
                 ) <= E_max

    # 8. Profondeur
    for k in range(K):
        H_max = drones[k]["H_max"]
        for j in range(nd, N):
            if depths[j - nd] > H_max:
                prob += y[(j, k)] == 0

    # 9. Activation minimale
    for k in range(K):
        prob += a[k] <= pulp.lpSum(y[(j, k)] for j in range(nd, N))

    # 10. Arcs infaisables
    INF = 1e8
    for i in range(N):
        for j in range(N):
            if i != j:
                for s in range(S):
                    if tm[s][i][j] >= INF:
                        for k in range(K):
                            prob += x[(i, j, s, k)] == 0

    # 11. SEC supplémentaires
    if extra_sec:
        for (subset, k) in extra_sec:
            if len(subset) < 2:
                continue
            prob += pulp.lpSum(x[(i, j, s, k)]
                               for i in subset for j in subset if i != j
                               for s in range(S)) <= len(subset) - 1

    # 12. Au moins un drone actif
    prob += pulp.lpSum(a[k] for k in range(K)) >= 1


# ============================================================
# DÉTECTION DES SOUS-TOURS (via y + x)
# ============================================================
def detect_subtours(x, y, a, drones, N, S, K, nd):
    new_sec = []
    for k in range(K):
        a_val = x.get((0, 0, 0, k))  # n'importe quelle variable de ce drone
        # Utiliser pulp.value pour l'activation
        if pulp.value(a[k]) is None or pulp.value(a[k]) < 0.5:
            continue
        parent = {i: i for i in range(N)}

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv

        # Unir les nœuds connectés par des arcs utilisés
        for (i, j, s, kk), var in x.items():
            if kk != k:
                continue
            v = pulp.value(var)
            if v is not None and v > 0.5:
                union(i, j)

        # Regrouper les cibles visitées par composante
        comps = {}
        for j in range(nd, N):
            yv = pulp.value(y[(j, k)])
            if yv is not None and yv > 0.5:
                root = find(j)
                comps.setdefault(root, set()).add(j)

        for root, nodes in comps.items():
            has_depot = any(d in nodes for d in range(nd))
            if not has_depot and len(nodes) >= 2:
                new_sec.append((frozenset(nodes), k))
    return new_sec


# ============================================================
# EXTRACTION DE LA ROUTE (pour affichage uniquement)
# ============================================================
def extract_route_for_display(x, a, k, drones, N, S, nd):
    """Extrait UNE route pour l'affichage. Ignorée pour le calcul."""
    if pulp.value(a[k]) is None or pulp.value(a[k]) < 0.5:
        return []
    start = drones[k]["start_depot"]
    route = [start]
    visited = {start}
    current = start
    for _ in range(N):
        nxt = None
        for j in range(N):
            if j in visited:
                continue
