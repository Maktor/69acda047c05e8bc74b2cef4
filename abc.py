import json
import math
from statistics import mean, stdev

FILE_PATH = "6dpt-7w23.json"
START_FY = "FY2012-13"
END_FY = "FY2018-19"

allowed_fys = [
    "FY2012-13",
    "FY2013-14",
    "FY2014-15",
    "FY2015-16",
    "FY2016-17",
    "FY2017-18",
    "FY2018-19",
]

def fmt(x):
    """Format all displayed calculations to 10 decimal places."""
    return f"{x:.10f}"

def sample_cv_percent(values):
    """
    Coefficient of variation (CV) as a percentage:
    CV = (sample standard deviation / mean) * 100
    Returns a dictionary with all intermediate values.
    """
    n = len(values)
    mu = mean(values)
    
    deviations = [x - mu for x in values]
    squared_deviations = [d ** 2 for d in deviations]
    sum_squared_deviations = sum(squared_deviations)
    sample_variance = sum_squared_deviations / (n - 1)
    sample_std = math.sqrt(sample_variance)
    cv_percent = (sample_std / mu) * 100
    
    return {
        "n": n,
        "mean": mu,
        "deviations": deviations,
        "squared_deviations": squared_deviations,
        "sum_squared_deviations": sum_squared_deviations,
        "sample_variance": sample_variance,
        "sample_std": sample_std,
        "cv_percent": cv_percent
    }

with open(FILE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

filtered_rows = []

for row in data:
    if (
        row.get("department_name") == "ACADEMY OF SCIENCES"
        and row.get("measure_title") == "Number of visitors"
        and row.get("fiscal_year") in allowed_fys
        and row.get("full_year_result") not in (None, "", "null")
    ):
        filtered_rows.append(row)

fy_order = {fy: i for i, fy in enumerate(allowed_fys)}
filtered_rows.sort(key=lambda r: fy_order[r["fiscal_year"]])

mid_year_values = []
full_year_values = []

print("=" * 90)
print("FILTERED RECORDS USED IN THE CALCULATION")
print("=" * 90)

for row in filtered_rows:
    fy = row["fiscal_year"]
    mid_val = row.get("mid_year_result")
    full_val = row.get("full_year_result")

    mid_float = float(mid_val) if mid_val not in (None, "", "null") else None
    full_float = float(full_val) if full_val not in (None, "", "null") else None

    print(
        f"{fy}: "
        f"mid_year_result = {fmt(mid_float) if mid_float is not None else 'MISSING':>15}, "
        f"full_year_result = {fmt(full_float) if full_float is not None else 'MISSING':>15}"
    )

    if mid_float is not None:
        mid_year_values.append(mid_float)
    if full_float is not None:
        full_year_values.append(full_float)

print()
print("=" * 90)
print("MID-YEAR VALUES")
print("=" * 90)
for i, v in enumerate(mid_year_values, start=1):
    print(f"x{i} = {fmt(v)}")

print()
print("=" * 90)
print("FULL-YEAR VALUES")
print("=" * 90)
for i, v in enumerate(full_year_values, start=1):
    print(f"y{i} = {fmt(v)}")

mid_stats = sample_cv_percent(mid_year_values)

print()
print("=" * 90)
print("STEP-BY-STEP: CV OF MID-YEAR RESULTS")
print("=" * 90)
print(f"n = {mid_stats['n']}")
print(f"Mean of mid-year results = {fmt(mid_stats['mean'])}")

print("\nDeviations from mean:")
for i, d in enumerate(mid_stats["deviations"], start=1):
    print(f"x{i} - mean = {fmt(d)}")

print("\nSquared deviations:")
for i, sd in enumerate(mid_stats["squared_deviations"], start=1):
    print(f"(x{i} - mean)^2 = {fmt(sd)}")

print(f"\nSum of squared deviations = {fmt(mid_stats['sum_squared_deviations'])}")
print(f"Sample variance = Sum / (n - 1) = {fmt(mid_stats['sample_variance'])}")
print(f"Sample standard deviation = sqrt(sample variance) = {fmt(mid_stats['sample_std'])}")
print(f"CV of mid-year results (%) = (sample std / mean) * 100 = {fmt(mid_stats['cv_percent'])}")

full_stats = sample_cv_percent(full_year_values)

print()
print("=" * 90)
print("STEP-BY-STEP: CV OF FULL-YEAR RESULTS")
print("=" * 90)
print(f"n = {full_stats['n']}")
print(f"Mean of full-year results = {fmt(full_stats['mean'])}")

print("\nDeviations from mean:")
for i, d in enumerate(full_stats["deviations"], start=1):
    print(f"y{i} - mean = {fmt(d)}")

print("\nSquared deviations:")
for i, sd in enumerate(full_stats["squared_deviations"], start=1):
    print(f"(y{i} - mean)^2 = {fmt(sd)}")

print(f"\nSum of squared deviations = {fmt(full_stats['sum_squared_deviations'])}")
print(f"Sample variance = Sum / (n - 1) = {fmt(full_stats['sample_variance'])}")
print(f"Sample standard deviation = sqrt(sample variance) = {fmt(full_stats['sample_std'])}")
print(f"CV of full-year results (%) = (sample std / mean) * 100 = {fmt(full_stats['cv_percent'])}")

difference = mid_stats["cv_percent"] - full_stats["cv_percent"]

print()
print("=" * 90)
print("FINAL CALCULATION")
print("=" * 90)
print(f"Difference = CV(mid-year) - CV(full-year)")
print(f"Difference = {fmt(mid_stats['cv_percent'])} - {fmt(full_stats['cv_percent'])}")
print(f"Difference = {fmt(difference)}")

print()
print(f"Final Answer (rounded to 2 decimals): {difference:.2f}")
