import os
import pandas as pd
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


def load_data(path):
    return pd.read_csv(path)


def plot_distribution(reference, current, column, project_root):
    plt.figure()

    plt.hist(reference[column], alpha=0.5, label="Reference", bins=10)
    plt.hist(current[column], alpha=0.5, label="Current", bins=10)

    plt.legend()
    plt.title(f"Distribution Comparison: {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plots_dir = os.path.join(project_root, "plots")

    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    plt.savefig(os.path.join(plots_dir, f"{column}.png"))
    plt.close()


def save_report(results, drift_score, project_root):

    report_path = os.path.join(project_root, "report.txt")

    with open(report_path, "w") as f:

        f.write("DATA DRIFT REPORT\n")
        f.write("====================\n\n")

        for r in results:
            f.write(f"Column: {r['column']}\n")
            f.write(f"P-value: {r['p_value']:.4f}\n")
            f.write(f"{r['status']}\n\n")

        f.write("====================\n")
        f.write(f"DRIFT SCORE: {drift_score:.2f}%\n")

    print(f"\nReport saved at: {report_path}")


def detect_drift(reference, current, project_root, threshold=0.05):

    results = []

    drift_count = 0
    total_columns = 0

    numeric_columns = reference.select_dtypes(include=['number']).columns

    for column in numeric_columns:

        if column == "pass":
            continue

        stat, p_value = ks_2samp(reference[column], current[column])

        status = "No drift"

        if p_value < threshold:
            status = "Drift detected"
            drift_count += 1

        total_columns += 1

        print(f"\nColumn: {column}")
        print(f"P-value: {p_value:.4f}")
        print(status)

        results.append({
            "column": column,
            "p_value": p_value,
            "status": status
        })

        plot_distribution(reference, current, column, project_root)

    drift_score = (drift_count / total_columns) * 100

    print(f"\nDRIFT SCORE: {drift_score:.2f}%")

    save_report(results, drift_score, project_root)


if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    ref_path = os.path.join(project_root, "data", "reference.csv")
    curr_path = os.path.join(project_root, "data", "current.csv")

    reference_data = load_data(ref_path)
    current_data = load_data(curr_path)

    detect_drift(reference_data, current_data, project_root)