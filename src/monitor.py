import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp


def load_data(path):
    return pd.read_csv(path)


def plot_distribution(reference, current, column, project_root):
    plt.figure()

    plt.hist(reference[column], alpha=0.5, label="Reference")
    plt.hist(current[column], alpha=0.5, label="Current")

    plt.title(f"Distribution Comparison: {column}")
    plt.legend()

    plots_dir = os.path.join(project_root, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    plot_path = os.path.join(plots_dir, f"{column}.png")
    plt.savefig(plot_path)
    plt.close()


def save_report(results, drift_score, project_root):
    report_path = os.path.join(project_root, "report.txt")

    with open(report_path, "w") as f:

        f.write("DATA DRIFT REPORT\n")
        f.write("====================\n\n")

        for result in results:
            f.write(f"Column: {result['column']}\n")
            f.write(f"P-value: {result['p_value']:.4f}\n")
            f.write(f"Status: {result['status']}\n\n")

        f.write("====================\n")
        f.write(f"DRIFT SCORE: {drift_score:.2f}%\n")

    print("Report saved at:", report_path)


def detect_drift(reference, current, project_root, threshold=0.05):

    results = []
    drift_count = 0
    total_columns = 0

    for column in reference.columns:

        if column == "pass":
            continue

        total_columns += 1

        ref_values = reference[column]
        curr_values = current[column]

        statistic, p_value = ks_2samp(ref_values, curr_values)

        if p_value < threshold:
            status = "Drift detected"
            drift_count += 1
        else:
            status = "No drift"

        print("\nColumn:", column)
        print("P-value:", round(p_value, 4))
        print(status)

        results.append({
            "column": column,
            "p_value": p_value,
            "status": status
        })

        plot_distribution(reference, current, column, project_root)

    drift_score = (drift_count / total_columns) * 100

    print("\nDRIFT SCORE:", round(drift_score, 2), "%")

    save_report(results, drift_score, project_root)


if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    ref_path = os.path.join(project_root, "data", "reference.csv")
    curr_path = os.path.join(project_root, "data", "current.csv")

    reference_data = load_data(ref_path)
    current_data = load_data(curr_path)

    detect_drift(reference_data, current_data, project_root)