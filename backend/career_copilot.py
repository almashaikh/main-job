"""
AI Career Copilot - Domain-Specific Chatbot
A specialized assistant for skill gap analysis, learning roadmap guidance,
and interview readiness assessment.
"""

from typing import List, Dict, Optional, Tuple
import json


class CareerCopilot:
    """
    Domain-specific chatbot for skill gap analysis platform.
    Handles user questions about skills, learning, progress, and interview readiness.
    """
    
    # System prompt defining the chatbot's role and constraints
    SYSTEM_CONTEXT = """
    You are AI Career Copilot, a domain-specific assistant for a skill gap analysis platform.
    Your ONLY purpose is to help users understand their skill gaps, learning roadmap, progress, 
    and interview readiness.
    
    You ONLY answer questions about:
    - Skill gap explanations (why certain skills are important)
    - Learning roadmap guidance (what to learn next, module recommendations)
    - User progress tracking (how much they've learned, completion status)
    - Module completion and revision advice (which topics to review)
    - Interview readiness assessment (are they ready for interviews)
    - Recruiter-style candidate evaluation (hiring perspective)
    
    You NEVER:
    - Answer unrelated questions (decline politely)
    - Write code or provide coding help
    - Give generic motivational advice
    - Act like a general-purpose AI assistant
    - Hallucinate data or make up statistics
    - Reference platform names, APIs, or technical implementation details
    """
    
    SCOPE_KEYWORDS = {
        'skill_gap': [
            'why', 'important', 'why this skill', 'skill matter', 'which skill',
            'priority', 'critical', 'essential', 'gap', 'missing'
        ],
        'learning_roadmap': [
            'learn', 'next', 'after', 'sequence', 'order', 'topic', 'module',
            'course', 'study', 'what should', 'which module', 'learning path'
        ],
        'progress': [
            'progress', 'completed', 'done', 'finished', 'how much', 'status',
            'percentage', 'score', 'assessment', 'revision', 'review'
        ],
        'interview_ready': [
            'interview', 'ready', 'prepared', 'eligible', 'qualified',
            'suitable', 'candidate', 'hire', 'recruiter'
        ]
    }
    
    OUT_OF_SCOPE = [
        'code', 'write code', 'programming', 'debug', 'error', 'syntax',
        'general', 'unrelated', 'joke', 'story', 'motivation', 'advice',
        'weather', 'news', 'politics', 'health'
    ]
    
    def __init__(self):
        """Initialize the Career Copilot"""
        self.conversation_history: List[Dict] = []
    
    def _classify_query(self, user_message: str) -> Tuple[str, float]:
        """
        Classify user query to determine if it's within scope
        
        Returns:
            (category, confidence) where category is one of:
            - skill_gap
            - learning_roadmap
            - progress
            - interview_ready
            - out_of_scope
        """
        message_lower = user_message.lower()
        
        # Check for out of scope first
        for keyword in self.OUT_OF_SCOPE:
            if keyword in message_lower:
                return ('out_of_scope', 0.8)
        
        # Check for in-scope categories
        scores = {}
        for category, keywords in self.SCOPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in message_lower)
            if score > 0:
                scores[category] = score / len(keywords)
        
        if scores:
            best_category = max(scores, key=scores.get)
            return (best_category, scores[best_category])
        
        return ('out_of_scope', 0.5)
    
    def _format_skill_gap_response(
        self,
        user_message: str,
        gap_analysis: Dict,
        user_skill_level: Optional[int] = None
    ) -> str:
        """Format response for skill gap related questions"""
        
        message_lower = user_message.lower()
        
        # Extract skill name from question
        skill_name = self._extract_skill_name(user_message, gap_analysis)
        
        if not skill_name:
            # General skill gap overview
            return self._generate_gap_overview(gap_analysis)
        
        # Specific skill explanation
        skill_data = self._find_skill_data(skill_name, gap_analysis)
        
        if not skill_data:
            return f"I don't have information about '{skill_name}' in your gap analysis. "
        
        response = f"**{skill_data['skill']}**\n\n"
        
        # Demand and relevance
        response += f"**Market Demand:** {skill_data.get('demand_percentage', 'N/A')}% of jobs require this\n"
        
        # Priority explanation
        priority = skill_data.get('demand_level', skill_data.get('priority', 'Medium'))
        response += f"**Priority Level:** {priority}\n\n"
        
        # Why it matters
        why_matters = self._explain_skill_importance(skill_data, gap_analysis)
        response += f"**Why This Matters for You:** {why_matters}\n\n"
        
        # Next steps
        response += "**Recommended Action:** "
        if priority == 'Critical':
            response += "This is essential for your target role. Focus on this skill in your next learning phase."
        elif priority == 'High':
            response += "This skill would significantly improve your job readiness. Consider prioritizing this after critical skills."
        else:
            response += "This is a valuable addition to your profile. Learn this after covering critical and high-priority skills."
        
        return response
    
    def _generate_gap_overview(self, gap_analysis: Dict) -> str:
        """Generate overview of skill gaps"""
        
        response = "**Your Skill Gap Analysis**\n\n"
        
        target_role = gap_analysis.get('target_role', 'Target Role')
        response += f"**Role:** {target_role}\n"
        response += f"**Match Percentage:** {gap_analysis.get('match_percentage', 0)}%\n\n"
        
        response += "**Summary:**\n"
        response += f"- Total required skills: {gap_analysis.get('total_required_skills', 0)}\n"
        response += f"- Skills you have: {gap_analysis.get('user_skills_count', 0)}\n"
        response += f"- Skills to acquire: {gap_analysis.get('missing_skills_count', 0)}\n\n"
        
        # Priority breakdown
        gaps_by_priority = gap_analysis.get('total_gaps_by_priority', {})
        if gaps_by_priority:
            response += "**Gaps by Priority:**\n"
            if gaps_by_priority.get('critical', 0) > 0:
                response += f"- Critical: {gaps_by_priority['critical']} skills\n"
            if gaps_by_priority.get('high', 0) > 0:
                response += f"- High: {gaps_by_priority['high']} skills\n"
            if gaps_by_priority.get('medium', 0) > 0:
                response += f"- Medium: {gaps_by_priority['medium']} skills\n"
            if gaps_by_priority.get('low', 0) > 0:
                response += f"- Low: {gaps_by_priority['low']} skills\n"
        
        response += "\nAsk me about specific skills to understand their importance!"
        
        return response
    
    def _format_learning_roadmap_response(
        self,
        user_message: str,
        gap_analysis: Dict,
        roadmap_data: Optional[Dict] = None
    ) -> str:
        """Format response for learning roadmap questions"""
        
        message_lower = user_message.lower()
        
        if 'next' in message_lower:
            return self._recommend_next_skill(gap_analysis)
        
        if 'order' in message_lower or 'sequence' in message_lower:
            return self._explain_learning_sequence(gap_analysis)
        
        # General roadmap guidance
        response = "**Your Learning Roadmap**\n\n"
        response += "I recommend learning skills in this priority order:\n\n"
        
        skill_gaps = gap_analysis.get('skill_gaps', {})
        priorities = ['critical', 'high', 'medium', 'low']
        
        for idx, priority in enumerate(priorities, 1):
            skills = skill_gaps.get(priority, [])
            if skills:
                response += f"**Phase {idx}: {priority.capitalize()} Priority Skills**\n"
                for skill in skills[:3]:  # Show top 3
                    response += f"- {skill.get('skill', skill)}\n"
                response += "\n"
        
        response += "Learn critical skills first, then high-priority, and build broader capabilities with medium and low-priority skills."
        
        return response
    
    def _format_progress_response(
        self,
        user_message: str,
        user_progress: Dict
    ) -> str:
        """Format response for progress tracking questions"""
        
        response = "**Your Learning Progress**\n\n"
        
        # Overall progress
        total_modules = user_progress.get('total_modules', 0)
        completed_modules = user_progress.get('completed_modules', 0)
        
        if total_modules > 0:
            progress_pct = (completed_modules / total_modules) * 100
            response += f"**Overall Progress:** {progress_pct:.0f}% ({completed_modules}/{total_modules} modules)\n\n"
        
        # Module-by-module status
        modules = user_progress.get('modules', {})
        if modules:
            response += "**Module Status:**\n"
            for module, status in modules.items():
                completion = status.get('completion', 0)
                response += f"- {module}: {completion}% complete\n"
            response += "\n"
        
        # Assessment scores
        assessments = user_progress.get('assessments', {})
        if assessments:
            response += "**Assessment Results:**\n"
            for assessment, score in assessments.items():
                response += f"- {assessment}: {score}%\n"
            response += "\n"
        
        # Revision recommendations
        response += "**Next Steps:**\n"
        low_score_modules = [m for m, s in assessments.items() if s < 70] if assessments else []
        
        if low_score_modules:
            response += f"Consider reviewing: {', '.join(low_score_modules)}\n"
        else:
            response += "Great progress! Continue with the next module in your roadmap."
        
        return response
    
    def _format_interview_ready_response(
        self,
        user_message: str,
        gap_analysis: Dict,
        user_progress: Optional[Dict] = None
    ) -> str:
        """Format response for interview readiness assessment"""
        
        readiness = gap_analysis.get('readiness_score', {})
        score = readiness.get('score', 0)
        level = readiness.get('level', 'Not Determined')
        
        response = "**Interview Readiness Assessment**\n\n"
        response += f"**Readiness Level:** {level}\n"
        response += f"**Score:** {score}/100\n"
        response += f"**Assessment:** {readiness.get('message', '')}\n\n"
        
        # Detailed breakdown
        gaps_by_priority = gap_analysis.get('total_gaps_by_priority', {})
        critical_gaps = gaps_by_priority.get('critical', 0)
        
        response += "**Interview Readiness Factors:**\n"
        
        if critical_gaps > 0:
            response += f"⚠️ You have {critical_gaps} critical skill gaps. "
            response += "Interviewers will likely ask about these areas.\n"
        else:
            response += "✓ No critical skill gaps.\n"
        
        match_pct = gap_analysis.get('match_percentage', 0)
        response += f"✓ Role match: {match_pct}%\n"
        
        if score >= 80:
            response += f"✓ Strong overall readiness\n\n"
            response += "You are well-prepared for interviews. "
            response += "Focus on articulating your experience and filling remaining gaps."
        elif score >= 60:
            response += f"△ Moderate readiness\n\n"
            response += "You have foundational knowledge but should strengthen critical areas "
            response += "before interviews. Focus on top-priority skills."
        else:
            response += f"✗ Limited readiness\n\n"
            response += "Continue learning before scheduling interviews. "
            response += "Prioritize critical and high-priority skills first."
        
        return response
    
    def _format_recruiter_evaluation_response(
        self,
        gap_analysis: Dict,
        candidate_name: Optional[str] = None
    ) -> str:
        """Format response for recruiter-mode candidate evaluation"""
        
        response = ""
        if candidate_name:
            response += f"**Candidate Evaluation: {candidate_name}**\n\n"
        else:
            response += "**Candidate Evaluation**\n\n"
        
        match_pct = gap_analysis.get('match_percentage', 0)
        readiness = gap_analysis.get('readiness_score', {})
        score = readiness.get('score', 0)
        
        response += f"**Role Match:** {match_pct}%\n"
        response += f"**Readiness Score:** {score}/100\n\n"
        
        # Strengths
        matched = gap_analysis.get('matched_skills_detailed', [])
        if matched:
            response += "**Strengths (Skills Match):**\n"
            top_matches = sorted(matched, key=lambda x: x.get('demand_percentage', 0), reverse=True)[:5]
            for skill in top_matches:
                response += f"- {skill['skill']} ({skill.get('demand_percentage', 0)}% market demand)\n"
            response += "\n"
        
        # Gaps
        skill_gaps = gap_analysis.get('skill_gaps', {})
        critical = skill_gaps.get('critical', [])
        
        if critical:
            response += f"**Critical Gaps ({len(critical)} skills):**\n"
            for gap in critical[:5]:
                response += f"- {gap.get('skill', gap)}\n"
            response += "\n"
        
        # Hiring recommendation
        response += "**Recommendation:**\n"
        if score >= 80:
            response += "✓ **READY TO HIRE** - Strong skill match and interview readiness"
        elif score >= 60:
            response += "△ **CONDITIONAL** - Has foundational skills but needs to address critical gaps before onboarding"
        else:
            response += "✗ **NOT READY** - Significant skill gaps. Candidate should complete learning before consideration"
        
        return response
    
    def _extract_skill_name(self, message: str, gap_analysis: Dict) -> Optional[str]:
        """Extract skill name from user message"""
        
        message_lower = message.lower()
        
        # Check all skills in gap analysis
        all_skills = []
        for priority in ['critical', 'high', 'medium', 'low']:
            skills = gap_analysis.get('skill_gaps', {}).get(priority, [])
            all_skills.extend([s.get('skill', s) if isinstance(s, dict) else s for s in skills])
        
        matched_skills = gap_analysis.get('matched_skills_detailed', [])
        all_skills.extend([s['skill'] for s in matched_skills])
        
        for skill in all_skills:
            if skill.lower() in message_lower:
                return skill
        
        return None
    
    def _find_skill_data(self, skill_name: str, gap_analysis: Dict) -> Optional[Dict]:
        """Find skill data in gap analysis"""
        
        # Check missing skills
        for priority in ['critical', 'high', 'medium', 'low']:
            skills = gap_analysis.get('skill_gaps', {}).get(priority, [])
            for skill in skills:
                if isinstance(skill, dict):
                    if skill.get('skill', '').lower() == skill_name.lower():
                        return skill
                elif skill.lower() == skill_name.lower():
                    return {'skill': skill, 'priority': priority}
        
        # Check matched skills
        matched = gap_analysis.get('matched_skills_detailed', [])
        for skill in matched:
            if skill['skill'].lower() == skill_name.lower():
                return skill
        
        return None
    
    def _explain_skill_importance(self, skill_data: Dict, gap_analysis: Dict) -> str:
        """Generate explanation for why a skill is important"""
        
        demand = skill_data.get('demand_percentage', 0)
        priority = skill_data.get('demand_level', skill_data.get('priority', 'Medium'))
        
        if demand > 80:
            return f"Nearly all jobs in this role ({demand}%) require this skill. It's fundamental to the position."
        elif demand > 60:
            return f"Most employers ({demand}%) seek this skill. It significantly increases your employability."
        elif demand > 40:
            return f"{demand}% of employers value this skill. It strengthens your profile and competitiveness."
        else:
            return f"{demand}% of employers need this skill. It's a nice-to-have that differentiates you from other candidates."
    
    def _recommend_next_skill(self, gap_analysis: Dict) -> str:
        """Recommend the next skill to learn"""
        
        skill_gaps = gap_analysis.get('skill_gaps', {})
        
        # Get first critical skill
        critical = skill_gaps.get('critical', [])
        if critical:
            skill = critical[0]
            skill_name = skill.get('skill', skill) if isinstance(skill, dict) else skill
            return f"**Learn {skill_name} next**\n\n" \
                   f"This is a critical gap for your target role. " \
                   f"Mastering this skill should be your immediate priority."
        
        # Fall back to high priority
        high = skill_gaps.get('high', [])
        if high:
            skill = high[0]
            skill_name = skill.get('skill', skill) if isinstance(skill, dict) else skill
            return f"**Learn {skill_name} next**\n\n" \
                   f"After covering critical skills, this high-priority skill will boost your readiness significantly."
        
        return "You've addressed the critical gaps! Continue with medium-priority skills to strengthen your profile."
    
    def _explain_learning_sequence(self, gap_analysis: Dict) -> str:
        """Explain the recommended learning sequence"""
        
        response = "**Learning Sequence - Why This Order?**\n\n"
        
        skill_gaps = gap_analysis.get('skill_gaps', {})
        target = gap_analysis.get('target_role', 'target role')
        
        response += f"1. **Critical Skills First**\n"
        response += f"   These are essential for {target}. "
        response += f"Master these before interviews or role transitions.\n\n"
        
        response += f"2. **High-Priority Skills**\n"
        response += f"   These are commonly required and expected. "
        response += f"They significantly improve your competitiveness.\n\n"
        
        response += f"3. **Medium-Priority Skills**\n"
        response += f"   These differentiate you from other candidates. "
        response += f"Learn them to strengthen your overall profile.\n\n"
        
        response += f"4. **Low-Priority Skills**\n"
        response += f"   Nice-to-have additions that demonstrate breadth. "
        response += f"Learn these after securing the core competencies."
        
        return response
    
    def process_message(
        self,
        user_message: str,
        gap_analysis: Dict,
        user_progress: Optional[Dict] = None,
        user_name: Optional[str] = None,
        is_recruiter: bool = False
    ) -> Dict:
        """
        Process user message and generate domain-specific response
        
        Args:
            user_message: User's question or statement
            gap_analysis: Current gap analysis data
            user_progress: Optional progress tracking data
            user_name: Optional user/candidate name
            is_recruiter: Whether responding in recruiter evaluation mode
            
        Returns:
            Response dict with message and metadata
        """
        
        # Classify the query
        category, confidence = self._classify_query(user_message)
        
        # Store in conversation history
        self.conversation_history.append({
            'role': 'user',
            'message': user_message,
            'category': category,
            'confidence': confidence
        })
        
        # Generate response based on category
        if category == 'out_of_scope':
            response_text = (
                "I appreciate the question, but I'm specifically designed to help with skill gap analysis, "
                "learning roadmap guidance, and interview readiness. "
                "Please ask me about your skills, what to learn next, your progress, or interview preparation!"
            )
        
        elif category == 'skill_gap':
            response_text = self._format_skill_gap_response(user_message, gap_analysis)
        
        elif category == 'learning_roadmap':
            response_text = self._format_learning_roadmap_response(user_message, gap_analysis)
        
        elif category == 'progress':
            if user_progress:
                response_text = self._format_progress_response(user_message, user_progress)
            else:
                response_text = "I don't have your progress data yet. Upload your resume and complete assessments to track your progress."
        
        elif category == 'interview_ready':
            if is_recruiter:
                response_text = self._format_recruiter_evaluation_response(gap_analysis, user_name)
            else:
                response_text = self._format_interview_ready_response(user_message, gap_analysis, user_progress)
        
        else:
            response_text = "I'm not sure how to help with that. Ask me about skill gaps, learning paths, progress, or interview readiness!"
        
        # Store response in history
        self.conversation_history.append({
            'role': 'assistant',
            'message': response_text,
            'category': category
        })
        
        return {
            'response': response_text,
            'category': category,
            'confidence': confidence,
            'is_in_scope': category != 'out_of_scope'
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
