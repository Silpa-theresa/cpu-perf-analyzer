import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/perf_counters.csv')

features = ['ipc', 'cache_miss_rate', 'branch_miss_rate']
X = df[features].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.05, random_state=42, n_estimators=100)
df['anomaly_score'] = model.fit_predict(X_scaled)
df['raw_score'] = model.score_samples(X_scaled)
df['is_anomaly'] = df['anomaly_score'] == -1

anomalies = df[df['is_anomaly']]
normal = df[~df['is_anomaly']]

print(f"Total runs: {len(df)}")
print(f"Anomalies detected: {len(anomalies)} ({100*len(anomalies)/len(df):.1f}%)")
print(f"\nAnomalous runs by workload:")
print(anomalies['workload'].value_counts())
print(f"\nAnomaly IPC range: {anomalies['ipc'].min():.3f} - {anomalies['ipc'].max():.3f}")
print(f"Normal IPC range:  {normal['ipc'].min():.3f} - {normal['ipc'].max():.3f}")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
threshold = df['raw_score'].quantile(0.05)  # bottom 5% = flagged, matches contamination=0.05
print(f"\nAlert threshold (raw_score): {threshold:.4f}")
print("\n--- ALERTS ---")
for _, row in df[df['is_anomaly']].iterrows():
    baseline_ipc = df[df['workload'] == row['workload']]['ipc'].mean()
    pct_diff = 100 * (row['ipc'] - baseline_ipc) / baseline_ipc
    direction = "below" if pct_diff < 0 else "above"
    print(f"ALERT: Run {row['run_id']} ({row['workload']}) — IPC {row['ipc']:.3f} is {abs(pct_diff):.1f}% {direction} workload baseline")

plt.figure(figsize=(10, 4))
colors = df['is_anomaly'].map({True: 'red', False: 'steelblue'})
plt.scatter(df['run_id'], df['raw_score'], c=colors, s=15)
plt.axhline(threshold, color='gray', linestyle='--', label='Alert threshold')
plt.xlabel('Run ID')
plt.ylabel('Anomaly score (lower = more anomalous)')
plt.title('Anomaly Score Trend with Alert Threshold')
plt.legend()
plt.tight_layout()
plt.savefig('results/alert_dashboard.png', dpi=150, bbox_inches='tight')
print("\nSaved results/alert_dashboard.png")
for i, feat in enumerate(features):
    axes[i].scatter(normal['run_id'], normal[feat],
                    c='steelblue', alpha=0.5, s=15, label='Normal')
    axes[i].scatter(anomalies['run_id'], anomalies[feat],
                    c='red', alpha=0.9, s=40, marker='x', label='Anomaly', linewidths=2)
    axes[i].set_xlabel('Run ID')
    axes[i].set_ylabel(feat)
    axes[i].set_title(f'{feat} - anomalies flagged')
    axes[i].legend(fontsize=8)

plt.tight_layout()
plt.savefig('results/anomaly_detection.png', dpi=150, bbox_inches='tight')
print("\nSaved results/anomaly_detection.png")

df.to_csv('results/annotated_runs.csv', index=False)
print("Saved results/annotated_runs.csv")
