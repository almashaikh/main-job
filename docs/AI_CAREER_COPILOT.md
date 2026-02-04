# AI Career Copilot - Feature Documentation

## Overview

**AI Career Copilot** is a domain-specific chatbot assistant integrated into the SkillSphere platform. It helps users understand their skill gaps, guides their learning roadmap, tracks their progress, and assesses their interview readiness.

Unlike general-purpose chatbots, AI Career Copilot is **strictly scoped** to career development context, ensuring users receive focused, data-driven guidance based on their skill gap analysis.

## Features

### 1. **Skill Gap Explanations**
- Explains why specific skills are important for their target role
- Shows market demand percentages for each skill
- Clarifies priority levels (Critical, High, Medium, Low)
- Helps users understand the relevance of missing skills

**Example Questions:**
- "Why is Docker important for me?"
- "What's the market demand for Kubernetes?"
- "Why is this skill critical?"

### 2. **Learning Roadmap Guidance**
- Recommends what skill to learn next based on priority
- Explains the recommended learning sequence
- Justifies why skills should be learned in a specific order
- Guides skill progression from critical to supplementary skills

**Example Questions:**
- "What should I learn next?"
- "In what order should I learn these skills?"
- "What comes after I master this skill?"

### 3. **Progress Tracking**
- Shows overall learning progress percentage
- Displays module-by-module completion status
- Reviews assessment scores and identifies weak areas
- Recommends revision topics based on assessment performance

**Example Questions:**
- "How much progress have I made?"
- "Which modules should I review?"
- "What's my assessment score for this topic?"

### 4. **Module Completion & Revision Advice**
- Identifies topics with low assessment scores (<70%)
- Recommends focused revision for weak areas
- Tracks module completion status
- Provides structured learning guidance

**Example Questions:**
- "Do I need to review any modules?"
- "Am I ready to move to the next topic?"
- "What should I focus on next?"

### 5. **Interview Readiness Assessment**
- Evaluates overall interview readiness score (0-100)
- Analyzes readiness level and provides assessment message
- Identifies critical skill gaps that may be asked in interviews
- Provides actionable recommendations based on readiness level

**Example Questions:**
- "Am I interview ready?"
- "Am I ready for Cloud Engineer interviews?"
- "What should I prepare for before interviewing?"

### 6. **Recruiter-Mode Candidate Evaluation**
- Provides hiring perspective on candidate suitability
- Evaluates role match percentage
- Identifies candidate strengths and critical gaps
- Recommends hire/no-hire/conditional decisions

**Example Questions (Recruiter Mode):**
- "Is this candidate suitable?"
- "Should we hire this candidate?"
- "What are the critical gaps for this role?"

## Architecture

### Backend (Python/FastAPI)

**File:** `backend/career_copilot.py`

**Core Class:** `CareerCopilot`

Key Methods:
- `_classify_query()` - Determines if question is in-scope
- `_format_skill_gap_response()` - Handles skill-related questions
- `_format_learning_roadmap_response()` - Provides learning guidance
- `_format_progress_response()` - Tracks user progress
- `_format_interview_ready_response()` - Assesses interview readiness
- `_format_recruiter_evaluation_response()` - Recruiter perspective
- `process_message()` - Main message processing pipeline

**API Endpoints:**

1. **POST `/api/chatbot/message`**
   - Processes user message
   - Requires: `message`, `gap_analysis`
   - Optional: `user_progress`, `user_name`, `is_recruiter`
   - Returns: `response`, `category`, `confidence`, `is_in_scope`

2. **GET `/api/chatbot/history`**
   - Retrieves full conversation history
   - Returns: List of messages with roles and timestamps

3. **POST `/api/chatbot/clear`**
   - Clears conversation history
   - Returns: Success confirmation

### Frontend (React/Next.js)

**File:** `frontend/app/dashboard/ai-copilot/page.tsx`

**Features:**
- Real-time chat interface with message history
- Automatic scrolling to latest messages
- Loading indicator during API calls
- Example prompt buttons for quick start
- Clear history functionality
- Data persistence using sessionStorage/localStorage
- Responsive design (mobile and desktop)

