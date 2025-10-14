# utils.py
from openai import OpenAI
import streamlit as st
import re
import json

client = OpenAI()

def get_openai_api_key():
    """Get OpenAI API key from Streamlit secrets or environment"""
    return st.secrets.get("OPENAI_API_KEY", None)

def moderate_input(prompt):
    """
    Security guard to prevent prompt injection and inappropriate content.
    Uses OpenAI's Moderation API and custom validation.
    """
    if not prompt or len(prompt.strip()) == 0:
        return True
    
    # Check length (prevent extremely long inputs)
    if len(prompt) > 2000:
        return True
    
    # Check for prompt injection attempts
    injection_patterns = [
        r"ignore\s+(previous|above|all)\s+instructions?",
        r"disregard\s+(previous|above|all)",
        r"you\s+are\s+now",
        r"new\s+instructions?:",
        r"system\s*:\s*",
        r"</?\s*system\s*>",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, prompt.lower()):
            return True
    
    # Use OpenAI Moderation API for content safety
    try:
        moderation = client.moderations.create(input=prompt)
        if moderation.results[0].flagged:
            return True
    except Exception as e:
        print(f"Moderation API error: {e}")
        # Fail open - allow if moderation fails
        pass
    
    return False

def validate_system_prompt(system_prompt):
    """Validate that system prompt hasn't been tampered with"""
    dangerous_keywords = ["jailbreak", "DAN", "developer mode", "unrestricted"]
    for keyword in dangerous_keywords:
        if keyword.lower() in system_prompt.lower():
            return False
    return True

def call_openai(system_prompt, messages, model="gpt-4o-mini", temperature=0.7, 
                max_tokens=800, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0,
                response_format=None):
    """
    Call OpenAI API with conversation history and configurable parameters.
    
    Args:
        system_prompt: System message to guide the AI
        messages: List of conversation messages
        model: OpenAI model to use
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum tokens in response
        top_p: Nucleus sampling parameter
        frequency_penalty: Penalize frequent tokens (-2.0 to 2.0)
        presence_penalty: Penalize tokens that have appeared (-2.0 to 2.0)
        response_format: Optional response format (e.g., {"type": "json_object"})
    """
    # Validate system prompt
    if not validate_system_prompt(system_prompt):
        raise ValueError("Invalid system prompt detected")
    
    # Build messages array
    api_messages = [{"role": "system", "content": system_prompt}]
    api_messages.extend(messages)
    
    # Call OpenAI API
    try:
        params = {
            "model": model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        
        if response_format:
            params["response_format"] = response_format
        
        response = client.chat.completions.create(**params)
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

def calculate_cost(model, input_tokens, output_tokens):
    """
    Calculate the cost of an API call based on token usage.
    Prices as of 2024 (approximate).
    """
    pricing = {
        "gpt-4o": {"input": 0.0025, "output": 0.01},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4": {"input": 0.03, "output": 0.06},
    }
    
    # Default pricing if model not found
    if model not in pricing:
        pricing[model] = {"input": 0.001, "output": 0.002}
    
    input_cost = (input_tokens / 1000) * pricing[model]["input"]
    output_cost = (output_tokens / 1000) * pricing[model]["output"]
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

def extract_json_from_response(response_text):
    """Extract JSON from AI response that might contain markdown or extra text"""
    try:
        # First, try direct JSON parse
        return json.loads(response_text)
    except:
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # Try to find JSON object in the text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
    
    return None

