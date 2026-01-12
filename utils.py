# Utility functions for EcoSense AI
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import ELECTRICITY_THRESHOLD_PERCENTILE, WATER_THRESHOLD_PERCENTILE, NIGHT_TIME_HOURS

def load_csv_data(file_path):
    """
    Load CSV data safely with error handling
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        DataFrame with parsed dates
    """
    try:
        df = pd.read_csv(file_path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def detect_anomalies(data, column, threshold_percentile=75):
    """
    Detect anomalies using percentile-based method
    
    Args:
        data: DataFrame
        column: Column to analyze
        threshold_percentile: Percentile threshold
        
    Returns:
        DataFrame with anomaly flags
    """
    threshold = data[column].quantile(threshold_percentile / 100)
    data['is_anomaly'] = data[column] > threshold
    data['anomaly_severity'] = (data[column] - data[column].mean()) / data[column].std()
    return data, threshold

def identify_night_time_usage(data):
    """
    Identify usage during night hours (10 PM - 5 AM)
    
    Args:
        data: DataFrame with datetime column
        
    Returns:
        DataFrame with night usage flags
    """
    data['hour'] = pd.to_datetime(data['date']).dt.hour
    data['is_night_time'] = data['hour'].isin(NIGHT_TIME_HOURS)
    return data

def calculate_daily_stats(data, value_column):
    """
    Calculate daily statistics
    
    Args:
        data: DataFrame
        value_column: Column to aggregate
        
    Returns:
        Daily aggregated DataFrame
    """
    data['date'] = pd.to_datetime(data['date']).dt.date
    daily = data.groupby('date').agg({
        value_column: ['sum', 'mean', 'min', 'max', 'std']
    }).reset_index()
    return daily

def get_trend_direction(series):
    """
    Determine if trend is increasing or decreasing
    
    Args:
        series: Pandas Series
        
    Returns:
        String: 'increasing', 'decreasing', or 'stable'
    """
    if len(series) < 2:
        return 'insufficient_data'
    
    first_half = series[:len(series)//2].mean()
    second_half = series[len(series)//2:].mean()
    
    diff_percent = ((second_half - first_half) / first_half) * 100 if first_half != 0 else 0
    
    if diff_percent > 5:
        return 'increasing'
    elif diff_percent < -5:
        return 'decreasing'
    else:
        return 'stable'

def format_sustainability_report(facility, data_type, anomalies, threshold, trend):
    """
    Format data into sustainability report
    
    Args:
        facility: Facility name
        data_type: 'electricity' or 'water'
        anomalies: Anomalous records count
        threshold: Threshold value
        trend: Trend direction
        
    Returns:
        Formatted report string
    """
    report = f"""
    ==================================================
    SUSTAINABILITY ANALYSIS REPORT
    ==================================================
    Facility: {facility}
    Resource Type: {data_type.upper()}
    Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Anomalies Detected: {anomalies}
    Alert Threshold: {threshold:.2f}
    Trend: {trend.upper()}
    ==================================================
    """
    return report

def save_insights(insights_text, output_file):
    """
    Save insights to file
    
    Args:
        insights_text: Text to save
        output_file: Output file path
    """
    try:
        with open(output_file, 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(insights_text)
            f.write("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error saving insights: {e}")
