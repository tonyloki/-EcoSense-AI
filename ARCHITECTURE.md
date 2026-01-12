# Project Architecture & Developer Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)                     │
│           Dashboard • Reports • User Interaction             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐      ┌──────▼────────────┐
│  Data Analysis   │      │   AI Intelligence │
├──────────────────┤      ├───────────────────┤
│ • Electricity    │      │ • Granite LLM     │
│   Analyzer       │      │ • Prompt Eng.     │
│ • Water          │      │ • Mock Responses  │
│   Analyzer       │      │                   │
│ • Anomaly        │      └────────┬──────────┘
│   Detection      │               │
│ • Trend Analysis │      ┌────────▼─────────┐
└────────┬─────────┘      │  RAG System       │
         │                ├───────────────────┤
         │                │ • PolicyRetriever │
         │                │ • FAISS Search    │
         │                │ • Augmentation    │
         │                └────────┬──────────┘
         │                         │
    ┌────▼─────────────────────────▼────┐
    │     Core Utilities & Config         │
    ├────────────────────────────────────┤
    │ • config.py - Configuration        │
    │ • utils.py - Helper Functions      │
    │ • logger_config.py - Logging       │
    │ • data_generator.py - Synthetic    │
    └────────────────────────────────────┘
         │
    ┌────▼────────────────┐
    │   Data Layer         │
    ├──────────────────────┤
    │ • electricity.csv    │
    │ • water.csv          │
    │ • policy_docs.txt    │
    │ • insights_log.txt   │
    └──────────────────────┘
```

## 📁 Module Structure

### 1. **app.py** - Main Streamlit Application
```
Functions:
- main() - Main app router
- show_dashboard() - Overview dashboard
- show_electricity_analysis() - Detailed electricity analysis
- show_water_analysis() - Detailed water analysis
- show_ai_insights() - AI insight generation
- show_report_generator() - Report creation
- show_about() - Project information
```

**Dependencies**: streamlit, plotly, analysis modules, llm, rag

### 2. **analysis/** - Data Analysis Modules

#### electricity_analysis.py
```python
class ElectricityAnalyzer:
    - __init__(csv_path, threshold_percentile)
    - analyze() - Comprehensive analysis
    - _facility_wise_analysis() - By facility
    - _detect_night_idle() - Night usage detection
    - get_anomalies_dataframe() - Anomaly data
```

**Key Methods**:
- `analyze()`: Returns dict with consumption stats, anomalies, trends
- Detects anomalies > 75th percentile
- Tracks night-time (10 PM - 5 AM) consumption

#### water_analysis.py
```python
class WaterAnalyzer:
    - __init__(csv_path, threshold_percentile)
    - analyze() - Comprehensive analysis
    - _facility_wise_analysis() - By facility
    - _detect_potential_leaks() - Leak detection
    - get_anomalies_dataframe() - Anomaly data
```

**Key Methods**:
- `analyze()`: Returns dict with consumption, anomalies, leak risks
- Detects potential leaks through sustained anomalies
- Facilities with high anomaly counts flagged for inspection

### 3. **ibm_ai/** - AI Integration

#### granite_llm.py
```python
class GraniteLLM:
    - __init__(api_key, project_id)
    - generate(prompt, system_prompt, max_tokens)
    - analyze_sustainability(data_summary)
    - explain_anomaly(anomaly_description, context)
    - get_recommendations(analysis_summary, policies)
    - _generate_mock_response() - Fallback
```

**Features**:
- Connects to IBM Watsonx API
- Falls back to mock mode if credentials missing
- Supports system prompts and parameters
- Transparent reasoning for recommendations

#### prompt_templates.py
```
Constants:
- SYSTEM_PROMPT - Main system instruction
- ELECTRICITY_ANALYSIS_PROMPT - Electricity analysis template
- WATER_ANALYSIS_PROMPT - Water analysis template
- COMBINED_INSIGHTS_PROMPT - Multi-resource template
- POLICY_GROUNDED_PROMPT - Policy-aligned template
- EXPLANATION_PROMPT - Transparent reasoning template

Functions:
- format_electricity_prompt()
- format_water_prompt()
```

### 4. **rag/** - Retrieval-Augmented Generation

#### retriever.py
```python
class PolicyRetriever:
    - __init__(knowledge_base_path)
    - retrieve(query, top_k) - Main retrieval method
    - _retrieve_with_faiss(query, top_k)
    - _retrieve_with_keywords(query, top_k)
    - augment_prompt(user_prompt, query)
    - get_policy_context(topic)
    - search_policies(keyword)

class RAGAnalyzer:
    - __init__(knowledge_base_path)
    - ground_analysis_in_policies(analysis_data, type)
