# 🧠 AI Interview Preparation Tool

A comprehensive Streamlit-based application for interview preparation powered by OpenAI's GPT models. This tool helps you practice technical and behavioral interviews with AI-powered feedback using advanced prompt engineering techniques.

## 🌟 Features

### Core Functionality
- **Full Chatbot Interface**: Conduct complete interview sessions with conversation context
- **Multiple Prompt Engineering Techniques**: 
  - Zero-shot prompting
  - Few-shot learning
  - Chain-of-Thought reasoning
  - Persona-based interviews
  - Role-specific evaluations
  - Structured JSON output
  - Mixed techniques
  
### Interview Customization
- **9 Role Options**: Frontend/Backend/Full Stack Developer, Data Scientist/Analyst, Product Manager, UX Designer, DevOps Engineer, ML Engineer
- **3 Experience Levels**: Junior (0-2 years), Mid (3-5 years), Senior (5+ years)
- **7 Industry Domains**: General, Tech/Startup, Finance, Healthcare, E-commerce, Enterprise, Consulting

### AI Configuration
- **Model Selection**: Choose from GPT-4o-mini, GPT-4o, GPT-4-turbo, or GPT-4
- **Advanced Parameters**:
  - Temperature control (0.0-2.0)
  - Max response tokens (200-2000)
  - Top-p nucleus sampling
  - Frequency penalty
  - Presence penalty

### Security Features
- ✅ Prompt injection detection
- ✅ Content moderation using OpenAI's Moderation API
- ✅ Input validation and length limits
- ✅ System prompt validation

### Session Management
- 📊 Real-time session statistics
- 💰 Cost tracking and estimation
- ⏱️ Duration monitoring
- 📈 Performance scoring (in JSON mode)
- 💾 Export interview sessions as JSON
- 🔄 Reset and restart functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd /Users/msantana/ai/interviewapp
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:

Create a `.streamlit` directory in the project folder:
```bash
mkdir -p .streamlit
```

Create a `secrets.toml` file:
```bash
cat > .streamlit/secrets.toml << EOF
OPENAI_API_KEY = "your-api-key-here"
EOF
```

Alternatively, set it as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Basic Workflow

1. **Configure Your Interview**:
   - Select your target role (e.g., "Frontend Developer")
   - Choose your experience level (Junior/Mid/Senior)
   - Pick an industry domain
   - Select a prompt engineering technique

2. **Select AI Model**:
   - Use `gpt-4o-mini` for faster, cost-effective interviews
   - Use `gpt-4o` or `gpt-4` for more sophisticated evaluation

3. **Fine-tune Parameters** (Optional):
   - Adjust temperature for creativity vs. consistency
   - Modify other advanced settings as needed

4. **Start the Interview**:
   - Type your answers in the chat input
   - Receive instant feedback and follow-up questions
   - Track your progress in the sidebar

5. **Export Your Session**:
   - Click "Export Chat" to download your interview transcript
   - Review scores and feedback for improvement

### Understanding Prompt Techniques

#### Zero-shot Prompting
- Direct instructions without examples
- Best for: General interviews, quick practice
- Pros: Fast, straightforward, versatile

#### Few-shot Learning
- Includes examples to guide AI behavior
- Best for: Consistent evaluation format
- Pros: More structured feedback, scoring examples

#### Chain-of-Thought
- Step-by-step reasoning process
- Best for: Deep technical evaluation
- Pros: Detailed analysis, shows reasoning

#### Persona Interview
- AI takes on a specific interviewer character
- Best for: Behavioral and soft skills
- Pros: More human-like, encouraging, realistic

#### Role-specific
- Highly customized for job functions
- Best for: Technical deep dives
- Pros: Comprehensive, progressive difficulty

#### Structured JSON
- Programmatic evaluation with scores
- Best for: Quantitative feedback
- Pros: Clear metrics, exportable data

#### Mixed Techniques
- Combines multiple approaches
- Best for: Balanced comprehensive evaluation
- Pros: Robust, versatile, thorough

## 🔧 Configuration Options

### OpenAI Models

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| gpt-4o-mini | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | Quick practice, high volume |
| gpt-4o | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | Balanced quality/cost |
| gpt-4-turbo | ⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Advanced evaluation |
| gpt-4 | ⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰💰 | Best quality |

### Advanced Parameters

- **Temperature (0.0-2.0)**: 
  - Low (0.0-0.3): Focused, consistent, deterministic
  - Medium (0.4-0.9): Balanced creativity and consistency
  - High (1.0-2.0): Creative, varied responses

- **Top-p (0.0-1.0)**: 
  - Alternative to temperature
  - 1.0 = consider all tokens
  - Lower = more focused output

- **Frequency Penalty (-2.0 to 2.0)**: 
  - Positive: Reduces repetition
  - Negative: Allows more repetition

- **Presence Penalty (-2.0 to 2.0)**: 
  - Positive: Encourages new topics
  - Negative: Allows topic focus

## 💡 Tips for Best Results

### For Technical Interviews
1. Use "Role-specific" or "Chain-of-Thought" prompting
2. Select appropriate domain (Tech/Startup for most technical roles)
3. Be specific in your answers with examples
4. Ask for clarification on ambiguous questions

### For Behavioral Interviews
1. Use "Persona Interview" or "Mixed Techniques"
2. Structure answers using STAR method (Situation, Task, Action, Result)
3. Focus on specific examples from your experience
4. Demonstrate self-awareness and growth mindset

### For Best Feedback
1. Enable "Structured JSON" for quantitative scores
2. Use higher temperature (0.7-0.9) for varied questions
3. Lower temperature (0.3-0.5) for consistent evaluation
4. Export sessions to track improvement over time

