# IBM Granite LLM integration via Watsonx
import os
import requests
import json
from config import IBM_API_KEY, IBM_PROJECT_ID, WATSONX_URL, MODEL_ID, MAX_TOKENS, TEMPERATURE
from logger_config import logger

class GraniteLLM:
    """
    Interface for IBM Granite LLM via Watsonx AI
    Implements responsible AI practices with transparency
    """
    
    def __init__(self, api_key=None, project_id=None):
        """
        Initialize Granite LLM client
        
        Args:
            api_key: IBM Watsonx API key
            project_id: IBM project ID
        """
        self.api_key = api_key or IBM_API_KEY
        self.project_id = project_id or IBM_PROJECT_ID
        self.base_url = WATSONX_URL
        self.model_id = MODEL_ID
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE

        if not self.api_key or not self.project_id:
            raise RuntimeError(
                "IBM Watsonx credentials are required. Set IBM_WATSONX_API_KEY and IBM_PROJECT_ID."
            )
    
    def generate(self, prompt, system_prompt=None, max_tokens=None):
        """
        Generate text using Granite LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text or mock response
        """
        max_tokens = max_tokens or self.max_tokens
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model_id": self.model_id,
                "input": prompt,
                "parameters": {
                    "max_tokens": max_tokens,
                    "temperature": self.temperature,
                    "top_p": 1.0,
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/v1/text/generation",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'results' in result and len(result['results']) > 0:
                    return result['results'][0].get('generated_text', '')
                return ""
            else:
                error_detail = response.text
                logger.error(f"Watsonx API error: {response.status_code} - {error_detail}")
                raise RuntimeError(f"Watsonx API error: {response.status_code} - {error_detail}")
                
        except Exception as e:
            logger.error(f"Error calling Granite LLM: {e}")
            raise
    
    def analyze_sustainability(self, data_summary, system_prompt):
        """
        Analyze sustainability data and generate insights
        
        Args:
            data_summary: Summary of resource data
            system_prompt: System instructions
            
        Returns:
            Sustainability insight
        """
        logger.info("Generating sustainability insights with Granite LLM...")
        return self.generate(data_summary, system_prompt=system_prompt)
    
    def explain_anomaly(self, anomaly_description, context_data):
        """
        Explain an anomaly in consumption
        
        Args:
            anomaly_description: Description of anomaly
            context_data: Contextual data about anomaly
            
        Returns:
            Explanation
        """
        prompt = f"""Given the following anomaly:

{anomaly_description}

Context:
{context_data}

Please explain:
1. What likely caused this anomaly?
2. What is the confidence level (high/medium/low)?
3. What interventions would address this?
4. Are there any data limitations in this analysis?"""
        
        return self.generate(prompt)
    
    def get_recommendations(self, analysis_summary, policies):
        """
        Get recommendations grounded in policies
        
        Args:
            analysis_summary: Summary of analysis
            policies: Relevant sustainability policies
            
        Returns:
            Policy-grounded recommendations
        """
        prompt = f"""Based on this analysis:
{analysis_summary}

And considering these sustainability best practices:
{policies}

Provide concrete, implementable recommendations that:
1. Address identified inefficiencies
2. Align with best practices
3. Have clear ROI and timelines
4. Respect privacy and autonomy
5. Support rather than mandate behavior change"""
        
        return self.generate(prompt)
