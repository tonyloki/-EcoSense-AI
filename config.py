# Configuration management for EcoSense AI
import os
from dotenv import load_dotenv

load_dotenv()

# IBM Watsonx Configuration
IBM_API_KEY = os.getenv("IBM_WATSONX_API_KEY", "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# Model Configuration
MODEL_ID = os.getenv("MODEL_ID", "ibm/granite-13b-instruct-v2")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Data Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
RAG_DIR = os.path.join(os.path.dirname(__file__), "rag")

# Anomaly Detection Thresholds
ELECTRICITY_THRESHOLD_PERCENTILE = 75  # Flag consumption above 75th percentile
WATER_THRESHOLD_PERCENTILE = 75
NIGHT_TIME_HOURS = [22, 23, 0, 1, 2, 3, 4, 5]  # 10 PM - 5 AM

# System Configuration
LOG_FILE = os.path.join(OUTPUT_DIR, "system.log")
INSIGHTS_FILE = os.path.join(OUTPUT_DIR, "insights_log.txt")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RAG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
