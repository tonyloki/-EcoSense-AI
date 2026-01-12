# EcoSense AI - Streamlit Dashboard
# Invisible Resource Loss Detection System for Sustainable Campuses

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Import custom modules
from analysis.electricity_analysis import ElectricityAnalyzer
from analysis.water_analysis import WaterAnalyzer
from ibm_ai.granite_llm import GraniteLLM
from rag.retriever import PolicyRetriever, RAGAnalyzer
from utils import load_csv_data, save_insights
from config import DATA_DIR, INSIGHTS_FILE
from logger_config import logger

# Page configuration
st.set_page_config(
    page_title="EcoSense AI - Sustainability Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #ffcccc;
        border-left: 4px solid #ff0000;
        padding: 1rem;
        border-radius: 0.3rem;
    }
    .alert-medium {
        background-color: #fff4cc;
        border-left: 4px solid #ff9900;
        padding: 1rem;
        border-radius: 0.3rem;
    }
    .alert-low {
        background-color: #ccffcc;
        border-left: 4px solid #00cc00;
        padding: 1rem;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'electricity_data' not in st.session_state:
    st.session_state.electricity_data = None
if 'water_data' not in st.session_state:
    st.session_state.water_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

def load_default_data():
    """Load default sample data"""
    electricity_path = os.path.join(DATA_DIR, "electricity.csv")
    water_path = os.path.join(DATA_DIR, "water.csv")
    
    if os.path.exists(electricity_path):
        st.session_state.electricity_data = load_csv_data(electricity_path)
    if os.path.exists(water_path):
        st.session_state.water_data = load_csv_data(water_path)

def main():
    """Main application"""
    
    # Header
    st.title("🌱 EcoSense AI")
    st.subheader("Invisible Resource Loss Detection System for Sustainable Campuses")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Select Page", [
            "📊 Dashboard",
            "⚡ Electricity Analysis",
            "💧 Water Analysis",
            "🤖 AI Insights",
            "📋 Report Generator",
            "ℹ️ About"
        ])
        
        st.divider()
        
        st.header("Data Management")
        if st.button("Load Sample Data"):
            load_default_data()
            st.success("Sample data loaded!")
        
        uploaded_electricity = st.file_uploader(
            "Upload Electricity CSV",
            type="csv",
            key="elec_upload"
        )
        
        uploaded_water = st.file_uploader(
            "Upload Water CSV",
            type="csv",
            key="water_upload"
        )
        
        if uploaded_electricity is not None:
            st.session_state.electricity_data = pd.read_csv(uploaded_electricity)
            st.success("Electricity data uploaded!")
        
        if uploaded_water is not None:
            st.session_state.water_data = pd.read_csv(uploaded_water)
            st.success("Water data uploaded!")
    
    # Routes
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "⚡ Electricity Analysis":
        show_electricity_analysis()
    elif page == "💧 Water Analysis":
        show_water_analysis()
    elif page == "🤖 AI Insights":
        show_ai_insights()
    elif page == "📋 Report Generator":
        show_report_generator()
    elif page == "ℹ️ About":
        show_about()

