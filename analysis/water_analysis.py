# Water consumption analysis module
import pandas as pd
import numpy as np
from utils import (
    load_csv_data,
    detect_anomalies,
    identify_night_time_usage,
    get_trend_direction
)

class WaterAnalyzer:
    """Analyze water consumption patterns"""
    
    def __init__(self, csv_path, threshold_percentile=75):
        """
        Initialize analyzer
        
        Args:
            csv_path: Path to water CSV
            threshold_percentile: Anomaly threshold
        """
        self.data = load_csv_data(csv_path)
        self.threshold_percentile = threshold_percentile
        self.threshold = None
        self.anomalies = None
        
    def analyze(self):
        """
        Comprehensive water analysis
        
        Returns:
            Dictionary with analysis results
        """
        if self.data is None or len(self.data) == 0:
            return {"error": "No data available"}
        
        # Detect anomalies
        self.data, self.threshold = detect_anomalies(
            self.data.copy(),
            'consumption_gallons',
            self.threshold_percentile
        )
        
        # Identify night-time usage
        self.data = identify_night_time_usage(self.data)
        
        # Calculate statistics
        total_consumption = self.data['consumption_gallons'].sum()
        avg_consumption = self.data['consumption_gallons'].mean()
        peak_consumption = self.data['consumption_gallons'].max()
        night_consumption = self.data[self.data['is_night_time']]['consumption_gallons'].sum()
        anomaly_count = self.data['is_anomaly'].sum()
        
        # Trend analysis
        trend = get_trend_direction(self.data['consumption_gallons'])
        
        # Facility-wise analysis
        facility_analysis = self._facility_wise_analysis()
        
        # Leak detection
        leak_indicators = self._detect_potential_leaks()
        
        results = {
            'total_consumption_gallons': round(total_consumption, 2),
            'average_consumption_gallons': round(avg_consumption, 2),
            'peak_consumption_gallons': round(peak_consumption, 2),
            'night_consumption_gallons': round(night_consumption, 2),
            'anomalies_detected': int(anomaly_count),
            'anomaly_threshold': round(self.threshold, 2),
            'consumption_trend': trend,
            'facility_analysis': facility_analysis,
            'potential_leaks': leak_indicators,
            'anomaly_percentage': round((anomaly_count / len(self.data)) * 100, 2)
        }
        
        return results
    
    def _facility_wise_analysis(self):
        """Analyze consumption by facility"""
        facilities = {}
        for facility in self.data['facility'].unique():
            facility_data = self.data[self.data['facility'] == facility]
            facilities[facility] = {
                'total_gallons': round(facility_data['consumption_gallons'].sum(), 2),
                'avg_gallons': round(facility_data['consumption_gallons'].mean(), 2),
                'anomalies': int(facility_data['is_anomaly'].sum())
            }
        return facilities
    
    def _detect_potential_leaks(self):
        """Detect potential water leaks or anomalies"""
        anomaly_data = self.data[self.data['is_anomaly']]
        sustained_high = anomaly_data.groupby('facility').size()
        
        leak_risk_facilities = sustained_high[sustained_high > 5].index.tolist()
        
        return {
            'high_anomaly_count': int(len(anomaly_data)),
            'facilities_at_risk': leak_risk_facilities,
            'leak_probability': 'HIGH' if len(leak_risk_facilities) > 0 else 'LOW',
            'recommended_inspection': leak_risk_facilities
        }
    
    def get_anomalies_dataframe(self):
        """Get dataframe of anomalies"""
        return self.data[self.data['is_anomaly']].sort_values('consumption_gallons', ascending=False)
