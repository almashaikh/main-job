"""
Gap Analyzer Module
Compares user skills with job market requirements
Enhanced with weighted matching and smart skill comparison
"""

import json
from typing import Dict, List, Set, Tuple
from pathlib import Path

# Import skill database functions for smart matching
try:
    from skill_database import get_skill_variations, normalize_skill
    SKILL_MATCHING_AVAILABLE = True
except ImportError:
    SKILL_MATCHING_AVAILABLE = False


class GapAnalyzer:
    """Analyze skill gaps between user and market demand"""
    
    def __init__(self):
        self.use_smart_matching = SKILL_MATCHING_AVAILABLE
    
    
    def analyze_gap(
        self, 
        user_skills: List[str], 
        market_skills: List[Dict],
        target_role: str = None
    ) -> Dict:
        """
        Compare user skills with market demand using weighted matching
        
        Args:
            user_skills: List of skills from user's resume
            market_skills: List of skill demand data from market analysis
            target_role: Name of target role
            
        Returns:
            Enhanced gap analysis results with weighted matching
        """
        
        print("\n" + "="*60)
        print("🎯 SKILL GAP ANALYSIS (Enhanced)")
        if target_role:
            print(f"Target Role: {target_role}")
        print("="*60)
        
        # Prepare skill matching
        market_skills_dict = {s['skill']: s for s in market_skills}
        required_skills_set = set(market_skills_dict.keys())
        
        # Smart skill matching with variations
        matched_skills = set()
        matched_skills_info = []
        user_skills_normalized = {}  # Track which user skill matched which market skill
        
        for user_skill in user_skills:
            match_found = False
            
            # Direct match
            if user_skill in required_skills_set:
                matched_skills.add(user_skill)
                match_found = True
                user_skills_normalized[user_skill] = user_skill
            
            # Smart matching with variations (if available)
            elif self.use_smart_matching:
                user_variations = get_skill_variations(user_skill)
                for variation in user_variations:
                    if variation in required_skills_set:
                        matched_skills.add(variation)
                        match_found = True
                        user_skills_normalized[user_skill] = variation
                        break
                
                # Try reverse: check if any market skill matches user skill variations
                if not match_found:
                    for market_skill in required_skills_set:
                        market_variations = get_skill_variations(market_skill)
                        if user_skill in market_variations:
                            matched_skills.add(market_skill)
                            match_found = True
                            user_skills_normalized[user_skill] = market_skill
                            break
        
        # Calculate gaps
        user_skills_set = set(user_skills)
        missing_skills = required_skills_set - matched_skills
        extra_skills = user_skills_set - set(user_skills_normalized.keys())
        
        # WEIGHTED MATCH PERCENTAGE (Improvement #1)
        # Instead of simple count, weight by demand percentage
        total_weight = sum(s['percentage'] for s in market_skills)
        matched_weight = sum(
            market_skills_dict[skill]['percentage'] 
            for skill in matched_skills 
            if skill in market_skills_dict
        )
        
        weighted_match_percentage = (matched_weight / total_weight * 100) if total_weight > 0 else 0
        
        # Simple match for comparison
        simple_match_percentage = (len(matched_skills) / len(required_skills_set) * 100) if required_skills_set else 0
        
        print(f"📊 Weighted Match: {weighted_match_percentage:.1f}% | Simple Match: {simple_match_percentage:.1f}%")
        
        # SKILL LEVEL WEIGHTING (Improvement #3)
        # Categorize by demand level with weights
        demand_weights = {
            'Critical': 1.0,
            'High': 0.8,
            'Medium': 0.5,
            'Low': 0.3
        }
        
        # Categorize missing skills by priority
        critical_gaps = []
        high_priority_gaps = []
        medium_priority_gaps = []
        low_priority_gaps = []
        
        for skill in missing_skills:
            skill_data = market_skills_dict[skill]
            demand_level = skill_data['demand_level']
            
            gap_info = {
                'skill': skill,
                'demand_percentage': skill_data['percentage'],
                'job_count': skill_data['count'],
                'priority': demand_level,
                'weight': demand_weights.get(demand_level, 0.5)
            }
            
            if demand_level == 'Critical':
                critical_gaps.append(gap_info)
            elif demand_level == 'High':
                high_priority_gaps.append(gap_info)
            elif demand_level == 'Medium':
                medium_priority_gaps.append(gap_info)
            else:
                low_priority_gaps.append(gap_info)
        
        # Sort each category by demand percentage
        critical_gaps.sort(key=lambda x: x['demand_percentage'], reverse=True)
        high_priority_gaps.sort(key=lambda x: x['demand_percentage'], reverse=True)
        medium_priority_gaps.sort(key=lambda x: x['demand_percentage'], reverse=True)
        low_priority_gaps.sort(key=lambda x: x['demand_percentage'], reverse=True)
        
        # Categorize matched skills by demand level
        critical_matched = []
        high_matched = []
        medium_matched = []
        low_matched = []
        
        for skill in matched_skills:
            if skill in market_skills_dict:
                skill_data = market_skills_dict[skill]
                demand_level = skill_data['demand_level']
                
                skill_info = {
                    'skill': skill,
                    'demand_percentage': skill_data['percentage'],
                    'demand_level': demand_level,
                    'weight': demand_weights.get(demand_level, 0.5)
                }
                
                matched_skills_info.append(skill_info)
                
                if demand_level == 'Critical':
                    critical_matched.append(skill_info)
                elif demand_level == 'High':
                    high_matched.append(skill_info)
                elif demand_level == 'Medium':
                    medium_matched.append(skill_info)
                else:
                    low_matched.append(skill_info)
        
        matched_skills_info.sort(key=lambda x: x['demand_percentage'], reverse=True)
        
        # Create result dictionary
        result = {
            'target_role': target_role,
            'match_percentage': round(weighted_match_percentage, 2),  # Use weighted match
            'simple_match_percentage': round(simple_match_percentage, 2),  # Keep simple for reference
            'total_required_skills': len(required_skills_set),
            'user_skills_count': len(user_skills_set),
            'matched_skills_count': len(matched_skills),
            'missing_skills_count': len(missing_skills),
            'extra_skills_count': len(extra_skills),
            
            'summary': {
                'matched_count': len(matched_skills),
                'missing_count': len(missing_skills),
                'extra_count': len(extra_skills)
            },
            
            'matched_skills': sorted(list(matched_skills)),
            'matched_skills_detailed': matched_skills_info,
            
            # Breakdown by priority
            'matched_by_priority': {
                'critical': len(critical_matched),
                'high': len(high_matched),
                'medium': len(medium_matched),
                'low': len(low_matched)
            },
            
            'skill_gaps': {
                'critical': critical_gaps,
                'high': high_priority_gaps,
                'medium': medium_priority_gaps,
                'low': low_priority_gaps
            },
            
            'total_gaps_by_priority': {
                'critical': len(critical_gaps),
                'high': len(high_priority_gaps),
                'medium': len(medium_priority_gaps),
                'low': len(low_priority_gaps)
            },
            
            'extra_skills': sorted(list(extra_skills)),
            
            # ENHANCED READINESS SCORE (Improvement #4)
            'readiness_score': self._calculate_enhanced_readiness(
                weighted_match_percentage=weighted_match_percentage,
                critical_matched=len(critical_matched),
                critical_gaps=len(critical_gaps),
                high_matched=len(high_matched),
                high_gaps=len(high_priority_gaps),
                extra_skills_count=len(extra_skills),
                total_critical=len(critical_matched) + len(critical_gaps),
                total_high=len(high_matched) + len(high_priority_gaps)
            ),
            
            'recommendations': self._generate_enhanced_recommendations(
                weighted_match_percentage,
                critical_gaps,
                high_priority_gaps,
                critical_matched,
                high_matched
            )
        }
        
        return result
    
    
    def _calculate_enhanced_readiness(
        self,
        weighted_match_percentage: float,
        critical_matched: int,
        critical_gaps: int,
        high_matched: int,
        high_gaps: int,
        extra_skills_count: int,
        total_critical: int,
        total_high: int
    ) -> Dict:
        """
        Enhanced readiness calculation with smarter weighting
        
        Considers:
        - Weighted match percentage (not just count)
        - % of critical skills you HAVE (not just missing)
        - Extra skills as bonus
        - Proportional penalties
        """
        
        # Start with weighted match percentage
        score = weighted_match_percentage
        
        # Calculate critical skill coverage
        critical_coverage = (critical_matched / total_critical * 100) if total_critical > 0 else 100
        
        # Boost score if you have most critical skills
        if critical_coverage >= 80:
            score += 5  # Bonus for having most critical skills
        elif critical_coverage < 50:
            score -= 10  # Penalty for missing many critical skills
        
        # Dynamic penalty based on proportion of gaps
        if total_critical > 0:
            critical_gap_ratio = critical_gaps / total_critical
            score -= (critical_gap_ratio * 20)  # Max -20 if missing all critical
        
        if total_high > 0:
            high_gap_ratio = high_gaps / total_high
            score -= (high_gap_ratio * 10)  # Max -10 if missing all high priority
        
        # Bonus for extra skills (shows versatility)
        if extra_skills_count > 0:
            extra_bonus = min(extra_skills_count * 0.5, 5)  # Max +5 bonus
            score += extra_bonus
        
        # Ensure score is between 0-100
        score = max(0, min(100, score))
        
        # Determine readiness level with more nuanced thresholds
        if score >= 85:
            level = "Excellent"
            message = "You're highly qualified! Strong match across critical skills."
        elif score >= 70:
            level = "Good"
            message = "Strong foundation. Address critical gaps to maximize chances."
        elif score >= 50:
            level = "Fair"
            message = "Decent base, but several key skills need development."
        elif score >= 30:
            level = "Needs Improvement"
            message = "Significant upskilling required for this role."
        else:
            level = "Not Ready"
            message = "Major skill gaps. Consider related roles or intensive training."
        
        return {
            'score': round(score, 2),
            'level': level,
            'message': message,
            'critical_coverage': round(critical_coverage, 1)
        }
    
    
    def _generate_enhanced_recommendations(
        self,
        match_percentage: float,
        critical_gaps: List[Dict],
        high_gaps: List[Dict],
        critical_matched: List[Dict],
        high_matched: List[Dict]
    ) -> List[str]:
        """Enhanced recommendations based on comprehensive analysis"""
        
        recommendations = []
        
        total_critical = len(critical_matched) + len(critical_gaps)
        critical_coverage = (len(critical_matched) / total_critical * 100) if total_critical > 0 else 100
        
        # Overall assessment
        if match_percentage >= 85:
            recommendations.append("✅ Excellent match! You're well-positioned for this role.")
            recommendations.append("💼 Recommended action: Start applying to jobs immediately.")
            recommendations.append("🎯 Focus: Build portfolio projects showcasing your skills.")
        elif match_percentage >= 70:
            recommendations.append("💪 Strong foundation! You're close to job-ready.")
            recommendations.append("⏱️ Estimated prep time: 2-4 weeks of focused learning.")
        elif match_percentage >= 50:
            recommendations.append("📚 Moderate skill gaps detected.")
            recommendations.append("⏱️ Estimated prep time: 1-3 months of structured learning.")
        else:
            recommendations.append("🎯 Significant learning path ahead.")
            recommendations.append("⏱️ Estimated prep time: 3-6 months intensive training.")
        
        # Critical skills analysis
        if critical_gaps:
            top_critical = [g['skill'] for g in critical_gaps[:4]]
            demand_str = f" (avg {sum(g['demand_percentage'] for g in critical_gaps[:4])/len(critical_gaps[:4]):.0f}% demand)"
            recommendations.append(f"🔴 TOP PRIORITY: {', '.join(top_critical)}{demand_str}")
            
            if critical_coverage < 50:
                recommendations.append("⚠️ Warning: Less than 50% of critical skills covered. Focus here first!")
        else:
            recommendations.append("✅ All critical skills covered! Great job!")
        
        # High priority skills
        if high_gaps:
            top_high = [g['skill'] for g in high_gaps[:3]]
            recommendations.append(f"🟠 IMPORTANT NEXT: {', '.join(top_high)}")
        
        # Positive reinforcement for matched critical skills
        if len(critical_matched) >= 3:
            top_strengths = [s['skill'] for s in critical_matched[:3]]
            recommendations.append(f"💪 Your strengths: {', '.join(top_strengths)} - leverage these!")
        
        return recommendations


