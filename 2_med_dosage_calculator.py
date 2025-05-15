#!/usr/bin/env python3
"""
Emergency Room Medication Calculator

This script calculates medication dosages for emergency room patients based on 
standard emergency protocols. It follows weight-based dosing guidelines for common 
emergency medications.

Dosing Formula:
    Base Dosage (mg) = Patient Weight (kg) × Medication Factor (mg/kg)
    Loading Dose (mg) = Base Dosage × 2 (for first dose only)

When to use Loading Doses:
    - Only for first doses of certain medications (e.g., antibiotics, anti-seizure meds)
    - Determined by 'is_first_dose' flag in the input
    - Some medications always use loading doses for first administration

Example:
    Patient: 70kg, Medication: epinephrine, Is First Dose: No
    Base Dosage = 70 kg × 0.01 mg/kg = 0.7 mg
    Final Dosage = 0.7 mg

    Patient: 70kg, Medication: amiodarone, Is First Dose: Yes
    Base Dosage = 70 kg × 5 mg/kg = 350 mg
    Loading Dose = 350 mg × 2 = 700 mg
    Final Dosage = 700 mg

Input Format:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "condition": "anaphylaxis",
        "is_first_dose": false,
        "allergies": ["penicillin"]
    }

Output:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "base_dosage": 0.7,
        "is_first_dose": false,
        "loading_dose_applied": false,
        "final_dosage": 0.7,
        "warnings": ["Monitor for arrhythmias"]
    }

Medication Factors (mg/kg):
    epinephrine:  0.01  (Anaphylaxis)
    amiodarone:   5.00  (Cardiac arrest)
    lorazepam:    0.05  (Seizures)
    fentanyl:     0.001 (Pain)
    ...
"""

import json
import os
import sys

# Dosage factors for different medications (mg per kg of body weight)
# These are standard dosing factors based on medical guidelines
DOSAGE_FACTORS = {
    "epinephrine": 0.01,  # Anaphylaxis
    "amiodarone": 5.00,   # Cardiac arrest
    "lorazepam": 0.05,    # Seizures
    "fentanyl": 0.001,    # Pain
    "lisinopril": 0.5,    # ACE inhibitor for blood pressure
    "metformin": 10.0,    # Diabetes medication
    "oseltamivir": 2.5,   # Antiviral for influenza
    "sumatriptan": 1.0,   # Migraine medication
    "albuterol": 0.1,     # Asthma medication
    "ibuprofen": 5.0,     # Pain/inflammation
    "sertraline": 1.5,    # Antidepressant
    "levothyroxine": 0.02 # Thyroid medication
}

# Medications that use loading doses for first administration
# BUG: Missing commas between list items
LOADING_DOSE_MEDICATIONS = [
    "amiodarone"
    "lorazepam"
    "fentanyl" #fentanyl spelled incorrectly
]

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: try except implemented below
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'File not found: {filepath}')
        sys.exit(1)

def calculate_dosage(patient):
    """
    Calculate medication dosage for a patient.
    
    Args:
        patient (dict): Patient dictionary with 'weight', 'medication', and 'is_first_dose' keys
        
    Returns:
        dict: Patient dictionary with added dosage information
    """
    # Create a copy of the patient data to avoid modifying the original
    patient_with_dosage = patient.copy()
    
    # Extract patient information
    # BUG: No check if the required keys exists
    #FIX: check if all keys are available, if not, error

    required_keys = ["weight", "medication", "is_first_dose"]
    if not all(key in patient_with_dosage for key in required_keys):
        print(f"Missing required fields in patient data: {patient_with_dosage}")
        return None
    
    weight = patient_with_dosage['weight']
    medication = patient_with_dosage['medication']
    is_first_dose = patient_with_dosage["is_first_dose"]

    # Get the medication factor
    # BUG: Adding 's' to medication name, which doesn't match DOSAGE_FACTORS keys
    # FIX: Removing 's' from medication name
    factor = DOSAGE_FACTORS.get(medication, 0)
    
    # Calculate base dosage
    # BUG: Using addition instead of multiplication
    #FIX: Change to multiplication
    base_dosage = weight * factor
    
    loading_dose_applied = False
    final_dosage = base_dosage
    # Apply loading dose if it's the first dose and the medication uses loading doses
    # BUG: Incorrect condition - should check if medication is in LOADING_DOSE_MEDICATIONS
    # BUG: Using addition instead of multiplication for loading dose
    # FIX: Have multiplication
    if is_first_dose and medication in LOADING_DOSE_MEDICATIONS:
        final_dosage = base_dosage * 2 #double base dosage
        loading_dose_applied = True

    # Add dosage information to the patient record
    patient_with_dosage['base_dosage'] = base_dosage
    patient_with_dosage['loading_dose_applied'] = loading_dose_applied
    patient_with_dosage['final_dosage'] = final_dosage
    
    # Add warnings based on medication
    warnings = []
    # BUG: Typos in medication names
    if medication == "epinephrine":
        warnings.append("Monitor for arrhythmias")
    elif medication == "amiodarone":
        warnings.append("Monitor for hypotension")
    elif medication == "fentanyl":
        warnings.append("Monitor for respiratory depression")
    
    patient_with_dosage['warnings'] = warnings
    
    return {
        **patient_with_dosage,
        "base_dosage": base_dosage,
        "loading_dose_applied": loading_dose_applied,
        "final_dosage": final_dosage,
        "warnings": warnings
    }

def calculate_all_dosages(patients):
    """
    Calculate dosages for all patients and sum the total.
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        tuple: (list of patient dicts with dosages, total medication needed)
    """
    total_medication = 0
    patients_with_dosages = []
    
    # Process all patients
    for patient in patients:
        # Calculate dosage for this patient
        result = calculate_dosage(patient)
        if result is not None:
            patients_with_dosages.append(result)
            total_medication += result.get('final_dosage', 0)
    
    return patients_with_dosages, total_medication

def main():
    """Main function to run the script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'raw', 'meds.json')

    patients = load_patient_data(data_path)
    patients_with_dosages, total_medication = calculate_all_dosages(patients)

    print("Medication Dosages:")
    for patient in patients_with_dosages:
        print(f"Name: {patient['name']}, Medication: {patient['medication']}, "
              f"Base Dosage: {patient['base_dosage']:.2f} mg, "
              f"Final Dosage: {patient['final_dosage']:.2f} mg")
        if patient['loading_dose_applied']:
            print("Loading dose applied")
        if patient['warnings']:
            print("Warnings: " + ", ".join(patient['warnings']))

    print(f"\nTotal medication needed: {total_medication:.2f} mg")

    return patients_with_dosages, total_medication


if __name__ == "__main__":
    main()