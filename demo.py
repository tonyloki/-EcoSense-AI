"""
EcoSense AI - Quick Start Guide

This script provides an interactive way to explore EcoSense AI without the dashboard.
"""

from analysis.electricity_analysis import ElectricityAnalyzer
from analysis.water_analysis import WaterAnalyzer
from ibm_ai.granite_llm import GraniteLLM
from rag.retriever import PolicyRetriever
from data_generator import generate_electricity_data, generate_water_data
from config import DATA_DIR
import os

def interactive_demo():
    """Run interactive demo"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║    EcoSense AI - Interactive Demo          ║
    ║    Sustainability Analysis & Insights      ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # Check for data
    electricity_path = os.path.join(DATA_DIR, "electricity.csv")
    water_path = os.path.join(DATA_DIR, "water.csv")
    
    if not os.path.exists(electricity_path) or not os.path.exists(water_path):
        print("📊 Generating sample data...")
        generate_electricity_data(days=90, output_dir=DATA_DIR)
        generate_water_data(days=90, output_dir=DATA_DIR)
        print("✅ Sample data ready!\n")
    
    while True:
        print("\n📋 Select Analysis:")
        print("1. Electricity Analysis")
        print("2. Water Analysis")
        print("3. Combined Analysis")
        print("4. AI Insights")
        print("5. Policy Search")
        print("6. Exit")
        
        choice = input("\nYour choice (1-6): ").strip()
        
        if choice == "1":
            electricity_demo()
        elif choice == "2":
            water_demo()
        elif choice == "3":
            combined_demo()
        elif choice == "4":
            ai_insights_demo()
        elif choice == "5":
            policy_search_demo()
        elif choice == "6":
            print("\n👋 Thank you for using EcoSense AI!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def electricity_demo():
    """Demonstrate electricity analysis"""
    print("\n⚡ ELECTRICITY CONSUMPTION ANALYSIS\n")
    
    try:
        electricity_path = os.path.join(DATA_DIR, "electricity.csv")
        analyzer = ElectricityAnalyzer(electricity_path)
        results = analyzer.analyze()
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        print(f"Total Consumption: {results['total_consumption_kwh']:,.2f} kWh")
        print(f"Average: {results['average_consumption_kwh']:.2f} kWh")
        print(f"Peak: {results['peak_consumption_kwh']:.2f} kWh")
        print(f"Night-time Usage: {results['night_consumption_kwh']:.2f} kWh")
        print(f"Anomalies Detected: {results['anomalies_detected']}")
        print(f"Trend: {results['consumption_trend'].upper()}")
        print(f"\nNight-time Analysis:")
        print(f"  - Consumption: {results['night_idle_issues']['night_consumption_percentage']:.1f}% of total")
        print(f"  - High usage events: {results['night_idle_issues']['high_night_consumption_count']}")
        print(f"  - Severity: {results['night_idle_issues']['issue_severity']}")
        print(f"\nFacility Breakdown:")
        for facility, data in results['facility_analysis'].items():
            print(f"  {facility}:")
            print(f"    - Total: {data['total_kwh']:,.2f} kWh")
            print(f"    - Average: {data['avg_kwh']:.2f} kWh")
            print(f"    - Anomalies: {data['anomalies']}")
    
    except Exception as e:
        print(f"Error in analysis: {e}")

def water_demo():
    """Demonstrate water analysis"""
    print("\n💧 WATER CONSUMPTION ANALYSIS\n")
    
    try:
        water_path = os.path.join(DATA_DIR, "water.csv")
        analyzer = WaterAnalyzer(water_path)
        results = analyzer.analyze()
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        print(f"Total Consumption: {results['total_consumption_gallons']:,.2f} gallons")
        print(f"Average: {results['average_consumption_gallons']:.2f} gallons/hour")
        print(f"Peak: {results['peak_consumption_gallons']:.2f} gallons")
        print(f"Night-time Usage: {results['night_consumption_gallons']:.2f} gallons")
        print(f"Anomalies Detected: {results['anomalies_detected']}")
        print(f"Trend: {results['consumption_trend'].upper()}")
        print(f"\nLeak Detection:")
        leak_info = results['potential_leaks']
        print(f"  - Leak Probability: {leak_info['leak_probability']}")
        print(f"  - Anomaly Count: {leak_info['high_anomaly_count']}")
        if leak_info['recommended_inspection']:
            print(f"  - Facilities for Inspection: {', '.join(leak_info['recommended_inspection'])}")
        print(f"\nFacility Breakdown:")
        for facility, data in results['facility_analysis'].items():
            print(f"  {facility}:")
            print(f"    - Total: {data['total_gallons']:,.2f} gallons")
            print(f"    - Average: {data['avg_gallons']:.2f} gallons")
            print(f"    - Anomalies: {data['anomalies']}")
    
    except Exception as e:
        print(f"Error in analysis: {e}")

def combined_demo():
    """Demonstrate combined analysis"""
    print("\n📊 COMBINED SUSTAINABILITY ANALYSIS\n")
    
    try:
        electricity_path = os.path.join(DATA_DIR, "electricity.csv")
        water_path = os.path.join(DATA_DIR, "water.csv")
        
        elec_analyzer = ElectricityAnalyzer(electricity_path)
        water_analyzer = WaterAnalyzer(water_path)
        
        elec_results = elec_analyzer.analyze()
        water_results = water_analyzer.analyze()
        
        print("ELECTRICITY:")
        print(f"  Total: {elec_results['total_consumption_kwh']:,.0f} kWh")
        print(f"  Anomalies: {elec_results['anomalies_detected']}")
        print(f"  Trend: {elec_results['consumption_trend']}")
        
        print("\nWATER:")
        print(f"  Total: {water_results['total_consumption_gallons']:,.0f} gallons")
        print(f"  Anomalies: {water_results['anomalies_detected']}")
        print(f"  Leak Risk: {water_results['potential_leaks']['leak_probability']}")
        
        print("\n🎯 RECOMMENDATIONS:")
        print("  1. Investigate night-time electricity usage (idle equipment)")
        print("  2. Conduct leak inspection for flagged facilities")
        print("  3. Implement automated shutdown protocols")
        print("  4. Schedule staff training on conservation practices")
        print("  5. Establish monthly monitoring dashboard")
        
    except Exception as e:
        print(f"Error in analysis: {e}")

def ai_insights_demo():
    """Demonstrate AI insights"""
    print("\n🤖 AI-POWERED INSIGHTS\n")
    
    try:
        llm = GraniteLLM()
        
        prompt = """Based on typical college campus resource usage patterns:
        - Average daily electricity: 45,000 kWh
        - Night-time consumption: 18% of total
        - Water usage peaks: 8-9 AM and 6-7 PM
        - Detected anomalies: 12 in past 90 days
        
        Provide sustainability recommendations."""
        
        print("Generating insights...")
        insight = llm.generate(prompt)
        print("\n" + insight)
        
    except Exception as e:
        print(f"Error generating insight: {e}")

def policy_search_demo():
    """Demonstrate policy search"""
    print("\n📚 SUSTAINABILITY POLICIES & GUIDELINES\n")
    
    try:
        retriever = PolicyRetriever()
        
        query = input("Enter search query (e.g., 'energy efficiency'): ").strip()
        
        if not query:
            query = "energy efficiency"
        
        results = retriever.search_policies(query)
        
        print(f"\n📋 Results for '{query}':\n")
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. {result[:200]}...")
                print()
        else:
            print("No matching policies found.")
        
    except Exception as e:
        print(f"Error searching policies: {e}")

if __name__ == "__main__":
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
