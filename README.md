# Model Monitoring and Drift Detection System

## Overview

This project implements a simple Machine Learning Model Monitoring system that detects data drift between reference data and current data using statistical methods.

Data drift occurs when the distribution of incoming data changes over time, which can reduce model performance. This system helps identify such changes early.

This is a core component of real-world ML production systems.

---

## Features

- Detects data drift using Kolmogorov-Smirnov statistical test
- Calculates overall Drift Score
- Generates visual distribution comparison plots
- Automatically creates drift report
- Clean modular Python project structure
- Portfolio-ready project

---

## Project Structure

---

## How It Works

The system:

1. Loads reference and current datasets
2. Compares distributions using KS test
3. Detects drift per feature
4. Calculates overall Drift Score
5. Generates plots and report

---

## Example Output
Column: hours_studied
P-value: 0.1379
No drift
Column: attendance
P-value: 0.0036
Drift detected
Column: previous_score
P-value: 0.0115
Drift detected
DRIFT SCORE: 66.67%

---

## Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib

---

## Why This Project Matters

Model monitoring is essential in real-world ML systems used by companies like:

- Netflix
- Amazon
- Google
- Uber

This project demonstrates understanding of ML production monitoring concepts.

---

## Future Improvements

- Email alerts for drift
- Dashboard visualization
- Real-time monitoring
- Integration with ML pipelines

---

## Author

GitHub: https://github.com/punyagl