def load_market_analysis(file_path: str) -> List[Dict]:
    """Load market skill analysis from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['skills']


def display_gap_analysis(analysis: Dict):
    """Display gap analysis results in a formatted way"""
    
    print("\n" + "="*60)
    print("📊 SKILL GAP ANALYSIS RESULTS")
    print("="*60)
    
    # Overview
    print(f"\n📈 Overview:")
    print(f"  • Target Role: {analysis.get('target_role', 'N/A')}")
    print(f"  • Match Percentage: {analysis['match_percentage']}%")
    print(f"  • Your Skills: {analysis['user_skills_count']}")
    print(f"  • Required Skills: {analysis['total_required_skills']}")
    print(f"  • Matched: {analysis['matched_skills_count']} ✅")
    print(f"  • Missing: {analysis['missing_skills_count']} ⚠️")
    
    # Readiness Score
    readiness = analysis['readiness_score']
    print(f"\n🎯 Job Readiness:")
    print(f"  Score: {readiness['score']}/100")
    print(f"  Level: {readiness['level']}")
    print(f"  {readiness['message']}")
    
    # Matched Skills
    print(f"\n✅ YOUR MATCHING SKILLS ({len(analysis['matched_skills'])}):")
    matched_detailed = analysis['matched_skills_detailed'][:10]  # Show top 10
    for skill_info in matched_detailed:
        skill = skill_info['skill']
        demand = skill_info['demand_percentage']
        level = skill_info['demand_level']
        emoji = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🔵'}[level]
        print(f"  {emoji} {skill:<30} (Demand: {demand}%)")
    
    if len(analysis['matched_skills']) > 10:
        print(f"  ... and {len(analysis['matched_skills']) - 10} more")
    
    # Skill Gaps by Priority
    gaps = analysis['skill_gaps']
    gap_counts = analysis['total_gaps_by_priority']
    
    print(f"\n⚠️  SKILL GAPS TO FILL:")
    
    if gaps['critical']:
        print(f"\n  🔴 CRITICAL GAPS ({gap_counts['critical']}) - LEARN THESE FIRST:")
        for i, gap in enumerate(gaps['critical'][:10], 1):
            print(f"     {i}. {gap['skill']:<30} (Demand: {gap['demand_percentage']}%)")
    
    if gaps['high']:
        print(f"\n  🟠 HIGH PRIORITY GAPS ({gap_counts['high']}):")
        for i, gap in enumerate(gaps['high'][:10], 1):
            print(f"     {i}. {gap['skill']:<30} (Demand: {gap['demand_percentage']}%)")
    
    if gaps['medium']:
        print(f"\n  🟡 MEDIUM PRIORITY GAPS ({gap_counts['medium']}):")
        for i, gap in enumerate(gaps['medium'][:5], 1):
            print(f"     {i}. {gap['skill']:<30} (Demand: {gap['demand_percentage']}%)")
    
    # Extra Skills
    if analysis['extra_skills']:
        print(f"\n💼 ADDITIONAL SKILLS YOU HAVE ({len(analysis['extra_skills'])}):")
        print(f"  (Not commonly required for this role, but valuable!)")
        for skill in analysis['extra_skills'][:10]:
            print(f"  • {skill}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    for rec in analysis['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "="*60)


def save_gap_analysis(analysis: Dict, output_file: str):
    """Save gap analysis to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Analysis saved to: {output_file}")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "🎯"*30)
    print("SKILL GAP ANALYZER")
    print("🎯"*30)
    
    # Import resume parser to get user skills
    from resume_parser import parse_resume
    
    try:
        # Step 1: Get user's resume
        print("\n📄 Step 1: Upload your resume")
        resume_path = input("Enter path to your resume (PDF/DOCX): ").strip()
        
        print(f"\n📂 Parsing resume...")
        resume_data = parse_resume(resume_path)
        user_skills = resume_data['skills']
        
        print(f"✅ Found {len(user_skills)} skills in your resume")
        
        # Step 2: Get market analysis
        print("\n📊 Step 2: Load market skill analysis")
        
        # Find analysis files
        analysis_files = list(Path('.').glob('skill_analysis*.json'))
        
        if analysis_files:
            print(f"\nFound {len(analysis_files)} analysis file(s):")
            for i, f in enumerate(analysis_files, 1):
                print(f"  {i}. {f.name}")
            
            file_choice = int(input(f"\nSelect file (1-{len(analysis_files)}): ")) - 1
            analysis_file = str(analysis_files[file_choice])
        else:
            analysis_file = input("Enter path to skill analysis JSON file: ").strip()
        
        print(f"\n📂 Loading market analysis from: {analysis_file}")
        market_skills = load_market_analysis(analysis_file)
        
        # Extract role name from filename
        role_name = Path(analysis_file).stem.replace('skill_analysis_', '').replace('_', ' ').title()
        if role_name == 'Skill Analysis':
            role_name = input("Enter target role name: ").strip()
        
        # Step 3: Perform gap analysis
        print(f"\n🔍 Analyzing skill gaps...")
        analyzer = GapAnalyzer()
        results = analyzer.analyze_gap(user_skills, market_skills, role_name)
        
        # Display results
        display_gap_analysis(results)
        
        # Save results
        output_file = f"gap_analysis_{role_name.replace(' ', '_').lower()}.json"
        save_gap_analysis(results, output_file)
        
        print(f"\n✅ Gap analysis complete!")
        
        # Ask if user wants course recommendations
        get_courses = input("\n📚 Would you like course recommendations for gaps? (y/n): ").strip().lower()
        
        if get_courses == 'y':
            print("\n🔍 Generating course recommendations...")
            print("(This feature will be implemented in the next module)")
        
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
