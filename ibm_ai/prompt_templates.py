# Prompt engineering templates for IBM Granite LLM (Responsible AI)

# System prompts
SYSTEM_PROMPT = """You are EcoSense AI, a sustainability decision-support system for educational institutions.
Your role is to:
1. Analyze resource consumption data and identify inefficiencies
2. Provide evidence-based explanations for consumption patterns
3. Suggest low-cost, practical interventions
4. Maintain transparency about your reasoning

Important: You provide recommendations, not enforcement. Decisions remain with administrators.
Focus on factual analysis, responsible suggestions, and ethical considerations."""

# Electricity analysis prompts
ELECTRICITY_ANALYSIS_PROMPT = """Analyze the following electricity consumption data and provide insights:

FACILITY DATA:
{facility_data}

CONSUMPTION STATISTICS:
- Total Consumption: {total_kwh} kWh
- Average Consumption: {avg_kwh} kWh
- Peak Consumption: {peak_kwh} kWh
- Night-time Consumption: {night_kwh} kWh ({night_percentage}% of total)
- Anomalies Detected: {anomalies} instances above threshold
- Trend: {trend}

ANOMALY DETAILS:
{anomaly_details}

Based on this data, provide:
1. Key findings about consumption patterns
2. Explanation of night-time usage and idle consumption
3. Facility-specific insights
4. Potential causes of anomalies
5. Sustainability recommendations (low-cost, practical)

Keep your response clear, factual, and actionable for campus decision-makers."""

# Water analysis prompts
WATER_ANALYSIS_PROMPT = """Analyze the following water consumption data and identify potential waste:

FACILITY DATA:
{facility_data}

CONSUMPTION STATISTICS:
- Total Consumption: {total_gallons} gallons
- Average Consumption: {avg_gallons} gallons per hour
- Peak Consumption: {peak_gallons} gallons
- Night-time Consumption: {night_gallons} gallons ({night_percentage}% of total)
- Anomalies Detected: {anomalies} instances
- Trend: {trend}

LEAK INDICATORS:
{leak_data}

Based on this analysis, provide:
1. Assessment of consumption patterns
2. Identification of potential leaks or continuous usage
3. Explanation of anomalies
4. Water conservation recommendations
5. Priority areas for immediate inspection
6. Long-term sustainability initiatives

Focus on practical, implementable solutions."""

# Combined insights prompt
COMBINED_INSIGHTS_PROMPT = """Generate a comprehensive sustainability insight report combining electricity and water analysis:

ELECTRICITY SUMMARY:
{electricity_summary}

WATER SUMMARY:
{water_summary}

Provide:
1. Overall sustainability assessment
2. Cross-resource inefficiency patterns
3. Behavioral insights (e.g., late-night usage culture)
4. Immediate action items (within 1 week)
5. Medium-term improvements (1-3 months)
6. Long-term strategy (6-12 months)
7. Expected impact on costs and emissions
8. Staff engagement recommendations

Frame recommendations as decision-support for administrators, not directives."""

# Policy grounding prompt (RAG-enhanced)
POLICY_GROUNDED_PROMPT = """Using the following sustainability best practices and policies, provide contextualized recommendations:

SUSTAINABILITY POLICIES AND GUIDELINES:
{retrieved_policies}

CURRENT SITUATION:
{situation_analysis}

ANALYSIS:
Align your recommendations with the provided policies and best practices. For each recommendation:
1. State the relevant policy or guideline
2. Explain how it applies to this situation
3. Suggest implementation steps
4. Identify potential challenges
5. Propose success metrics

This ensures recommendations are grounded in established sustainability frameworks."""

# Explanation prompt (Transparency)
EXPLANATION_PROMPT = """Explain your reasoning for the following insights in a transparent, understandable way:

INSIGHT:
{insight}

DATA SUPPORTING THIS:
{supporting_data}

Please explain:
1. What data pattern led to this conclusion?
2. What assumptions did you make?
3. What alternative explanations exist?
4. What confidence level do you have (high/medium/low)?
5. What additional data would strengthen this conclusion?
6. Any limitations or caveats?

This transparency helps stakeholders understand and trust the AI system."""

# Template for interactive query
INTERACTIVE_QUERY_TEMPLATE = """User Query: {user_query}

Available Data Context:
{data_context}

Retrieved Relevant Policies:
{policies}

Please provide:
1. Direct answer to the query
2. Supporting analysis from the data
3. Relevant policy context
4. Actionable recommendations
5. Confidence level and limitations

Keep response concise but comprehensive."""

def get_system_prompt():
    """Return system prompt"""
    return SYSTEM_PROMPT

def format_electricity_prompt(facility_data, total_kwh, avg_kwh, peak_kwh, night_kwh, night_percentage, anomalies, anomaly_details, trend):
    """Format electricity analysis prompt"""
    return ELECTRICITY_ANALYSIS_PROMPT.format(
        facility_data=facility_data,
        total_kwh=total_kwh,
        avg_kwh=avg_kwh,
        peak_kwh=peak_kwh,
        night_kwh=night_kwh,
        night_percentage=night_percentage,
        anomalies=anomalies,
        anomaly_details=anomaly_details,
        trend=trend
    )

def format_water_prompt(facility_data, total_gallons, avg_gallons, peak_gallons, night_gallons, night_percentage, anomalies, leak_data, trend):
    """Format water analysis prompt"""
    return WATER_ANALYSIS_PROMPT.format(
        facility_data=facility_data,
        total_gallons=total_gallons,
        avg_gallons=avg_gallons,
        peak_gallons=peak_gallons,
        night_gallons=night_gallons,
        night_percentage=night_percentage,
        anomalies=anomalies,
        leak_data=leak_data,
        trend=trend
    )
