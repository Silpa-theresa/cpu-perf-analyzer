import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

df = pd.read_csv('data/perf_counters.csv')

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 2, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])
workloads = df['workload'].unique()
ipc_data = [df[df['workload'] == w]['ipc'].values for w in workloads]
ax1.boxplot(ipc_data, labels=workloads, patch_artist=True)
ax1.set_title('IPC Distribution by Workload')
ax1.set_ylabel('IPC')
ax1.tick_params(axis='x', rotation=30)

ax2 = fig.add_subplot(gs[0, 1])
colors = plt.cm.tab10(np.linspace(0, 1, len(workloads)))
for i, wl in enumerate(workloads):
    sub = df[df['workload'] == wl]
    ax2.scatter(sub['cache_miss_rate'], sub['ipc'],
                label=wl, alpha=0.6, s=20, color=colors[i])
ax2.set_xlabel('Cache Miss Rate')
ax2.set_ylabel('IPC')
ax2.set_title('Cache Miss Rate vs IPC')
ax2.legend(fontsize=8)

ax3 = fig.add_subplot(gs[1, 0])
for i, wl in enumerate(workloads):
    sub = df[df['workload'] == wl]
    ax3.scatter(sub['branch_miss_rate'], sub['ipc'],
                label=wl, alpha=0.6, s=20, color=colors[i])
ax3.set_xlabel('Branch Miss Rate')
ax3.set_ylabel('IPC')
ax3.set_title('Branch Misprediction vs IPC')
ax3.legend(fontsize=8)

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(df['run_id'], df['ipc'], alpha=0.4, linewidth=0.8, color='steelblue')
ax4.set_xlabel('Run ID')
ax4.set_ylabel('IPC')
ax4.set_title('IPC Across All Runs (anomalies visible as spikes)')

plt.tight_layout()
plt.savefig('results/performance_analysis.png', dpi=150, bbox_inches='tight')
print("Saved results/performance_analysis.png")

print("\nMean IPC per workload:")
print(df.groupby('workload')['ipc'].mean().round(3))
print("\nMean cache miss rate per workload:")
print(df.groupby('workload')['cache_miss_rate'].mean().round(4))