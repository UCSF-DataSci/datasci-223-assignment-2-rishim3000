import polars as pl

def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.
    
    Args:
        input_file: Path to the input CSV file
        
    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Convert CSV to Parquet for efficient processing
    pl.read_csv(input_file).write_parquet("patients_large.parquet")
    
    # Create a lazy query to analyze cohorts
    cohort_results = pl.scan_parquet("patients_large.parquet").pipe(
        lambda df: df.filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))
    ).pipe(
        lambda df: df.select(["BMI", "Glucose", "Age"])
    ).pipe(
        lambda df: df.with_columns(
            pl.when(pl.col("BMI") < 18.5).then(pl.lit('Underweight'))
            .when(pl.col("BMI") < 25).then(pl.lit("Normal"))
            .when(pl.col("BMI") < 30).then(pl.lit("Overweight"))
            .otherwise(pl.lit("Obese"))
            .alias("bmi_range")

        )
    ).pipe(
        lambda df: df.group_by("bmi_range").agg([
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.count().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
    ).collect(streaming=True)
    
    return cohort_results

def main():
    # Input file
    input_file = "patients_large.csv"
    
    # Run analysis
    results = analyze_patient_cohorts(input_file)
    
    # Print summary statistics
    print("\nCohort Analysis Summary:")
    print(results)

if __name__ == "__main__":
    main() 