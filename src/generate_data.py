import numpy as np
import pandas as pd

np.random.seed(42)
n = 200

workloads = ['matrix_mul', 'linked_list', 'fft', 'memcpy', 'sort']
data = []

for i in range(n):
    wl = np.random.choice(workloads)
    if wl == 'matrix_mul':
        ipc = np.random.normal(2.8, 0.15)
        cache_miss = np.random.normal(0.02, 0.005)
        branch_miss = np.random.normal(0.03, 0.008)
    elif wl == 'linked_list':
        ipc = np.random.normal(0.6, 0.1)
        cache_miss = np.random.normal(0.45, 0.05)
        branch_miss = np.random.normal(0.05, 0.01)
    elif wl == 'fft':
        ipc = np.random.normal(2.1, 0.2)
        cache_miss = np.random.normal(0.08, 0.02)
        branch_miss = np.random.normal(0.04, 0.01)
    elif wl == 'memcpy':
        ipc = np.random.normal(1.2, 0.1)
        cache_miss = np.random.normal(0.25, 0.04)
        branch_miss = np.random.normal(0.01, 0.003)
    else:  # sort
        ipc = np.random.normal(1.8, 0.15)
        cache_miss = np.random.normal(0.12, 0.03)
        branch_miss = np.random.normal(0.15, 0.02)

    if np.random.random() < 0.05:
        ipc *= np.random.choice([0.3, 2.5])
        cache_miss *= np.random.choice([5.0, 0.1])

    data.append({
        'run_id': i,
        'workload': wl,
        'ipc': round(max(0.1, ipc), 4),
        'cache_miss_rate': round(min(1.0, max(0.001, cache_miss)), 4),
        'branch_miss_rate': round(min(1.0, max(0.001, branch_miss)), 4),
        'cycles': int(np.random.uniform(1e6, 1e8)),
        'instructions': 0
    })

df = pd.DataFrame(data)
df['instructions'] = (df['ipc'] * df['cycles']).astype(int)
df.to_csv('data/perf_counters.csv', index=False)
print(f"Generated {len(df)} samples across {df['workload'].nunique()} workloads")
print(df.describe().round(3))