def show_dashboard():
    """Main dashboard view"""
    st.header("Campus Resource Dashboard")
    
    if st.session_state.electricity_data is None and st.session_state.water_data is None:
        st.info("📂 Please load data from the sidebar to begin analysis")
        if st.button("Load Sample Data Now"):
            load_default_data()
            st.rerun()
        return
    
    col1, col2 = st.columns(2)
    
    # Electricity Overview
    with col1:
        st.subheader("⚡ Electricity Consumption")
        if st.session_state.electricity_data is not None:
            analyzer = ElectricityAnalyzer(None)
            analyzer.data = st.session_state.electricity_data
            results = analyzer.analyze()
            
            if 'error' not in results:
                st.metric(
                    "Total Consumption",
                    f"{results['total_consumption_kwh']:,.0f} kWh",
                    f"Avg: {results['average_consumption_kwh']:.1f} kWh"
                )
                st.metric(
                    "Anomalies Detected",
                    results['anomalies_detected'],
                    f"{results['anomaly_percentage']:.1f}% of usage"
                )
                st.metric(
                    "Trend",
                    results['consumption_trend'].upper(),
                    "Night usage: " + str(round(results['night_consumption_kwh'], 0)) + " kWh"
                )
    
    # Water Overview
    with col2:
        st.subheader("💧 Water Consumption")
        if st.session_state.water_data is not None:
            analyzer = WaterAnalyzer(None)
            analyzer.data = st.session_state.water_data
            results = analyzer.analyze()
            
            if 'error' not in results:
                st.metric(
                    "Total Consumption",
                    f"{results['total_consumption_gallons']:,.0f} gal",
                    f"Avg: {results['average_consumption_gallons']:.1f} gal"
                )
                st.metric(
                    "Anomalies Detected",
                    results['anomalies_detected'],
                    f"{results['anomaly_percentage']:.1f}% of usage"
                )
                st.metric(
                    "Leak Risk",
                    results['potential_leaks']['leak_probability'],
                    f"Facilities at risk: {len(results['potential_leaks']['recommended_inspection'])}"
                )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.electricity_data is not None:
            st.subheader("Electricity by Facility")
            facility_elec = st.session_state.electricity_data.groupby('facility')['consumption_kwh'].sum().reset_index()
            fig = px.pie(
                facility_elec,
                values='consumption_kwh',
                names='facility',
                title="Electricity Distribution by Facility"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if st.session_state.water_data is not None:
            st.subheader("Water by Facility")
            facility_water = st.session_state.water_data.groupby('facility')['consumption_gallons'].sum().reset_index()
            fig = px.pie(
                facility_water,
                values='consumption_gallons',
                names='facility',
                title="Water Distribution by Facility"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Time series
    if st.session_state.electricity_data is not None:
        st.subheader("Electricity Consumption Over Time")
        elec_daily = st.session_state.electricity_data.groupby('date')['consumption_kwh'].sum().reset_index()
        fig = px.line(
            elec_daily,
            x='date',
            y='consumption_kwh',
            title="Daily Electricity Consumption",
            labels={'consumption_kwh': 'Consumption (kWh)', 'date': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)

def show_electricity_analysis():
    """Detailed electricity analysis"""
    st.header("⚡ Electricity Analysis")
    
    if st.session_state.electricity_data is None:
        st.warning("Please load electricity data first")
        return
    
    analyzer = ElectricityAnalyzer(None)
    analyzer.data = st.session_state.electricity_data
    results = analyzer.analyze()
    
    if 'error' in results:
        st.error(results['error'])
        return
    
    # Save results
    st.session_state.analysis_results['electricity'] = results
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total (kWh)", f"{results['total_consumption_kwh']:,.0f}")
    col2.metric("Average (kWh)", f"{results['average_consumption_kwh']:.1f}")
    col3.metric("Peak (kWh)", f"{results['peak_consumption_kwh']:.1f}")
    col4.metric("Anomalies", results['anomalies_detected'])
    
    st.divider()
    
    # Facility Analysis
    st.subheader("Facility-wise Breakdown")
    facility_df = pd.DataFrame(results['facility_analysis']).T
    st.dataframe(facility_df, use_container_width=True)
    
    # Night-time usage
    st.subheader("🌙 Night-time Usage Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Night Hours Consumption", f"{results['night_idle_issues']['night_consumption_percentage']:.1f}%")
    col2.metric("High Night Usage Events", results['night_idle_issues']['high_night_consumption_count'])
    col3.metric("Issue Severity", results['night_idle_issues']['issue_severity'])
    
    # Anomalies
    st.subheader("Anomaly Detection")
    anomalies_df = analyzer.get_anomalies_dataframe()
    if not anomalies_df.empty:
        st.write(f"Found {len(anomalies_df)} anomalies")
        st.dataframe(anomalies_df[['timestamp', 'facility', 'consumption_kwh', 'anomaly_severity']].head(20), use_container_width=True)
    else:
        st.success("No anomalies detected")
    
    # Charts
    fig = px.bar(
        facility_df.reset_index(),
        x='index',
        y='total_kwh',
        title="Total Consumption by Facility",
        labels={'index': 'Facility', 'total_kwh': 'Total (kWh)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_water_analysis():
    """Detailed water analysis"""
    st.header("💧 Water Analysis")
    
    if st.session_state.water_data is None:
        st.warning("Please load water data first")
        return
    
    analyzer = WaterAnalyzer(None)
    analyzer.data = st.session_state.water_data
    results = analyzer.analyze()
    
    if 'error' in results:
        st.error(results['error'])
        return
    
    # Save results
    st.session_state.analysis_results['water'] = results
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total (gal)", f"{results['total_consumption_gallons']:,.0f}")
    col2.metric("Average (gal)", f"{results['average_consumption_gallons']:.1f}")
    col3.metric("Peak (gal)", f"{results['peak_consumption_gallons']:.1f}")
    col4.metric("Anomalies", results['anomalies_detected'])
    
    st.divider()
    
    # Leak Detection
    st.subheader("🚨 Leak Detection")
    leak_info = results['potential_leaks']
    
    if leak_info['leak_probability'] == 'HIGH':
        st.markdown("""<div class="alert-high">
            <strong>⚠️ HIGH LEAK RISK DETECTED</strong><br>
            Facilities recommended for immediate inspection
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="alert-low">
            <strong>✓ Low leak risk</strong><br>
            No immediate concerns detected
        </div>""", unsafe_allow_html=True)
    
    if leak_info['recommended_inspection']:
        st.write("**Facilities for Inspection:**")
        for facility in leak_info['recommended_inspection']:
            st.write(f"  • {facility}")
    
    # Facility Analysis
    st.subheader("Facility-wise Breakdown")
    facility_df = pd.DataFrame(results['facility_analysis']).T
    st.dataframe(facility_df, use_container_width=True)
    
    # Night-time usage
    st.subheader("🌙 Night-time Usage Analysis")
    col1, col2 = st.columns(2)
    col1.metric("Night Hours Consumption", f"{results['night_consumption_gallons']:,.0f} gal")
    col2.metric("Night Usage Percentage", f"{(results['night_consumption_gallons'] / results['total_consumption_gallons'] * 100):.1f}%")
    
    # Charts
    fig = px.bar(
        facility_df.reset_index(),
        x='index',
        y='total_gallons',
        title="Total Consumption by Facility",
        labels={'index': 'Facility', 'total_gallons': 'Total (gallons)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_ai_insights():
    """AI-powered insights using Granite LLM"""
    st.header("🤖 AI-Powered Sustainability Insights")
    
    if st.session_state.analysis_results == {}:
        st.info("Please run analysis first (Electricity or Water Analysis tabs)")
        return
    
    llm = GraniteLLM()
    rag = RAGAnalyzer()
    
    st.subheader("Generate AI Insights")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Electricity", "Water", "Combined"],
        key="insight_type"
    )
    
    if st.button("🚀 Generate Insights", key="generate_insights"):
        with st.spinner("Generating insights..."):
            try:
                if analysis_type == "Electricity":
                    if 'electricity' not in st.session_state.analysis_results:
                        st.error("Please run electricity analysis first")
                        return
                    
                    results = st.session_state.analysis_results['electricity']
                    prompt = f"""Analyze this electricity consumption data for a college campus:
                    
Total: {results['total_consumption_kwh']} kWh
Average: {results['average_consumption_kwh']} kWh
Peak: {results['peak_consumption_kwh']} kWh
Night usage: {results['night_consumption_kwh']} kWh ({results['night_idle_issues']['night_consumption_percentage']}%)
Anomalies: {results['anomalies_detected']} events
Trend: {results['consumption_trend']}

Provide:
1. Key findings about consumption patterns
2. Analysis of night-time usage (likely causes)
3. Facility-specific insights
4. Practical, low-cost recommendations
5. Expected impact if implemented"""
                    
                    insight = llm.generate(prompt)
                
                elif analysis_type == "Water":
                    if 'water' not in st.session_state.analysis_results:
                        st.error("Please run water analysis first")
                        return
                    
                    results = st.session_state.analysis_results['water']
                    prompt = f"""Analyze this water consumption data for a college campus:
                    
Total: {results['total_consumption_gallons']} gallons
Average: {results['average_consumption_gallons']} gal/hour
Peak: {results['peak_consumption_gallons']} gallons
Night usage: {results['night_consumption_gallons']} gallons
Anomalies: {results['anomalies_detected']} events
Leak Risk: {results['potential_leaks']['leak_probability']}

Provide:
1. Assessment of consumption patterns
2. Leak probability analysis
3. Explanation of anomalies
4. Water conservation recommendations
5. Priority areas for inspection"""
                    
                    insight = llm.generate(prompt)
                
                else:  # Combined
                    if 'electricity' not in st.session_state.analysis_results or 'water' not in st.session_state.analysis_results:
                        st.error("Please run both analyses first")
                        return
                    
                    elec = st.session_state.analysis_results['electricity']
                    water = st.session_state.analysis_results['water']
                    
                    prompt = f"""Generate a comprehensive sustainability report for a campus with:

ELECTRICITY:
- Total: {elec['total_consumption_kwh']} kWh
- Anomalies: {elec['anomalies_detected']} events
- Night usage: {elec['night_consumption_kwh']} kWh

WATER:
- Total: {water['total_consumption_gallons']} gallons
- Anomalies: {water['anomalies_detected']} events
- Leak Risk: {water['potential_leaks']['leak_probability']}

Provide:
1. Overall sustainability assessment
2. Cross-resource inefficiency patterns
3. Integrated recommendations
4. 30-day action plan
5. Expected cost savings"""
                    
                    insight = llm.generate(prompt)
                
                st.subheader("Generated Insight")
                st.write(insight)
                
                # Save insight
                save_insights(f"{analysis_type} Analysis Insight:\n{insight}", INSIGHTS_FILE)
                st.success("✓ Insight saved to insights log")
                
            except Exception as e:
                st.error(f"Error generating insight: {e}")
                logger.error(f"Insight generation error: {e}")
    
    st.divider()
    st.subheader("Policy-Grounded Recommendations")
    
    if st.button("📚 Retrieve Relevant Policies"):
        with st.spinner("Retrieving policies..."):
            if analysis_type == "Electricity":
                policies = rag.retriever.get_policy_context("electricity efficiency energy")
            elif analysis_type == "Water":
                policies = rag.retriever.get_policy_context("water conservation efficiency")
            else:
                policies = rag.retriever.get_policy_context("sustainability efficiency conservation")
            
            st.write(policies)

def show_report_generator():
    """Generate comprehensive reports"""
    st.header("📋 Sustainability Report Generator")
    
    if st.session_state.analysis_results == {}:
        st.warning("Please run analyses first")
        return
    
    st.subheader("Generate Executive Report")
    
    report_type = st.selectbox(
        "Report Type",
        ["Executive Summary", "Detailed Analysis", "Recommendations", "Full Report"]
    )
    
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            report_content = generate_report(report_type)
            st.markdown(report_content)
            
            # Download button
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=report_content,
                file_name=f"ecosense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

def generate_report(report_type):
    """Generate report based on type"""
    results = st.session_state.analysis_results
    
    if report_type == "Executive Summary":
        report = f"""# EcoSense AI - Executive Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
This report summarizes resource consumption patterns and sustainability inefficiencies detected on campus.

## Key Metrics
"""
        if 'electricity' in results:
            r = results['electricity']
            report += f"""
### Electricity
- Total Consumption: {r['total_consumption_kwh']:,.0f} kWh
- Anomalies: {r['anomalies_detected']} ({r['anomaly_percentage']:.1f}%)
- Trend: {r['consumption_trend'].upper()}
- Night Usage: {r['night_consumption_kwh']:.0f} kWh ({r['night_idle_issues']['night_consumption_percentage']:.1f}% of total)
"""
        
        if 'water' in results:
            r = results['water']
            report += f"""
### Water
- Total Consumption: {r['total_consumption_gallons']:,.0f} gallons
- Anomalies: {r['anomalies_detected']} ({r['anomaly_percentage']:.1f}%)
- Leak Risk: {r['potential_leaks']['leak_probability']}
"""
        
        report += f"""

## Recommendations
1. Conduct facility audit for night-time usage
2. Implement automated controls for non-critical systems
3. Schedule leak inspections
4. Establish monitoring dashboard
5. Train staff on conservation practices

## Responsible AI Note
This analysis uses aggregated, facility-level data only. No personal data is processed.
Recommendations support human decision-making; final decisions rest with administration.
"""
    
    else:
        report = "## Full Report\n\n"
        for analysis_type, data in results.items():
            report += f"### {analysis_type.upper()}\n"
            report += str(data) + "\n\n"
    
    return report

def show_about():
    """About page"""
    st.header("About EcoSense AI")
    
    st.markdown("""
### Project Overview
**EcoSense AI** is an intelligent decision-support system designed to identify invisible resource wastage on educational campuses.

### Problem Statement
Educational institutions consume vast amounts of electricity and water daily. However, a significant portion of this consumption is **unnoticed wastage** due to:
- Equipment left running unnecessarily
- Water leaks and continuous usage
- Inefficient operational patterns
- Lack of visibility into resource usage

### Solution
EcoSense AI combines:
- **Data Analysis**: Pattern detection and anomaly identification
- **AI Intelligence**: IBM Granite LLM for explainable insights
- **RAG Technology**: Policy-grounded recommendations
- **Responsible AI**: Privacy-first, transparent, ethical design

### Key Features
✅ Real-time consumption monitoring
✅ Anomaly and leak detection
✅ Night-time idle usage analysis
✅ AI-powered insights
✅ Policy-aligned recommendations
✅ Comprehensive reporting

### Alignment with SDGs
- **SDG 12**: Responsible Consumption and Production
- **SDG 11**: Sustainable Cities and Communities
- **SDG 13**: Climate Action

### Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python, Pandas, NumPy
- **AI**: IBM Granite LLM via Watsonx
- **RAG**: FAISS + Sentence Transformers
- **Visualization**: Plotly

### Responsible AI Principles
✓ **Fairness**: Aggregated data only, no personal information
✓ **Transparency**: Explains reasoning for all recommendations
✓ **Privacy**: No student/individual tracking
✓ **Ethics**: Recommendations support, not enforce, decisions

### Team
**Student Name**: Loki
**College**: [Your College Name]
**Project Type**: Internship Final Project

### Contact & Support
For questions or feedback, please contact the development team.

---
**EcoSense AI** - Making Campus Sustainability Visible and Actionable
    """)

if __name__ == "__main__":
    main()
