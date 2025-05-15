#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os
import pdb
import pandas as pd
import sys

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Failed to load data')
        sys.exit(1)

def clean_patient_data(patients):
    """
    Clean patient data using pandas:
    - Capitalize names
    - Convert ages to integers
    - Filter out patients under 18
    - Remove duplicates

    Args:
        patients (list): List of patient dictionaries

    Returns:
        list: Cleaned list of patient dictionaries
    """

    df = pd.DataFrame(patients)

    # BUG: Limit to required columns
    # FIX: Fill missing columns if necessary
    required_columns = ['name', 'age', 'gender', 'diagnosis']
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
 
    # BUG: Duplicates need to be dropped
    # FIX: Drop duplicates
    df = df.drop_duplicates()

    # BUG: Underage patients not filtered out
    # FIX: Filter out underage (>18) patients
    df  = df[df['age'] >= 18]

    # BUG: Age strings not always valid integers
    # FIX: Convert to numeric, NaNs filled with 0
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # BUG: Names are not capitalized
    # FIX: Capitalize name
    df['name'] = df['name'].fillna('').apply(lambda x: x.title())

    return df.to_dict(orient = 'records')

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    # Load the patient data
    patients = load_patient_data(data_path)
    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)

    if not cleaned_patients:
        print("No valid patient records found.")
        return []
    
    # Print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        print(f"Name: {patient['name']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()