**API Integration:**
- Connects to backend chatbot endpoints
- Loads gap analysis from sessionStorage/localStorage
- Supports user progress context
- Handles user and recruiter modes

## Scope Definition

### ✅ IN-SCOPE Questions

The chatbot ONLY answers questions about:

**Skill Gap Analysis:**
- Why specific skills are important
- Market demand for skills
- Priority and criticality of skills
- Gap explanations and relevance

**Learning Roadmap:**
- What skill to learn next
- Recommended learning sequence
- Topic and module recommendations
- Learning path guidance

**User Progress:**
- Completion percentage
- Module status
- Assessment scores
- Progress milestones

**Module & Revision:**
- Which topics to review
- Module completion status
- Assessment-based recommendations
- Revision advice

**Interview Readiness:**
- Overall readiness score
- Readiness level assessment
- Critical skill gaps for interviews
- Interview preparation guidance

**Recruiter Evaluation:**
- Candidate suitability
- Role match analysis
- Strength and gap assessment
- Hiring recommendations

### ❌ OUT-OF-SCOPE Questions

The chatbot REJECTS and does NOT answer:

- **General Queries:** Unrelated topics
- **Code Assistance:** Writing code, debugging, syntax errors
- **Generic Advice:** Motivational platitudes without data
- **Other Topics:** Weather, news, politics, health, general AI queries
- **Hallucinated Data:** No made-up statistics or information

**Response to Out-of-Scope:**
> "I appreciate the question, but I'm specifically designed to help with skill gap analysis, learning roadmap guidance, and interview readiness. Please ask me about your skills, what to learn next, your progress, or interview preparation!"

## System Prompt & Constraints

The chatbot operates under strict constraints:

```
ROLE:
You are NOT a general chatbot.
You act as a domain-specific assistant for skill gaps, learning, and interview readiness.

SCOPE (STRICT):
You ONLY answer questions about:
- Skill gap explanations
- Learning roadmap guidance
- User progress tracking
- Module completion and revision advice
- Interview readiness assessment
- Recruiter-style candidate evaluation

DO NOT:
- Answer unrelated questions
- Write code or provide coding help
- Give generic motivational advice
- Act like a general-purpose AI assistant
- Hallucinate data or make up statistics
- Reference platform names, APIs, or technical details

BEHAVIOR:
- Always give structured, clear, and explainable answers
- Base responses only on provided data
- Explain WHY a skill matters, not just WHAT to learn
- Be concise, professional, and supportive
- If user is not ready, clearly say so with next steps
```

## Response Format

### Skill Gap Response Example

```
**Docker**

**Market Demand:** 75% of jobs require this
**Priority Level:** Critical

**Why This Matters for You:** This is essential for your target role. Mastering this skill should be your immediate priority.

**Recommended Action:** Focus on this skill in your next learning phase.
```

### Learning Roadmap Response Example

```
**Learning Sequence - Why This Order?**

1. **Critical Skills First**
   Master these before interviews or role transitions.

2. **High-Priority Skills**
   They significantly improve your competitiveness.

3. **Medium-Priority Skills**
   Learn them to strengthen your overall profile.
```

### Interview Readiness Response Example

```
**Interview Readiness Assessment**

**Readiness Level:** Moderate
**Score:** 65/100

⚠️ You have 3 critical skill gaps. Interviewers will likely ask about these areas.
✓ Role match: 72%
△ Moderate readiness

**Recommendation:** Continue learning before scheduling interviews.
```

## Data Flow

```
User Question
     ↓
API Request → /api/chatbot/message
     ↓
Query Classification (category + confidence)
     ↓
Scope Validation (in-scope or out-of-scope)
     ↓
Response Generation (based on category and gap data)
     ↓
API Response → {response, category, confidence, is_in_scope}
     ↓
Frontend Display + History Storage
```

## Data Context

The chatbot receives and uses:

**Gap Analysis Data:**
```json
{
  "target_role": "Cloud Engineer",
  "match_percentage": 72,
  "total_required_skills": 15,
  "user_skills_count": 10,
  "matched_skills_count": 8,
  "missing_skills_count": 7,
  "readiness_score": {
    "score": 65,
    "level": "Moderate",
    "message": "Continue learning before interviews"
  },
  "skill_gaps": {
    "critical": [...],
    "high": [...],
    "medium": [...],
    "low": [...]
  }
}
```

