"""
Smart Resume Feedback & Improvement Suggestions
Analyzes resume quality, skill density, formatting, and provides actionable improvements
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter
from pathlib import Path

class ResumeFeedbackAnalyzer:
    """Analyze resume and provide improvement suggestions"""
    
    def __init__(self):
        # Impact words that strengthen resume
        self.impact_words = {
            'action': ['built', 'created', 'developed', 'designed', 'implemented', 'launched'],
            'performance': ['optimized', 'improved', 'accelerated', 'enhanced', 'boosted', 'scaled'],
            'quantifiable': ['increased', 'reduced', 'achieved', 'generated', 'saved', 'earned'],
            'leadership': ['led', 'managed', 'directed', 'mentored', 'supervised', 'coordinated'],
            'innovation': ['pioneered', 'revolutionized', 'transformed', 'innovated', 'spearheaded'],
            'technical': ['integrated', 'automated', 'architected', 'engineered', 'deployed']
        }
        
        # Common resume formatting issues
        self.formatting_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b',
            'url': r'https?://[^\s]+|www\.[^\s]+',
            'linked_in': r'linkedin\.com/in/[\w-]+'
        }
        
    def analyze_resume(self, resume_text: str, skills: List[str], target_role: str = None) -> Dict:
        """
        Comprehensive resume analysis
        
        Args:
            resume_text: Full resume text
            skills: Extracted skills from resume
            target_role: Optional target job role for relevance analysis
            
        Returns:
            Dictionary with feedback scores and suggestions
        """
        
        feedback = {
            'overall_score': 0,
            'skill_density_analysis': self._analyze_skill_density(resume_text, skills),
            'impact_words_analysis': self._analyze_impact_words(resume_text),
            'formatting_analysis': self._analyze_formatting(resume_text),
            'relevance_analysis': self._analyze_skill_relevance(skills, target_role) if target_role else {'score': 0, 'feedback': 'No target role provided'},
            'improvement_suggestions': []
        }
        
        # Calculate overall score
        feedback['overall_score'] = self._calculate_overall_score(feedback)
        
        # Generate actionable suggestions
        feedback['improvement_suggestions'] = self._generate_suggestions(feedback)
        
        return feedback
    
    def _analyze_skill_density(self, resume_text: str, skills: List[str]) -> Dict:
        """
        Analyze if skills are scattered or focused
        Skill density = total skill mentions / total words
        """
        total_words = len(resume_text.split())
        skill_mentions = 0
        skill_frequency = Counter()
        
        resume_lower = resume_text.lower()
        
        # Count skill mentions
        for skill in skills:
            skill_lower = skill.lower()
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            matches = len(re.findall(pattern, resume_lower))
            skill_mentions += matches
            skill_frequency[skill] = matches
        
        # Calculate density
        density_percentage = (skill_mentions / total_words * 100) if total_words > 0 else 0
        
        # Analyze distribution
        unique_skills = len(skills)
        avg_mentions_per_skill = skill_mentions / unique_skills if unique_skills > 0 else 0
        
        # Determine if skills are focused or scattered
        if density_percentage > 8:
            density_status = 'Excellent - Well integrated'
            density_score = 100
        elif density_percentage > 5:
            density_status = 'Good - Balanced distribution'
            density_score = 80
        elif density_percentage > 2:
            density_status = 'Fair - Could be improved'
            density_score = 60
        else:
            density_status = 'Poor - Skills underrepresented'
            density_score = 40
        
        top_skills = [skill for skill, count in skill_frequency.most_common(5)]
        
        return {
            'score': density_score,
            'status': density_status,
            'density_percentage': round(density_percentage, 2),
            'total_skill_mentions': skill_mentions,
            'unique_skills': unique_skills,
            'avg_mentions_per_skill': round(avg_mentions_per_skill, 2),
            'top_skills': top_skills,
            'details': f"Your resume has {density_percentage:.1f}% skill density. "
                      f"Skills mentioned {skill_mentions} times across {total_words} words."
        }
    
    def _analyze_impact_words(self, resume_text: str) -> Dict:
        """
        Identify missing and present impact words
        """
        resume_lower = resume_text.lower()
        found_impact_words = {}
        missing_categories = {}
        total_impact_found = 0
        
        for category, words in self.impact_words.items():
            found = []
            for word in words:
                pattern = r'\b' + re.escape(word) + r'\b'
                if re.search(pattern, resume_lower):
                    found.append(word)
                    total_impact_found += 1
            
            found_impact_words[category] = found
            missing_categories[category] = [w for w in words if w not in found]
        
        # Score impact words
        total_categories = len(self.impact_words)
        categories_with_words = sum(1 for v in found_impact_words.values() if len(v) > 0)
        
        if categories_with_words >= 5:
            impact_score = 90
            impact_status = 'Excellent'
        elif categories_with_words >= 4:
            impact_score = 75
            impact_status = 'Good'
        elif categories_with_words >= 3:
            impact_score = 60
            impact_status = 'Fair'
        else:
            impact_score = 40
            impact_status = 'Needs Improvement'
        
        return {
            'score': impact_score,
            'status': impact_status,
            'total_impact_words_found': total_impact_found,
            'categories_with_words': categories_with_words,
            'found_words': found_impact_words,
            'missing_words': missing_categories,
            'priority_missing': missing_categories.get('action', []) + missing_categories.get('performance', [])
        }
    
    def _analyze_formatting(self, resume_text: str) -> Dict:
        """
        Check resume formatting quality
        """
        issues = []
        score = 100
        
        # Check for contact information
        has_email = bool(re.search(self.formatting_patterns['email'], resume_text))
        has_phone = bool(re.search(self.formatting_patterns['phone'], resume_text))
        has_linkedin = bool(re.search(self.formatting_patterns['linked_in'], resume_text))
        
        contact_info_count = sum([has_email, has_phone, has_linkedin])
        
        if contact_info_count < 2:
            issues.append('Missing contact information (email/phone/LinkedIn)')
            score -= 15
        
        # Check for proper structure (sections)
        required_sections = ['experience', 'skills', 'education']
        found_sections = sum(1 for section in required_sections if section.lower() in resume_text.lower())
        
        if found_sections < 3:
            issues.append(f'Missing or unclear sections. Found {found_sections}/3 required sections')
            score -= 10
        
        # Check for readability (line length, excessive special characters)
        lines = resume_text.split('\n')
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        
        if avg_line_length > 120:
            issues.append('Lines too long - may affect readability')
            score -= 10
        elif avg_line_length < 20:
            issues.append('Lines too short - may indicate poor formatting')
            score -= 10
        
        # Check for bullet points/structure
        bullet_points = len(re.findall(r'[•\-\*]', resume_text))
        if bullet_points < 5:
            issues.append('Consider using bullet points for better readability')
            score -= 5
        
        # Check word count
        word_count = len(resume_text.split())
        if word_count < 300:
            issues.append('Resume may be too brief - consider adding more details')
            score -= 5
        elif word_count > 1000:
            issues.append('Resume may be too long - consider condensing')
            score -= 5
        
        format_status = 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs Work'
        
        return {
            'score': score,
            'status': format_status,
            'contact_info_found': {
                'email': has_email,
                'phone': has_phone,
                'linkedin': has_linkedin
            },
            'sections_found': found_sections,
            'word_count': word_count,
            'avg_line_length': round(avg_line_length, 1),
            'bullet_points': bullet_points,
            'issues': issues,
            'details': f"Your resume has {word_count} words, {found_sections} clear sections, and {bullet_points} bullet points."
        }
    
    def _analyze_skill_relevance(self, skills: List[str], target_role: str) -> Dict:
        """
        Analyze relevance of extracted skills to target role
        """
        if not target_role or not skills:
            return {'score': 0, 'feedback': 'Insufficient data for relevance analysis'}
        
        # Define role categories and their related skills
        role_skill_mapping = {
            'software engineer': ['python', 'java', 'javascript', 'c++', 'sql', 'git', 'api', 'rest', 'microservices'],
            'data scientist': ['python', 'machine learning', 'sql', 'tableau', 'pandas', 'numpy', 'scikit-learn', 'statistics'],
            'product manager': ['product management', 'agile', 'user research', 'analytics', 'strategy', 'roadmap', 'jira'],
            'devops engineer': ['docker', 'kubernetes', 'jenkins', 'terraform', 'aws', 'azure', 'ci/cd', 'linux'],
            'frontend developer': ['javascript', 'react', 'vue', 'css', 'html', 'typescript', 'webpack', 'responsive design'],
            'backend developer': ['python', 'java', 'nodejs', 'sql', 'database', 'api', 'microservices', 'docker'],
            'qa engineer': ['testing', 'selenium', 'automation', 'jira', 'bug tracking', 'performance testing'],
            'cloud architect': ['aws', 'azure', 'gcp', 'terraform', 'kubernetes', 'microservices', 'security'],
            'security engineer': ['security', 'firewall', 'encryption', 'penetration testing', 'compliance', 'authentication'],
        }
        
        target_lower = target_role.lower()
        skills_lower = [s.lower() for s in skills]
        
        # Find matching role category
        matching_roles = [role for role in role_skill_mapping.keys() if role in target_lower or target_lower in role]
        
        if not matching_roles:
            # Try partial matching
            for role in role_skill_mapping.keys():
                if any(word in role for word in target_lower.split()):
                    matching_roles.append(role)
        
        if matching_roles:
            expected_skills = set()
            for role in matching_roles:
                expected_skills.update(role_skill_mapping[role])
            
            matched_count = sum(1 for skill in skills_lower if skill in expected_skills)
            relevance_score = int((matched_count / len(expected_skills)) * 100) if expected_skills else 0
            
            missing_skills = [s for s in expected_skills if s not in skills_lower][:5]
            
            relevance_status = 'Highly Relevant' if relevance_score >= 70 else 'Moderately Relevant' if relevance_score >= 40 else 'Needs Work'
        else:
            relevance_score = 50
            relevance_status = 'Unknown Role Type'
            missing_skills = []
        
        return {
            'score': relevance_score,
            'status': relevance_status,
            'matched_skills': matched_count if matching_roles else 0,
            'missing_critical_skills': missing_skills,
            'target_role': target_role,
            'details': f"{matched_count if matching_roles else 0} of your skills align with {target_role} requirements."
        }
    
    def _calculate_overall_score(self, feedback: Dict) -> int:
        """Calculate weighted overall score"""
        weights = {
            'skill_density_analysis': 0.25,
            'impact_words_analysis': 0.25,
            'formatting_analysis': 0.25,
            'relevance_analysis': 0.25
        }
        
        total_score = 0
        for key, weight in weights.items():
            if key in feedback and 'score' in feedback[key]:
                total_score += feedback[key]['score'] * weight
        
        return int(total_score)
    
    def _generate_suggestions(self, feedback: Dict) -> List[Dict]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Skill density suggestions
        density_score = feedback['skill_density_analysis']['score']
        if density_score < 70:
            suggestions.append({
                'category': 'Skill Integration',
                'priority': 'High' if density_score < 50 else 'Medium',
                'suggestion': 'Integrate your technical skills throughout your work experience descriptions rather than listing them separately',
                'impact': 'Improves skill visibility and demonstrates practical application'
            })
        
        # Impact words suggestions
        impact_analysis = feedback['impact_words_analysis']
        missing_priority = impact_analysis.get('priority_missing', [])
        if missing_priority and impact_analysis['score'] < 80:
            suggestions.append({
                'category': 'Action Verbs',
                'priority': 'High',
                'suggestion': f'Use action verbs like {", ".join(missing_priority[:3])} to strengthen your accomplishments',
                'impact': 'Makes your achievements more impactful and memorable to recruiters'
            })
        
        # Formatting suggestions
        format_issues = feedback['formatting_analysis'].get('issues', [])
        if format_issues:
            for issue in format_issues[:2]:  # Top 2 issues
                suggestions.append({
                    'category': 'Formatting',
                    'priority': 'Medium',
                    'suggestion': issue,
                    'impact': 'Improves readability and first impressions'
                })
        
        # Relevance suggestions
        relevance = feedback['relevance_analysis']
        missing_skills = relevance.get('missing_critical_skills', [])
        if missing_skills and relevance['score'] < 70:
            suggestions.append({
                'category': 'Skills Gap',
                'priority': 'High',
                'suggestion': f'Consider developing skills in: {", ".join(missing_skills[:3])}',
                'impact': 'Aligns your profile better with target role requirements'
            })
        
        # General best practices
        if feedback['overall_score'] < 70:
            suggestions.append({
                'category': 'Overall Quality',
                'priority': 'High',
                'suggestion': 'Review and update your resume following the feedback above to improve competitiveness',
                'impact': 'Increases chances of getting interviews for target roles'
            })
        
        return suggestions
