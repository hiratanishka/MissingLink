
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from benchmark_worst_case import run_worst_case


sizes = [1000, 10000, 100000]

results = [
    run_worst_case(size)
    for size in sizes
]

top10_times = [
    result["Top10Time"]
    for result in results
]

sort_times = [
    result["MergeSortTime"]
    for result in results
]

plt.figure(figsize=(8, 5))

plt.plot(
    sizes,
    top10_times,
    marker="o",
    label="Top 10 Search Pipeline"
)

plt.plot(
    sizes,
    sort_times,
    marker="s",
    label="Merge Sort Only"
)

plt.xlabel("Number of Records")
plt.ylabel("Execution Time (seconds)")
plt.title("MissingLink Worst-Case Performance")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "performance_graph.png",
    dpi=180
)

print("Graph saved: performance_graph.png")
