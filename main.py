#!/usr/bin/env python3
"""
EcoSense AI - Main Entry Point
Initializes sample data and runs the Streamlit dashboard
"""

import os
import sys
import subprocess
from data_generator import generate_electricity_data, generate_water_data
from config import DATA_DIR

def setup_sample_data():
    """Generate sample data if not already present"""
    electricity_path = os.path.join(DATA_DIR, "electricity.csv")
    water_path = os.path.join(DATA_DIR, "water.csv")
    
    if not os.path.exists(electricity_path) or not os.path.exists(water_path):
        print("📊 Generating sample data...")
        generate_electricity_data(days=90, output_dir=DATA_DIR)
        generate_water_data(days=90, output_dir=DATA_DIR)
        print("✅ Sample data generated successfully!")
    else:
        print("✅ Sample data already exists")

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching EcoSense AI Dashboard...")
    print("📊 Dashboard will open at: http://localhost:8501")
    
    try:
        subprocess.run([
            "streamlit", "run", "app.py",
            "--logger.level=info"
        ], check=True)
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it:")
        print("   pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✋ Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════╗
    ║   🌱 EcoSense AI - Sustainability System   ║
    ║   Invisible Resource Loss Detection         ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Setup sample data
    setup_sample_data()
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()
