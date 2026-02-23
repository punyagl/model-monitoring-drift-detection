import pandas as pd
from scipy.stats import ks_2samp
import os
import matplotlib.pyplot as plt


def load_data(path):
    return pd.read_csv(path)


def plot_distribution(reference, current, column):

    plt.figure()

    plt.hist(reference[column], alpha=0.5, label="Reference", density=True)
    plt.hist(current[column], alpha=0.5, label="Current", density=True)

    plt.title(f"Distribution Comparison - {column}")
    plt.xlabel(column)
    plt.ylabel("Density")
    plt.legend()

    plt.show()


def save_report(results, project_root, drift_score, total_features, drifted_features):

    report_path = os.path.join(project_root, "report.txt")

    with open(report_path, "w") as f:

        f.write("DATA DRIFT REPORT\n")
        f.write("=================\n\n")

        for result in results:
            f.write(f"Column: {result['column']}\n")
            f.write(f"P-value: {result['p_value']:.4f}\n")
            f.write(f"{result['status']}\n\n")

        f.write("=================\n")
        f.write("SUMMARY\n")
        f.write("=================\n\n")

        f.write(f"Total features checked: {total_features}\n")
        f.write(f"Features with drift: {drifted_features}\n")
        f.write(f"Drift Score: {drift_score:.2f}%\n")

    print(f"\nReport saved at: {report_path}")


def detect_drift(reference, current, project_root, threshold=0.05):

    feature_columns = reference.columns.drop("pass")

    results = []

    drift_count = 0
    total_features = len(feature_columns)

    for column in feature_columns:

        stat, p_value = ks_2samp(reference[column], current[column])

        print(f"\nColumn: {column}")
        print(f"P-value: {p_value:.4f}")

        if p_value < threshold:
            status = "Drift detected"
            drift_count += 1
        else:
            status = "No drift"

        print(status)

        results.append({
            "column": column,
            "p_value": p_value,
            "status": status
        })

        plot_distribution(reference, current, column)

    drift_score = (drift_count / total_features) * 100

    print("\n========== SUMMARY ==========")
    print(f"Total features: {total_features}")
    print(f"Drifted features: {drift_count}")
    print(f"Drift Score: {drift_score:.2f}%")

    save_report(results, project_root, drift_score, total_features, drift_count)


if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    ref_path = os.path.join(project_root, "data", "reference.csv")
    curr_path = os.path.join(project_root, "data", "current.csv")

    reference_data = load_data(ref_path)
    current_data = load_data(curr_path)

    detect_drift(reference_data, current_data, project_root)