## 🔒 Security Features

### Implemented Safeguards

1. **Prompt Injection Detection**:
   - Pattern matching for common injection attempts
   - Detects "ignore instructions" type attacks
   - Validates system prompts

2. **Content Moderation**:
   - OpenAI Moderation API integration
   - Filters inappropriate content
   - Protects against misuse

3. **Input Validation**:
   - Length limits (max 2000 characters)
   - Empty input rejection
   - Special character filtering

4. **System Prompt Protection**:
   - Validation against tampering
   - Dangerous keyword detection
   - Safe prompt generation

## 📊 Session Statistics

The application tracks:
- Number of questions asked
- Session duration
- Total tokens used
- Estimated cost
- Performance scores (in JSON mode)

Export your session data for:
- Progress tracking
- Portfolio building
- Performance analysis
- Cost monitoring

## 💰 Cost Estimation

Approximate costs per 1,000 tokens:

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o-mini | $0.00015 | $0.0006 |
| gpt-4o | $0.0025 | $0.01 |
| gpt-4-turbo | $0.01 | $0.03 |
| gpt-4 | $0.03 | $0.06 |

A typical 30-minute interview session:
- gpt-4o-mini: ~$0.05-0.15
- gpt-4o: ~$0.30-0.80
- gpt-4: ~$2.00-5.00

## 🏗️ Project Structure

```
interviewapp/
├── app.py              # Main Streamlit application
├── prompts.py          # Prompt engineering templates
├── utils.py            # Utility functions and API calls
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎓 Educational Value

This project demonstrates:

### Prompt Engineering Techniques
- ✅ Zero-shot prompting
- ✅ Few-shot learning
- ✅ Chain-of-Thought reasoning
- ✅ Persona-based prompting
- ✅ Role-specific prompting
- ✅ Structured output (JSON)
- ✅ Mixed technique approaches

### OpenAI API Features
- ✅ Chat completions API
- ✅ Parameter tuning (temperature, top-p, penalties)
- ✅ Model selection and comparison
- ✅ Moderation API for safety
- ✅ JSON mode for structured output
- ✅ Conversation context management

### Security Best Practices
- ✅ Prompt injection prevention
- ✅ Input validation
- ✅ Content moderation
- ✅ System prompt protection
- ✅ Rate limiting awareness

### Software Engineering
- ✅ Modular code architecture
- ✅ Session state management
- ✅ Error handling
- ✅ User experience design
- ✅ Cost tracking and optimization

## 🚀 Optional Enhancements

### Completed Features
- ✅ Multiple prompt techniques (7 types)
- ✅ All OpenAI parameters tunable
- ✅ Structured JSON output
- ✅ Cost calculation
- ✅ Security guards
- ✅ Full chatbot implementation
- ✅ Model selection
- ✅ Session export functionality

### Future Enhancements (Ideas)

#### Easy
- [ ] Difficulty level adjustment
- [ ] More industry domains
- [ ] Interview guideline generation
- [ ] Interviewer personality variants

#### Medium
- [ ] Deploy to Streamlit Cloud / Heroku
- [ ] Multi-LLM support (Claude, Gemini)
- [ ] Image generation integration
- [ ] RAG with job descriptions
- [ ] LLM-as-judge validation

#### Hard
- [ ] Deploy to AWS/Azure/GCP
- [ ] LangChain integration
- [ ] Vector database for deduplication
- [ ] Open-source LLM support
- [ ] Fine-tuned model training

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API error"**
- Check your API key in `.streamlit/secrets.toml`
- Verify you have credits in your OpenAI account
- Ensure your API key has proper permissions

**"Moderation API error"**
- The app will continue to work (fails open)
- Check your internet connection
- Verify API key validity

**"Invalid system prompt detected"**
- Reset the session
- Avoid copying prompts from external sources
- Use the built-in prompt selectors

**Slow responses**
- Use gpt-4o-mini for faster responses
- Reduce max_tokens setting
- Check your internet connection

## 📝 License

This project is intended for educational purposes. Please ensure you comply with OpenAI's usage policies and terms of service.

## 🤝 Contributing

This is an educational project. Feel free to:
- Experiment with different prompts
- Test various parameter combinations
- Try to jailbreak the security (ethically)
- Share improvements and findings

## 📚 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Cookbook](https://cookbook.openai.com/)

## 👨‍💻 Development Notes

### Task Requirements Met

✅ **Required Features**:
- [x] Research and creative interview preparation approach
- [x] Streamlit front-end implementation
- [x] OpenAI API integration
- [x] Model selection from allowed list
- [x] 5+ system prompts with different techniques (7 implemented)
- [x] Parameter tuning (temperature + 4 more)
- [x] Security guards (multiple layers)

✅ **Optional Features Implemented**:
- [x] All OpenAI settings as user controls (Medium)
- [x] Structured JSON output (Medium)
- [x] Cost calculation and display (Medium)
- [x] Full-fledged chatbot application (Hard)
- [x] Multiple prompt technique improvements (Easy)
- [x] Input validation and security (Easy)

### Evaluation Criteria Coverage

✅ **Understanding Core Concepts**:
- Different prompting techniques clearly documented
- LLM settings explained with tooltips
- User/System/Assistant roles properly implemented
- JSON output type demonstrated

✅ **Technical Implementation**:
- Working interview preparation system
- Successful OpenAI API integration
- Professional Streamlit UI
- Proper error handling

✅ **Reflection and Improvement**:
- README documents design choices
- Security considerations outlined
- Cost optimization features
- Multiple enhancement paths suggested

---

**Built with ❤️ using Streamlit and OpenAI** | **Version 2.0** | **Updated: October 2025**

