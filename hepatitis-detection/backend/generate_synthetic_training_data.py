"""
Synthetic Hepatitis Training Data Generator
Generates medically realistic patient records for ML model training
with clear class separation between healthy and hepatitis-positive cases
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

def generate_negative_case():
    """
    Generate a healthy patient with normal liver function values
    Hepatitis Outcome = 0
    """
    case = {
        # Demographic
        'Age': np.random.randint(18, 80),
        'Sex': np.random.choice([0, 1]),  # 0=Male, 1=Female
        
        # Laboratory Values - NORMAL RANGES for healthy liver
        'Bilirubin': np.random.uniform(0.1, 1.2),
        'Alkaline_Phosphatase': np.random.uniform(44, 147),
        'SGOT_AST': np.random.uniform(10, 40),
        'SGPT_ALT': np.random.uniform(7, 56),
        'Albumin': np.random.uniform(3.5, 5.0),
        'Total_Proteins': np.random.uniform(6.0, 8.3),
        
        # Clinical Symptoms - Healthy patients rarely show these
        'Fatigue': np.random.choice([0, 1], p=[0.95, 0.05]),  # 5% chance (normal variation)
        'Malaise': np.random.choice([0, 1], p=[0.97, 0.03]),  # 3% chance
        'Anorexia': np.random.choice([0, 1], p=[0.96, 0.04]),  # 4% chance
        
        # Physical Examination - Normal
        'Liver_Big': np.random.choice([0, 1], p=[0.98, 0.02]),  # 2% chance (borderline normal)
        'Liver_Firm': np.random.choice([0, 1], p=[0.99, 0.01]),  # 1% chance
        'Spleen_Palpable': np.random.choice([0, 1], p=[0.95, 0.05]),  # 5% chance (can be normal)
        
        # Severe Findings - Absent in healthy patients
        'Ascites': 0,
        'Varices': 0,
        
        # Outcome
        'Outcome': 0  # Negative (Healthy)
    }
    return case

def generate_positive_case():
    """
    Generate a hepatitis-positive patient with elevated liver function markers
    Hepatitis Outcome = 1
    """
    # Determine severity level (mild, moderate, severe)
    severity = np.random.choice(['mild', 'moderate', 'severe'], p=[0.4, 0.4, 0.2])
    
    case = {
        # Demographic
        'Age': np.random.randint(20, 75),  # Slightly lower age range for active infection
        'Sex': np.random.choice([0, 1]),
        
        # Laboratory Values - ELEVATED for hepatitis
        'Bilirubin': np.random.uniform(1.5, 3.5) if severity == 'mild' else np.random.uniform(2.5, 6.0),
        'Alkaline_Phosphatase': np.random.uniform(150, 250) if severity == 'mild' else np.random.uniform(200, 400),
        'SGOT_AST': np.random.uniform(70, 150) if severity == 'mild' else np.random.uniform(150, 500),
        'SGPT_ALT': np.random.uniform(80, 160) if severity == 'mild' else np.random.uniform(160, 600),
        'Albumin': np.random.uniform(2.5, 3.4),  # Decreased
        'Total_Proteins': np.random.uniform(5.5, 6.5),  # Decreased
        
        # Clinical Symptoms - Expected in hepatitis
        'Fatigue': np.random.choice([0, 1], p=[0.15, 0.85]),  # 85% have fatigue
        'Malaise': np.random.choice([0, 1], p=[0.20, 0.80]),  # 80% have malaise
        'Anorexia': np.random.choice([0, 1], p=[0.25, 0.75]),  # 75% have anorexia
        
        # Physical Examination - Common in hepatitis
        'Liver_Big': np.random.choice([0, 1], p=[0.10, 0.90]),  # 90% have hepatomegaly
        'Liver_Firm': np.random.choice([0, 1], p=[0.20, 0.80]),  # 80% have liver firmness
        'Spleen_Palpable': np.random.choice([0, 1], p=[0.30, 0.70]),  # 70% have splenomegaly
        
        # Severe Findings - More common in moderate/severe cases
        'Ascites': 1 if severity in ['moderate', 'severe'] and np.random.random() < 0.6 else 0,
        'Varices': 1 if severity == 'severe' and np.random.random() < 0.5 else 0,
        
        # Outcome
        'Outcome': 1  # Positive (Hepatitis)
    }
    return case

def generate_dataset(n_samples=1000):
    """
    Generate balanced synthetic dataset
    n_samples: total number of samples (will be split 50-50 between classes)
    """
    samples = []
    
    # Generate negative cases
    for _ in range(n_samples // 2):
        samples.append(generate_negative_case())
    
    # Generate positive cases
    for _ in range(n_samples // 2):
        samples.append(generate_positive_case())
    
    # Create DataFrame
    df = pd.DataFrame(samples)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def validate_dataset(df):
    """
    Validate the generated dataset for medical realism and class separation
    """
    print("=" * 80)
    print("DATASET VALIDATION REPORT")
    print("=" * 80)
    
    print(f"\n📊 DATASET OVERVIEW")
    print(f"Total samples: {len(df)}")
    print(f"Negative cases (Healthy): {sum(df['Outcome'] == 0)} ({sum(df['Outcome'] == 0)/len(df)*100:.1f}%)")
    print(f"Positive cases (Hepatitis): {sum(df['Outcome'] == 1)} ({sum(df['Outcome'] == 1)/len(df)*100:.1f}%)")
    
    print(f"\n🔬 LABORATORY MARKERS - NEGATIVE CASES (Healthy)")
    negative_df = df[df['Outcome'] == 0]
    print(f"Bilirubin:               {negative_df['Bilirubin'].mean():.2f} ± {negative_df['Bilirubin'].std():.2f} mg/dL")
    print(f"SGOT (AST):              {negative_df['SGOT_AST'].mean():.2f} ± {negative_df['SGOT_AST'].std():.2f} U/L")
    print(f"SGPT (ALT):              {negative_df['SGPT_ALT'].mean():.2f} ± {negative_df['SGPT_ALT'].std():.2f} U/L")
    print(f"Alkaline Phosphatase:    {negative_df['Alkaline_Phosphatase'].mean():.2f} ± {negative_df['Alkaline_Phosphatase'].std():.2f} IU/L")
    print(f"Albumin:                 {negative_df['Albumin'].mean():.2f} ± {negative_df['Albumin'].std():.2f} g/dL")
    print(f"Total Proteins:          {negative_df['Total_Proteins'].mean():.2f} ± {negative_df['Total_Proteins'].std():.2f} g/dL")
    
    print(f"\n🔬 LABORATORY MARKERS - POSITIVE CASES (Hepatitis)")
    positive_df = df[df['Outcome'] == 1]
    print(f"Bilirubin:               {positive_df['Bilirubin'].mean():.2f} ± {positive_df['Bilirubin'].std():.2f} mg/dL")
    print(f"SGOT (AST):              {positive_df['SGOT_AST'].mean():.2f} ± {positive_df['SGOT_AST'].std():.2f} U/L")
    print(f"SGPT (ALT):              {positive_df['SGPT_ALT'].mean():.2f} ± {positive_df['SGPT_ALT'].std():.2f} U/L")
    print(f"Alkaline Phosphatase:    {positive_df['Alkaline_Phosphatase'].mean():.2f} ± {positive_df['Alkaline_Phosphatase'].std():.2f} IU/L")
    print(f"Albumin:                 {positive_df['Albumin'].mean():.2f} ± {positive_df['Albumin'].std():.2f} g/dL")
    print(f"Total Proteins:          {positive_df['Total_Proteins'].mean():.2f} ± {positive_df['Total_Proteins'].std():.2f} g/dL")
    
    print(f"\n⚕️ CLINICAL SYMPTOMS")
    print(f"{'Symptom':<20} {'Negative (%)':<15} {'Positive (%)':<15}")
    print("-" * 50)
    for symptom in ['Fatigue', 'Malaise', 'Anorexia']:
        neg_pct = (negative_df[symptom].sum() / len(negative_df) * 100)
        pos_pct = (positive_df[symptom].sum() / len(positive_df) * 100)
        print(f"{symptom:<20} {neg_pct:<15.1f} {pos_pct:<15.1f}")
    
    print(f"\n🔍 PHYSICAL EXAMINATION")
    print(f"{'Finding':<20} {'Negative (%)':<15} {'Positive (%)':<15}")
    print("-" * 50)
    for finding in ['Liver_Big', 'Liver_Firm', 'Spleen_Palpable', 'Ascites', 'Varices']:
        neg_pct = (negative_df[finding].sum() / len(negative_df) * 100)
        pos_pct = (positive_df[finding].sum() / len(positive_df) * 100)
        print(f"{finding:<20} {neg_pct:<15.1f} {pos_pct:<15.1f}")
    
    print(f"\n✅ CLASS SEPARATION QUALITY")
    print(f"Bilirubin ratio (Pos/Neg):     {positive_df['Bilirubin'].mean() / negative_df['Bilirubin'].mean():.2f}x")
    print(f"AST ratio (Pos/Neg):           {positive_df['SGOT_AST'].mean() / negative_df['SGOT_AST'].mean():.2f}x")
    print(f"ALT ratio (Pos/Neg):           {positive_df['SGPT_ALT'].mean() / negative_df['SGPT_ALT'].mean():.2f}x")
    
    print("\n" + "=" * 80)

def main():
    print("🧬 Generating high-quality synthetic hepatitis training dataset...")
    print("=" * 80)
    
    # Generate dataset with 1000 samples (500 negative, 500 positive)
    df = generate_dataset(n_samples=1000)
    
    # Validate and display statistics
    validate_dataset(df)
    
    # Save to CSV
    output_path = r"c:\new major\hepatitis-detection\backend\data\synthetic_training_data.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Dataset saved to: {output_path}")
    print(f"   Total records: {len(df)}")
    print(f"   Features: {len(df.columns)}")
    
    # Display sample records
    print("\n📋 SAMPLE RECORDS FROM DATASET")
    print("\nNegative Case Examples:")
    print(df[df['Outcome'] == 0].head(3).to_string())
    print("\nPositive Case Examples:")
    print(df[df['Outcome'] == 1].head(3).to_string())
    
    return df

if __name__ == "__main__":
    df = main()