```

**Features**:
- FAISS embedding-based search (if available)
- Keyword fallback search
- Document chunking for better context
- Prompt augmentation with policy context

### 5. **config.py** - Configuration Management
```
Settings:
- IBM API credentials
- Model parameters
- Data directories
- Anomaly thresholds
- Night-time hours
- Logging configuration
```

### 6. **utils.py** - Utility Functions
```
Functions:
- load_csv_data() - Safe CSV loading
- detect_anomalies() - Percentile-based detection
- identify_night_time_usage() - Night hour flagging
- calculate_daily_stats() - Aggregation
- get_trend_direction() - Trend analysis
- format_sustainability_report() - Report generation
- save_insights() - Append to insights log
```

### 7. **logger_config.py** - Logging Setup
```
Features:
- File and console logging
- Consistent formatting
- Error tracking
- Debug support
```

### 8. **data_generator.py** - Synthetic Data Creation
```python
Functions:
- generate_electricity_data(days, facilities, output_dir)
- generate_water_data(days, facilities, output_dir)

Features:
- Realistic consumption patterns
- Time-based variation
- Weekday/weekend patterns
- Simulated anomalies
- Leak simulation
```

---

## 🔄 Data Flow

### 1. Data Analysis Flow
```
CSV Upload/Load
    ↓
CSV Parsing (utils.load_csv_data)
    ↓
Create Analyzer (ElectricityAnalyzer/WaterAnalyzer)
    ↓
Detect Anomalies (detect_anomalies)
    ↓
Identify Night Usage (identify_night_time_usage)
    ↓
Calculate Metrics (facility-wise, daily, trends)
    ↓
Return Results Dict
```

### 2. AI Insight Flow
```
Analysis Results
    ↓
Format Prompt (prompt_templates)
    ↓
Augment with RAG (retriever.augment_prompt)
    ↓
Call Granite LLM (granite_llm.generate)
    ↓
Receive Insight (with reasoning)
    ↓
Display & Save
```

### 3. Report Generation Flow
```
Select Report Type
    ↓
Compile Analysis Data
    ↓
Format Markdown Report
    ↓
Generate Visualizations
    ↓
Enable Download
```

---

## 🧪 Testing & Development

### Unit Testing Pattern
```python
from analysis.electricity_analysis import ElectricityAnalyzer

def test_electricity_analysis():
    analyzer = ElectricityAnalyzer('test_data.csv')
    results = analyzer.analyze()
    assert 'total_consumption_kwh' in results
    assert results['anomalies_detected'] >= 0
```

### Integration Testing
```bash
# Run demo for manual testing
python demo.py

# Test analysis module
python -c "from analysis.electricity_analysis import *"

# Test LLM
python -c "from ibm_ai.granite_llm import GraniteLLM; llm = GraniteLLM()"
```

---

## 🔐 Security Considerations

1. **API Keys**: Store in `.env`, never in code
2. **Data Privacy**: Only aggregated data processed
3. **File Access**: Validate file paths
4. **Input Validation**: Sanitize CSV data
5. **Error Handling**: Graceful degradation

---

## 🚀 Extension Points

### Add New Analysis Type
```python
# Create new analyzer class
class GasAnalyzer:
    def __init__(self, csv_path):
        self.data = load_csv_data(csv_path)
    
    def analyze(self):
        # Implementation
        return results
```

### Add New Data Source
```python
# Add to data_generator.py
def generate_gas_data(days=90):
    # Implementation
    pass
```

### Add New Report Type
```python
# Extend generate_report() in app.py
elif report_type == "Custom":
    report = generate_custom_report()
```

---

## 📊 Performance Considerations

### Optimization Tips
1. **Lazy loading**: Load data on demand
2. **Caching**: Use Streamlit @st.cache_data
3. **Aggregation**: Pre-compute daily/weekly stats
4. **Indexing**: FAISS for faster search
5. **Chunking**: Process data in batches

### Scalability
- Current design: ~90 days data, 4 facilities
- Scalable to: Multiple years, 100+ facilities
- Bottleneck: LLM API calls (implement caching)

---

## 🐛 Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```bash
# Test data loading
python -c "from utils import load_csv_data; df = load_csv_data('data/electricity.csv'); print(df.shape)"

# Test analysis
python -c "from analysis.electricity_analysis import ElectricityAnalyzer; a = ElectricityAnalyzer('data/electricity.csv'); print(a.analyze())"

# Test RAG
python -c "from rag.retriever import PolicyRetriever; r = PolicyRetriever(); print(r.retrieve('energy'))"
```

---

## 📈 Future Enhancements

- [ ] Machine learning-based anomaly detection (Isolation Forest)
- [ ] Multi-campus support
- [ ] Real-time data integration (SCADA, IoT)
- [ ] Mobile application
- [ ] Advanced NLP for policy search
- [ ] Automated alerting system
- [ ] Prediction models for consumption forecasting
- [ ] Carbon footprint calculation

---

## 👥 Code Style & Standards

- **PEP 8**: Python style guide
- **Docstrings**: Google style for all functions
- **Type hints**: Used for clarity
- **Comments**: Explain "why", not "what"
- **Error handling**: Try-except with logging

---

**Last Updated**: January 2024
**Version**: 1.0
**Status**: Production Ready for Internship
