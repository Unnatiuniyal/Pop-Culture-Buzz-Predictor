# notebooks/eda.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Config
# -----------------------------
DATA_PATH = "data/google_trends_clean.csv"
os.makedirs("docs/screenshots", exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df.set_index("date", inplace=True)
print("Shape:", df.shape)
print(df.head())

# -----------------------------
# Missing values
# -----------------------------
missing = df.isna().sum().sort_values(ascending=False)
print("\nMissing values per column:\n", missing)

# -----------------------------
# Descriptive stats
# -----------------------------
print("\nSummary statistics:\n", df.describe().T)

# -----------------------------
# Plot 1: Lineplot of all buzz
# -----------------------------
plt.figure(figsize=(16,6))
for col in df.columns:
    plt.plot(df.index, df[col], label=col, alpha=0.8)
plt.title("Buzz Over Time (All Keywords)")
plt.xlabel("Date")
plt.ylabel("Buzz (scaled)")
plt.legend(loc="center left", bbox_to_anchor=(1,0.5), ncol=2)
plt.tight_layout()
plt.savefig("docs/screenshots/eda_all_trends.png", dpi=150)
plt.show()

# -----------------------------
# Plot 2: Weekly Average
# -----------------------------
df_weekly = df.resample("W").mean()
plt.figure(figsize=(16,6))
for col in df_weekly.columns:
    plt.plot(df_weekly.index, df_weekly[col], label=col)
plt.title("Weekly Average Buzz")
plt.xlabel("Week")
plt.ylabel("Buzz (scaled)")
plt.legend(loc="center left", bbox_to_anchor=(1,0.5), ncol=2)
plt.tight_layout()
plt.savefig("docs/screenshots/eda_weekly_trends.png", dpi=150)
plt.show()

# -----------------------------
# Plot 3: Correlation heatmap
# -----------------------------
plt.figure(figsize=(12,8))
corr = df_weekly.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
plt.title("Correlation Heatmap (Weekly Buzz)")
plt.tight_layout()
plt.savefig("docs/screenshots/eda_correlation_heatmap.png", dpi=150)
plt.show()

# -----------------------------
# Plot 4: Distribution of buzz
# -----------------------------
df_melt = df.reset_index().melt(id_vars="date", var_name="artist", value_name="buzz")
plt.figure(figsize=(14,6))
sns.boxplot(x="artist", y="buzz", data=df_melt)
plt.xticks(rotation=45)
plt.title("Distribution of Buzz per Artist")
plt.tight_layout()
plt.savefig("docs/screenshots/eda_boxplot.png", dpi=150)
plt.show()

# -----------------------------
# Save summary report
# -----------------------------
with open("docs/screenshots/eda_summary.txt", "w") as f:
    f.write("Missing values:\n")
    f.write(str(missing))
    f.write("\n\nSummary statistics:\n")
    f.write(str(df.describe().T))

print("EDA complete! Plots and summary saved in docs/screenshots/")
