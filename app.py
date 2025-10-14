# app.py
"""
AI Interview Preparation Tool - Enhanced Version
Features:
- Full chatbot functionality with conversation context
- Multiple prompt engineering techniques
- Adjustable OpenAI parameters
- Security guards against misuse
- Structured JSON output for evaluation
- Session tracking and cost calculation
"""

import streamlit as st
import json
from datetime import datetime
from prompts import (
    get_zero_shot_prompt,
    get_few_shot_prompt,
    get_chain_of_thought_prompt,
    get_persona_prompt,
    get_role_specific_prompt,
    get_structured_json_prompt,
    get_mixed_techniques_prompt,
)
from utils import (
    call_openai,
    moderate_input,
    extract_json_from_response,
)

# Page configuration
st.set_page_config(
    page_title="AI Interview Preparation Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .score-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: bold;
        margin: 0.25rem;
    }
    .score-high { background-color: #d4edda; color: #155724; }
    .score-medium { background-color: #fff3cd; color: #856404; }
    .score-low { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "session_cost" not in st.session_state:
        st.session_state.session_cost = 0.0
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "scores" not in st.session_state:
        st.session_state.scores = []
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    if "json_mode" not in st.session_state:
        st.session_state.json_mode = False
    if "response_scores" not in st.session_state:
        st.session_state.response_scores = []
    if "average_score" not in st.session_state:
        st.session_state.average_score = 0.0

init_session_state()

# Header
st.markdown('<h1 class="main-header">🧠 AI Interview Preparation Tool</h1>', unsafe_allow_html=True)
st.markdown("**Practice interviews with AI • Get instant feedback • Improve your skills**")

# Sidebar Configuration
st.sidebar.title("⚙️ Interview Configuration")

# Basic Settings
st.sidebar.header("📋 Interview Setup")
role = st.sidebar.selectbox(
    "Choose Interview Role",
    [
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Scientist",
        "Data Analyst",
        "Product Manager",
        "UX Designer",
        "DevOps Engineer",
        "ML Engineer"
    ],
    help="Select the role you're preparing for"
)

level = st.sidebar.radio(
    "Experience Level",
    ["Junior", "Mid", "Senior"],
    help="Junior: 0-2 years | Mid: 3-5 years | Senior: 5+ years"
)

domain = st.sidebar.selectbox(
    "Industry Domain",
    ["General", "Tech/Startup", "Finance", "Healthcare", "E-commerce", "Enterprise", "Consulting"],
    help="Industry focus for your interview preparation"
)

# Interviewer Tone Selection
tone = st.sidebar.selectbox(
    "Interviewer Tone",
    ["Friendly", "Professional", "Strict"],
    index=1,
    help="""
    Friendly: Warm, encouraging, supportive
    Professional: Balanced, neutral, business-like
    Strict: Direct, demanding, high standards
    """
)

st.sidebar.divider()

# Prompt Engineering Techniques
st.sidebar.header("🎯 Prompt Technique")
prompt_style = st.sidebar.selectbox(
    "Select Prompting Strategy",
    [
        "Zero-shot",
        "Few-shot",
        "Chain-of-Thought",
        "Persona Interview",
        "Role-specific",
        "Structured JSON",
        "Mixed Techniques"
    ],
    help="""
    Zero-shot: Direct instructions
    Few-shot: Learn from examples
    Chain-of-Thought: Step-by-step reasoning
    Persona: Behavioral interview focus
    Role-specific: Technical deep dive
    Structured JSON: Programmatic evaluation
    Mixed: Combines multiple techniques
    """
)

st.sidebar.divider()

# Model Selection
st.sidebar.header("🤖 AI Model Settings")
model = st.sidebar.selectbox(
    "OpenAI Model",
    [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4-turbo",
        "gpt-4"
    ],
    index=0,
    help="Choose the AI model. Mini is faster and cheaper, GPT-4 is more capable."
)

# Advanced Settings Expander
with st.sidebar.expander("🔧 Advanced Parameters", expanded=False):
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower = more focused, Higher = more creative"
    )
    
    max_tokens = st.slider(
        "Max Response Tokens",
        min_value=200,
        max_value=2000,
        value=800,
        step=100,
        help="Maximum length of AI responses"
    )
    
    top_p = st.slider(
        "Top P (Nucleus Sampling)",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Alternative to temperature for controlling randomness"
    )
    
    frequency_penalty = st.slider(
        "Frequency Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Penalize repeated tokens. Positive values reduce repetition."
    )
    
    presence_penalty = st.slider(
        "Presence Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Penalize tokens that have appeared. Positive values encourage new topics."
    )

st.sidebar.divider()

# Session Stats
st.sidebar.header("📊 Session Statistics")
duration = datetime.now() - st.session_state.session_start_time
st.sidebar.metric("Questions Answered", st.session_state.question_count)

# Display average score with color
if st.session_state.average_score > 0:
    score_color = "🟢" if st.session_state.average_score >= 7 else "🟡" if st.session_state.average_score >= 5 else "🔴"
    st.sidebar.metric("Average Score", f"{score_color} {st.session_state.average_score:.1f}/10")
else:
    st.sidebar.metric("Average Score", "Not yet scored")

st.sidebar.metric("Session Duration", f"{duration.seconds // 60}m {duration.seconds % 60}s")
st.sidebar.metric("Total Tokens Used", st.session_state.total_tokens)
st.sidebar.metric("Estimated Cost", f"${st.session_state.session_cost:.4f}")

# Score history chart
if len(st.session_state.response_scores) > 0:
    st.sidebar.markdown("**📈 Score Progress**")
    scores_display = [score["overall"] for score in st.session_state.response_scores]
    st.sidebar.line_chart(scores_display)

# Session Controls
st.sidebar.divider()
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔄 Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col2:
    if st.button("💾 Export Chat", use_container_width=True):
        export_data = {
            "role": role,
            "level": level,
            "domain": domain,
            "tone": tone,
            "prompt_style": prompt_style,
            "messages": st.session_state.messages,
            "scores": st.session_state.scores,
            "response_scores": st.session_state.response_scores,
            "average_score": st.session_state.average_score,
            "session_duration": str(duration),
            "total_cost": st.session_state.session_cost
        }
        st.sidebar.download_button(
            "📥 Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"interview_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

# Main content area
tone_emoji = {"Friendly": "😊", "Professional": "💼", "Strict": "📋"}
st.subheader(f"💼 Mock Interview: {level} {role} ({domain})")
st.caption(f"**Technique:** {prompt_style} | **Model:** {model} | **Tone:** {tone_emoji[tone]} {tone}")

# Get tone instructions
def get_tone_instructions(tone):
    """Return tone-specific instructions for the AI"""
    if tone == "Friendly":
        return """
TONE: Friendly and Supportive
- Use warm, encouraging language
- Celebrate good answers enthusiastically
- Provide constructive criticism gently
- Use phrases like "Great!", "Excellent point!", "I appreciate that..."
- Be patient and understanding
- Offer helpful hints when candidate struggles
- Make the candidate feel comfortable and valued
"""
    elif tone == "Strict":
        return """
TONE: Strict and Demanding
- Be direct and to-the-point
- Set high standards and expectations
- Point out weaknesses clearly
- Don't sugarcoat feedback
- Use phrases like "That's insufficient", "You need to...", "Expected more..."
- Challenge the candidate to think deeper
- Be professional but demanding
- Only praise truly excellent answers
"""
    else:  # Professional
        return """
TONE: Professional and Balanced
- Maintain a neutral, business-like demeanor
- Be objective and fair in assessments
- Provide balanced feedback (positives and areas for improvement)
- Use clear, professional language
- Be respectful but not overly warm
- Focus on facts and competencies
- Standard phrases: "Your answer demonstrates...", "Consider improving..."
"""

# Update system prompt based on selection
def update_system_prompt():
    """Update the system prompt based on current configuration"""
    tone_instruction = get_tone_instructions(tone)
    
    if prompt_style == "Zero-shot":
        base_prompt = get_zero_shot_prompt(role, level, domain)
    elif prompt_style == "Few-shot":
        base_prompt = get_few_shot_prompt(role, level, domain)
    elif prompt_style == "Chain-of-Thought":
        base_prompt = get_chain_of_thought_prompt(role, level, domain)
    elif prompt_style == "Persona Interview":
        base_prompt = get_persona_prompt(role, level, domain)
    elif prompt_style == "Role-specific":
        base_prompt = get_role_specific_prompt(role, level, domain)
    elif prompt_style == "Structured JSON":
        st.session_state.json_mode = True
        base_prompt = get_structured_json_prompt(role, level, domain)
    elif prompt_style == "Mixed Techniques":
        base_prompt = get_mixed_techniques_prompt(role, level, domain)
    else:
        base_prompt = get_zero_shot_prompt(role, level, domain)
    
    # Add scoring instruction to all prompts
    scoring_instruction = """

SCORING REQUIREMENT:
After each candidate answer, you MUST provide a numerical score from 1-10 for their response.
Include this scoring in your feedback using this format:

**Score: X/10**

Base your score on:
- Technical accuracy and depth (if applicable)
- Clarity and structure of communication
- Completeness of the answer
- Relevance to the question
- Examples and evidence provided

Scoring Guide:
- 1-3: Poor/Inadequate answer, major gaps
- 4-5: Below average, missing key points
- 6-7: Good, meets basic expectations
- 8-9: Excellent, thorough and well-articulated
- 10: Outstanding, exceeds all expectations
"""
    
    return base_prompt + "\n" + tone_instruction + "\n" + scoring_instruction

st.session_state.current_prompt = update_system_prompt()

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    role_display = "assistant" if message["role"] == "assistant" else "user"
    with st.chat_message(role_display):
        st.markdown(message["content"])
        
        # Display scores for this response
        if "response_score" in message and message["response_score"] is not None:
            score_val = message["response_score"]
            score_class = "score-high" if score_val >= 7 else "score-medium" if score_val >= 5 else "score-low"
            st.markdown(
                f'<div class="score-badge {score_class}">Response Score: {score_val}/10</div>',
                unsafe_allow_html=True
            )
        
        # Display structured scores if available in JSON mode
        if "scores" in message and message["scores"]:
            scores = message["scores"]
            cols = st.columns(4)
            metrics = [
                ("Technical", scores.get("technical_accuracy", {}).get("score", 0)),
                ("Communication", scores.get("communication", {}).get("score", 0)),
                ("Problem Solving", scores.get("problem_solving", {}).get("score", 0)),
                ("Completeness", scores.get("completeness", {}).get("score", 0))
            ]
            
            for col, (label, score) in zip(cols, metrics):
                score_class = "score-high" if score >= 7 else "score-medium" if score >= 5 else "score-low"
                col.markdown(
                    f'<div class="score-badge {score_class}">{label}: {score}/10</div>',
                    unsafe_allow_html=True
                )

# Start interview if not yet started
if not st.session_state.interview_started and len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        tone_greetings = {
            "Friendly": "Welcome! I'm so excited to help you prepare! 😊",
            "Professional": "Welcome to your interview preparation session.",
            "Strict": "Welcome. Let's begin the interview. I expect focused, detailed answers."
        }
        
        welcome_msg = f"""{tone_greetings[tone]}

**Session Configuration:**
- Role: {level} {role}
- Domain: {domain}
- Technique: {prompt_style}
- Interviewer Tone: {tone_emoji[tone]} {tone}

{"💡 Remember: I'll be scoring each of your responses from 1-10 based on quality, depth, and relevance." if tone != "Strict" else "⚠️ Note: Each response will be scored from 1-10. I maintain high standards."}

Let's begin with our first question:

**Tell me about yourself and why you're interested in this {role} position.**"""
        st.markdown(welcome_msg)
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg,
            "response_score": None
        })
        st.session_state.interview_started = True

# Chat input
if user_input := st.chat_input("Type your answer here...", key="chat_input"):
    # Security check
    if moderate_input(user_input):
        st.error("⚠️ **Security Alert:** Inappropriate input detected. Please provide a professional interview response.")
        st.stop()
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing your response..."):
            try:
                # Prepare messages for API call
                api_messages = []
                for msg in st.session_state.messages:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Determine if JSON mode should be used
                response_format = {"type": "json_object"} if st.session_state.json_mode else None
                
                # Call OpenAI API
                ai_response = call_openai(
                    system_prompt=st.session_state.current_prompt,
                    messages=api_messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    response_format=response_format
                )
                
                # Extract score from response
                import re
                score_match = re.search(r'\*\*Score:\s*(\d+(?:\.\d+)?)\s*/\s*10\*\*', ai_response)
                response_score = None
                if score_match:
                    try:
                        response_score = float(score_match.group(1))
                        response_score = min(10.0, max(1.0, response_score))  # Clamp between 1-10
                    except:
                        pass
                
                # Parse JSON response if in structured mode
                scores_data = None
                display_response = ai_response
                
                if st.session_state.json_mode:
                    json_data = extract_json_from_response(ai_response)
                    if json_data:
                        scores_data = json_data.get("evaluation", {})
                        
                        # Format the display response
                        display_response = f"""
**Evaluation:**

📊 **Overall Score:** {json_data.get('overall_score', 'N/A')}/10

**Detailed Feedback:**
"""
                        for category, details in scores_data.items():
                            if isinstance(details, dict):
                                score = details.get('score', 'N/A')
                                feedback = details.get('feedback', '')
                                display_response += f"\n**{category.replace('_', ' ').title()}:** {score}/10\n{feedback}\n"
                        
                        if json_data.get('strengths'):
                            display_response += f"\n**✅ Strengths:**\n"
                            for strength in json_data['strengths']:
                                display_response += f"- {strength}\n"
                        
                        if json_data.get('improvements'):
                            display_response += f"\n**💡 Areas for Improvement:**\n"
                            for improvement in json_data['improvements']:
                                display_response += f"- {improvement}\n"
                        
                        if json_data.get('recommendation'):
                            display_response += f"\n**Recommendation:**\n{json_data['recommendation']}\n"
                        
                        if json_data.get('question'):
                            display_response += f"\n**Next Question:**\n{json_data['question']}"
                        
                        # Store scores
                        st.session_state.scores.append({
                            "question_num": st.session_state.question_count + 1,
                            "overall": json_data.get('overall_score', 0),
                            "details": scores_data
                        })
                
                st.markdown(display_response)
                
                # Store the score for this response
                if response_score is not None:
                    st.session_state.response_scores.append({
                        "question_num": st.session_state.question_count + 1,
                        "overall": response_score
                    })
                    
                    # Calculate average score
                    all_scores = [s["overall"] for s in st.session_state.response_scores]
                    st.session_state.average_score = sum(all_scores) / len(all_scores)
                    
                    # Display score badge
                    score_class = "score-high" if response_score >= 7 else "score-medium" if response_score >= 5 else "score-low"
                    st.markdown(
                        f'<div class="score-badge {score_class}">Your Score: {response_score}/10</div>',
                        unsafe_allow_html=True
                    )
                
                # Save to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": display_response,
                    "scores": scores_data,
                    "response_score": response_score
                })
                
                st.session_state.question_count += 1
                
                # Update token usage (approximate - would need actual API response for exact count)
                estimated_tokens = len(user_input.split()) * 1.3 + len(ai_response.split()) * 1.3
                st.session_state.total_tokens += int(estimated_tokens)
                
                # Estimate cost (very approximate)
                if model == "gpt-4o-mini":
                    cost_per_1k = 0.00015
                elif model == "gpt-4o":
                    cost_per_1k = 0.0025
                elif model == "gpt-4-turbo":
                    cost_per_1k = 0.01
                else:
                    cost_per_1k = 0.03
                
                st.session_state.session_cost += (estimated_tokens / 1000) * cost_per_1k
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: Check your OpenAI API key in `.streamlit/secrets.toml`")
    
    st.rerun()

# Bottom info
st.divider()
st.caption("🔒 **Security Features:** Prompt injection detection • Content moderation • Input validation")
st.caption(f"💡 **Current Settings:** {model} at temperature {temperature} | Max tokens: {max_tokens}")

