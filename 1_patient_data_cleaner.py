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
    with open(filepath, 'r') as file:
        return json.load(file)

def clean_patient_data(patients):
    """
    Clean and validate patient data.
    
    Args:
        data: Dictionary containing patient information
        
    Returns:
        Cleaned patient data dictionary
    """
    # TODO: Fix the bugs in this function
    # Hint: Look for these common issues:
    # 1. Type conversion errors (str vs int)
    # 2. Missing key checks
    # 3. Invalid value ranges
    # 4. Incorrect string operations
    
    # BUG: Add your bug description here
    # FIX: Add your fix description here
    
    return data

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    # BUG: No error handling for load_patient_data failure
    patients = load_patient_data(data_path)
    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)

    if not cleaned_patients:
        print("No valid patient records found.")
        return []
    
    # BUG: No check if cleaned_patients is None
    # Print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        # BUG: Using 'name' key but we changed it to 'nage'
        print(f"Name: {patient['name']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()