**User Progress Data (Optional):**
```json
{
  "total_modules": 10,
  "completed_modules": 6,
  "modules": {
    "Docker Basics": { "completion": 100 },
    "Kubernetes": { "completion": 60 }
  },
  "assessments": {
    "Docker Assessment": 85,
    "Kubernetes Assessment": 68
  }
}
```

## Usage Guide

### For Regular Users

1. **Complete Gap Analysis First**
   - Run the gap analyzer to populate skill data
   - This enables personalized responses

2. **Ask Specific Questions**
   - "Why is Kubernetes critical?"
   - "What should I learn after Docker?"
   - "Am I interview ready?"

3. **Track Progress**
   - Update progress data after completing modules
   - Ask about revision recommendations
   - Check interview readiness regularly

4. **Use Example Prompts**
   - Click quick-start example buttons
   - Start with "What should I learn next?"

### For Recruiters

1. **Enable Recruiter Mode**
   - Set `is_recruiter=true` in API request
   - Backend switches to evaluation perspective

2. **Evaluate Candidates**
   - Ask: "Is this candidate suitable?"
   - Get hiring recommendations with detailed analysis
   - See strengths and critical gaps

3. **Review Scores**
   - Role match percentage
   - Readiness score
   - Recommendation level

## Integration Points

### 1. Dashboard Navigation
The chatbot is accessible from:
- Dashboard sidebar under "AI Career Copilot"
- Link: `/dashboard/ai-copilot`

### 2. Data Storage
The chatbot can access:
- Gap analysis from sessionStorage/localStorage
- User progress data if available
- User name and role (recruiter/user)

### 3. API Integration
Backend endpoints:
- Imports `CareerCopilot` class
- Initializes on API startup
- Maintains conversation history per session

## Benefits

✅ **Domain-Focused:** Only answers career-relevant questions
✅ **Data-Driven:** Responses based on actual gap analysis
✅ **Explainable:** Always explains WHY, not just WHAT
✅ **Non-Hallucinating:** Never makes up information
✅ **User-Friendly:** Clear, structured responses
✅ **Progress-Aware:** Tracks and guides learning
✅ **Interview-Ready:** Assesses interview readiness
✅ **Recruiter-Capable:** Supports hiring decisions

## Future Enhancements

1. **Conversational Context**
   - Track multi-turn conversations
   - Reference previous discussion points

2. **Adaptive Recommendations**
   - Suggest next skills based on past queries
   - Personalize learning paths

3. **Integration with Learning Modules**
   - Link to specific course resources
   - Recommend courses based on gaps

4. **Analytics & Insights**
   - Track most asked questions
   - Identify common learning bottlenecks
   - Generate insights for platform improvement

5. **Multi-Language Support**
   - Support queries in different languages
   - Provide localized responses

## Troubleshooting

**Issue:** Chatbot not responding
- Check if gap analysis data is loaded
- Verify backend API is running
- Check browser console for errors

**Issue:** Responses seem generic
- Run gap analysis first for personalized data
- Ensure gap analysis is saved before chatting

**Issue:** Chatbot answering out-of-scope questions
- Query classification confidence may be low
- Try being more specific about topic
- Rephrase to include skill/learning/progress keywords

## Files Modified/Created

**Created:**
- `backend/career_copilot.py` - Core chatbot logic
- `frontend/app/dashboard/ai-copilot/page.tsx` - Chat UI

**Modified:**
- `backend/api.py` - Added chatbot endpoints and imports
- `frontend/lib/api.ts` - Added chatbot API functions
- `frontend/app/dashboard/layout.tsx` - Added navigation link

## Testing Checklist

- [ ] Skill gap questions are answered with market data
- [ ] Learning roadmap provides sequence guidance
- [ ] Progress tracking shows completion percentages
- [ ] Interview readiness gives actionable feedback
- [ ] Out-of-scope questions are rejected politely
- [ ] Conversation history is maintained
- [ ] Clear history button works
- [ ] Mobile and desktop layouts work
- [ ] API responses are error-handled
- [ ] Data persistence works (localStorage/sessionStorage)
