# Electricity consumption analysis module
import pandas as pd
import numpy as np
from utils import (
    load_csv_data, 
    detect_anomalies, 
    identify_night_time_usage,
    get_trend_direction
)

class ElectricityAnalyzer:
    """Analyze electricity consumption patterns"""
    
    def __init__(self, csv_path, threshold_percentile=75):
        """
        Initialize analyzer
        
        Args:
            csv_path: Path to electricity CSV
            threshold_percentile: Anomaly threshold
        """
        self.data = load_csv_data(csv_path)
        self.threshold_percentile = threshold_percentile
        self.threshold = None
        self.anomalies = None
        
    def analyze(self):
        """
        Comprehensive electricity analysis
        
        Returns:
            Dictionary with analysis results
        """
        if self.data is None or len(self.data) == 0:
            return {"error": "No data available"}
        
        # Detect anomalies
        self.data, self.threshold = detect_anomalies(
            self.data.copy(), 
            'consumption_kwh',
            self.threshold_percentile
        )
        
        # Identify night-time usage
        self.data = identify_night_time_usage(self.data)
        
        # Calculate statistics
        total_consumption = self.data['consumption_kwh'].sum()
        avg_consumption = self.data['consumption_kwh'].mean()
        peak_consumption = self.data['consumption_kwh'].max()
        night_consumption = self.data[self.data['is_night_time']]['consumption_kwh'].sum()
        anomaly_count = self.data['is_anomaly'].sum()
        
        # Trend analysis
        trend = get_trend_direction(self.data['consumption_kwh'])
        
        # Facility-wise analysis
        facility_analysis = self._facility_wise_analysis()
        
        # Night-time idle detection
        night_idle = self._detect_night_idle()
        
        results = {
            'total_consumption_kwh': round(total_consumption, 2),
            'average_consumption_kwh': round(avg_consumption, 2),
            'peak_consumption_kwh': round(peak_consumption, 2),
            'night_consumption_kwh': round(night_consumption, 2),
            'anomalies_detected': int(anomaly_count),
            'anomaly_threshold': round(self.threshold, 2),
            'consumption_trend': trend,
            'facility_analysis': facility_analysis,
            'night_idle_issues': night_idle,
            'anomaly_percentage': round((anomaly_count / len(self.data)) * 100, 2)
        }
        
        return results
    
    def _facility_wise_analysis(self):
        """Analyze consumption by facility"""
        facilities = {}
        for facility in self.data['facility'].unique():
            facility_data = self.data[self.data['facility'] == facility]
            facilities[facility] = {
                'total_kwh': round(facility_data['consumption_kwh'].sum(), 2),
                'avg_kwh': round(facility_data['consumption_kwh'].mean(), 2),
                'anomalies': int(facility_data['is_anomaly'].sum())
            }
        return facilities
    
    def _detect_night_idle(self):
        """Detect unnecessary consumption during night hours"""
        night_data = self.data[self.data['is_night_time']]
        high_night_usage = night_data[night_data['consumption_kwh'] > self.threshold]
        
        return {
            'high_night_consumption_count': int(len(high_night_usage)),
            'night_consumption_percentage': round((night_data['consumption_kwh'].sum() / self.data['consumption_kwh'].sum()) * 100, 2),
            'issue_severity': 'HIGH' if len(high_night_usage) > 10 else 'MEDIUM' if len(high_night_usage) > 5 else 'LOW'
        }
    
    def get_anomalies_dataframe(self):
        """Get dataframe of anomalies"""
        return self.data[self.data['is_anomaly']].sort_values('consumption_kwh', ascending=False)
