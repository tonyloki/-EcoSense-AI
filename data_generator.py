# Data generation for realistic campus resource usage patterns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_electricity_data(days=365, facilities=None, output_dir="data"):
    """
    Generate realistic electricity consumption data
    
    Args:
        days: Number of days of data
        facilities: List of facility names
        output_dir: Output directory
        
    Returns:
        DataFrame with electricity data
    """
    if facilities is None:
        facilities = [
            "Building A",
            "Building B",
            "Hostel Block C",
            "Lab Block D",
            "Library Block",
            "Sports Complex",
            "Cafeteria",
            "Administration"
        ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        
        for facility in facilities:
            # Base consumption pattern (higher during day, lower at night)
            for hour in range(24):
                # Time-based pattern
                if 6 <= hour < 22:  # Day time
                    base_consumption = np.random.normal(150, 20)
                else:  # Night time
                    base_consumption = np.random.normal(40, 10)
                
                # Day-of-week pattern (higher on weekdays)
                if current_date.weekday() < 5:  # Weekday
                    base_consumption *= 1.1
                
                # Random anomaly (10% chance of anomalous day)
                if np.random.random() < 0.1:
                    base_consumption *= np.random.uniform(1.3, 1.8)
                
                consumption_kwh = max(0, base_consumption)
                
                data.append({
                    'timestamp': current_date.replace(hour=hour),
                    'date': current_date.date(),
                    'hour': hour,
                    'consumption_kwh': round(consumption_kwh, 2),
                    'facility': facility,
                    'day_of_week': current_date.strftime('%A')
                })
    
    df = pd.DataFrame(data)
    csv_path = os.path.join(output_dir, "electricity.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated electricity data: {csv_path}")
    return df

def generate_water_data(days=365, facilities=None, output_dir="data"):
    """
    Generate realistic water consumption data
    
    Args:
        days: Number of days of data
        facilities: List of facility names
        output_dir: Output directory
        
    Returns:
        DataFrame with water data
    """
    if facilities is None:
        facilities = [
            "Building A",
            "Building B",
            "Hostel Block C",
            "Lab Block D",
            "Library Block",
            "Sports Complex",
            "Cafeteria",
            "Administration"
        ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        
        for facility in facilities:
            # Morning and evening peak (bathrooms, kitchens)
            for hour in range(24):
                if hour in [7, 8, 9, 18, 19, 20]:  # Peak hours
                    base_consumption = np.random.normal(80, 15)
                else:
                    base_consumption = np.random.normal(20, 5)
                
                # Occasional leaks (5% anomaly rate)
                if np.random.random() < 0.05:
                    base_consumption *= np.random.uniform(2.0, 3.5)
                
                consumption_gallons = max(0, base_consumption)
                
                data.append({
                    'timestamp': current_date.replace(hour=hour),
                    'date': current_date.date(),
                    'hour': hour,
                    'consumption_gallons': round(consumption_gallons, 2),
                    'facility': facility,
                    'day_of_week': current_date.strftime('%A')
                })
    
    df = pd.DataFrame(data)
    csv_path = os.path.join(output_dir, "water.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated water data: {csv_path}")
    return df

if __name__ == "__main__":
    # Generate larger sample data
    generate_electricity_data(days=365)
    generate_water_data(days=365)
    print("Sample data generation complete!")
