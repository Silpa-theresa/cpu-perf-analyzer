# CPU Performance Counter Analyzer

A Python pipeline for ingesting CPU performance counter data, visualising microarchitectural behaviour, and automatically flagging anomalous runs using ML-based anomaly detection.

## What it does

- Ingests per-run CPU performance counters: IPC, cache miss rate, branch misprediction rate, cycle count, instruction count
- Visualises IPC distribution across workload types (matrix multiply, linked list traversal, FFT, memcpy, sort)
- Identifies correlations between cache/branch behaviour and IPC
- Applies Isolation Forest anomaly detection to flag runs with statistically unusual performance signatures

## Key findings from synthetic dataset (200 runs, 5 workloads)

| Workload | Mean IPC | Mean Cache Miss Rate | Characteristic |
|---|---|---|---|
| matrix_mul | ~2.8 | ~2% | ALU-bound, cache-friendly |
| linked_list | ~0.6 | ~45% | Memory-bound, pointer chasing |
| fft | ~2.1 | ~8% | Compute + moderate memory |
| memcpy | ~1.2 | ~25% | Bandwidth-bound |
| sort | ~1.8 | ~12% | Branch-heavy |

Anomaly detection (Isolation Forest, contamination=5%) correctly identified injected regressions with no labelled training data.

## Usage

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/analyze.py
python src/anomaly.py
```

## Results

![Performance Analysis](results/performance_analysis.png)
![Anomaly Detection](results/anomaly_detection.png)
