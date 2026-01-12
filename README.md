# EcoSense AI – Invisible Resource Loss Detection System for Sustainable Campuses

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-green.svg)
![IBM Watsonx](https://img.shields.io/badge/IBM%20Watsonx-AI-0F62FE.svg)

## 📋 Project Overview

**EcoSense AI** is an intelligent decision-support system designed to identify invisible resource wastage on educational campuses through data analysis and AI-powered insights. The system detects inefficiencies in electricity and water consumption and provides evidence-based, policy-grounded recommendations to campus administrators.

### 🎯 Problem Statement

Educational campuses consume large amounts of resources daily, but significant portions go unnoticed:
- **Lights, fans, and air conditioners** left running unnecessarily
- **Water wastage** in washrooms and facilities
- **Inefficient lab and facility usage**
- **Behavioral patterns** that go untracked

**How might we use AI to identify and explain invisible resource wastage patterns on campuses so that institutions can become more sustainable without additional infrastructure costs?**

### 🌍 SDG Alignment

- **Primary**: SDG 12 – Responsible Consumption and Production
- **Secondary**: SDG 11 – Sustainable Cities and Communities
- **Secondary**: SDG 13 – Climate Action

## 🚀 Key Features

✅ **Real-time Data Analysis**
- Electricity consumption pattern detection
- Water usage monitoring and leak detection
- Anomaly and threshold-based alerts

✅ **AI-Powered Insights**
- IBM Granite LLM integration for explainable recommendations
- Natural language generation of sustainability insights
- Transparent reasoning for all recommendations

✅ **Retrieval-Augmented Generation (RAG)**
- Policy-grounded recommendations using sustainability best practices
- Knowledge base of sustainability guidelines
- Aligned with industry standards and certifications

✅ **Interactive Dashboard**
- Facility-wise consumption breakdown
- Time-series visualization
- Anomaly tracking and reporting
- Executive summary generation

✅ **Responsible AI**
- Privacy-first design (aggregated data only)
- Transparent decision-making process
- Recommendations support, not enforce, decisions
- No personal/individual tracking

## 📁 Project Structure

```
EcoSense-AI/
│
├── app.py                              # Streamlit UI Dashboard
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── .env.example                        # Environment template
│
├── data/
│   ├── electricity.csv                 # Electricity consumption data
│   └── water.csv                       # Water consumption data
│
├── analysis/
│   ├── electricity_analysis.py         # Electricity analysis module
│   └── water_analysis.py               # Water analysis module
│
├── ibm_ai/
│   ├── granite_llm.py                  # IBM Granite LLM integration
│   └── prompt_templates.py             # Prompt engineering templates
│
├── rag/
│   ├── policy_docs.txt                 # Sustainability knowledge base
│   └── retriever.py                    # RAG implementation with FAISS
│
├── config.py                           # Configuration management
├── utils.py                            # Utility functions
├── logger_config.py                    # Logging configuration
├── data_generator.py                   # Sample data generation
│
└── outputs/
    ├── insights_log.txt                # AI-generated insights log
    └── system.log                      # System logs
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip or conda package manager
- IBM Watsonx API credentials (optional for demo mode)

### Step 1: Clone and Navigate
```bash
cd EcoSense-AI
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# IBM_WATSONX_API_KEY=your_key_here
# IBM_PROJECT_ID=your_project_id_here
```

### Step 5: Generate Sample Data (Optional)
```bash
python data_generator.py
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📊 How It Works

### 1. Data Input
- Upload electricity and water consumption CSV files
- System loads and parses temporal data
- Facility-level aggregation for privacy

### 2. Pattern Detection
- **Time-based analysis**: Identifies consumption trends
- **Anomaly detection**: Percentile-based threshold flagging
- **Night-time usage**: Detects unnecessary off-hours consumption
- **Facility comparison**: Benchmarks against peer facilities

### 3. RAG Knowledge Retrieval
- Searches sustainability policy knowledge base
- Retrieves relevant best practices using semantic search
- Grounds AI recommendations in established frameworks

### 4. AI Insight Generation
- IBM Granite LLM analyzes patterns with context
- Generates explainable insights with reasoning
- Suggests practical, low-cost interventions
- Prioritizes recommendations by impact and feasibility

### 5. User Interaction
- Dashboard visualizes findings
- Reports provide actionable recommendations
- Insights are logged for tracking
- Policy context maintains transparency

## 📈 Analysis Capabilities

### Electricity Analysis
- Total consumption tracking
- Per-facility breakdown
- Night-time idle detection (10 PM - 5 AM)
- Anomaly flagging above 75th percentile
- Trend analysis (increasing/decreasing/stable)

### Water Analysis
- Consumption aggregation
- Peak usage period identification
- Leak detection through anomaly patterns
- Facility-specific risk assessment
- Conservation opportunity identification

### Combined Insights
- Cross-resource efficiency analysis
- Behavioral pattern correlation
- Integrated sustainability recommendations
- Cost-benefit analysis
- Implementation roadmap

## 🤖 IBM Granite LLM Integration

The system uses **IBM Granite Large Language Models** via Watsonx AI to:

1. **Analyze consumption patterns** in natural language
2. **Generate explainable insights** with reasoning
3. **Ground recommendations** in sustainability policies
4. **Adapt tone** for different stakeholder groups
5. **Support decision-making** rather than enforce compliance

### Example Prompts

```python
# Electricity analysis prompt
"Analyze electricity consumption data and provide insights on:
1. Peak usage patterns
2. Night-time idle consumption
3. Facility-specific anomalies
4. Practical recommendations"

# Policy-grounded prompt
"Using these sustainability guidelines, recommend actions for 
the identified inefficiencies, considering ROI and implementation ease"
```

## 🔍 RAG (Retrieval-Augmented Generation)

### Knowledge Base
The system includes sustainability best practices covering:
- Energy efficiency standards (LED, smart controls, automation)
- Water conservation guidelines (low-flow fixtures, recycling)
- Carbon footprint reduction (renewables, EVs, supply chain)
- Compliance frameworks (ISO 50001, LEED, Carbon Neutral)
- Implementation best practices

### Retrieval Process
- **Keyword-based search**: Fast fallback method
- **Semantic search**: FAISS + Sentence Transformers (if available)
- **Context ranking**: Returns top 3-5 most relevant policies
- **Augmented prompts**: Combines user query with policy context

## 📱 Dashboard Features

### 📊 Main Dashboard
- Overall consumption metrics
- Facility distribution pie charts
- Time-series consumption trends
- Quick anomaly summary

### ⚡ Electricity Analysis
- Facility-wise consumption breakdown
- Night-time usage analysis
- Anomaly table with severity scores
- Consumption distribution chart

### 💧 Water Analysis
- Leak risk assessment
- Facility inspection priorities
- Consumption statistics
- Anomaly details

### 🤖 AI Insights
- One-click insight generation
- Policy context retrieval
- Multi-analysis reporting
- Insight logging

### 📋 Report Generator
- Executive summaries
- Detailed technical reports
- Markdown export
- Timestamped archiving

## 🔐 Responsible AI Principles

### 1. Fairness
- **Aggregated data only**: No individual/personal data processing
- **Facility-level analysis**: Treats all facilities equally
- **Unbiased thresholds**: Statistical percentile-based

### 2. Transparency
- **Explainable insights**: AI explains reasoning for recommendations
- **Confidence levels**: Clear indication of analysis certainty
- **Data visibility**: Users see underlying analysis and data

### 3. Privacy
- **No personal tracking**: Campus-level aggregation only
- **Optional data**: Users control what data is uploaded
- **Secure logging**: Insights stored locally in audit trail

### 4. Ethics
- **Recommendations only**: System supports, doesn't mandate
- **Human agency**: Final decisions with administrators
- **Behavior support**: Encourages without punishment
- **Transparency note**: Clearly states system limitations

## 📊 Sample Output

### Analysis Results
```json
{
  "electricity": {
    "total_consumption_kwh": 45230.5,
    "average_consumption_kwh": 150.8,
    "peak_consumption_kwh": 580.3,
    "night_consumption_kwh": 4200.5,
    "anomalies_detected": 18,
    "consumption_trend": "increasing"
  },
  "water": {
    "total_consumption_gallons": 250000,
    "anomalies_detected": 12,
    "potential_leaks": "HIGH"
  }
}
```

### AI-Generated Insight
```
SUSTAINABILITY ANALYSIS REPORT

KEY FINDINGS:
1. Night-time consumption is 15-20% of daily total, indicating 
   unnecessary baseline load and always-on equipment.
2. Building A shows consistent 2-5 AM spikes suggesting HVAC inefficiency.
3. Water anomalies may indicate minor leaks in facilities B and D.

RECOMMENDATIONS:
1. Conduct equipment audit for always-on devices (Week 1)
2. Implement timer-based controls (Week 2-3)
3. Schedule leak inspections (Week 2)
4. Staff training on shutdown protocols (Week 4)

EXPECTED IMPACT:
- 10-15% reduction in night-time electricity use
- 5-10% water savings through leak prevention
- Annual cost savings: $5,000-$8,000
```

## 🧪 Testing

### Run Data Generator
```bash
python data_generator.py
```

### Run Specific Analysis
```bash
python -c "
from analysis.electricity_analysis import ElectricityAnalyzer
analyzer = ElectricityAnalyzer('data/electricity.csv')
results = analyzer.analyze()
print(results)
"
```

## 📚 API Usage

### Using ElectricityAnalyzer
```python
from analysis.electricity_analysis import ElectricityAnalyzer

analyzer = ElectricityAnalyzer('path/to/electricity.csv')
results = analyzer.analyze()

print(f"Total: {results['total_consumption_kwh']} kWh")
print(f"Anomalies: {results['anomalies_detected']}")
print(f"Anomaly details: {results['anomaly_details']}")
```

### Using Granite LLM
```python
from ibm_ai.granite_llm import GraniteLLM

llm = GraniteLLM(api_key="your_key", project_id="your_project_id")
insight = llm.generate("Analyze electricity consumption...")
print(insight)
```

### Using RAG
```python
from rag.retriever import PolicyRetriever

retriever = PolicyRetriever('rag/policy_docs.txt')
policies = retriever.retrieve("energy efficiency", top_k=3)
augmented_prompt = retriever.augment_prompt(user_prompt)
```

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Streamlit Cloud
```bash
# Requirements:
# - GitHub account with code repository
# - .streamlit/secrets.toml with environment variables

streamlit cloud deploy
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- [ ] Additional data sources (gas, renewable energy)
- [ ] Machine learning-based anomaly detection
- [ ] Mobile app version
- [ ] Integration with SCADA systems
- [ ] Multi-campus support
- [ ] Advanced visualization

*Built with ❤️ for a sustainable future*
