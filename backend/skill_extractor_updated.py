"""
Skill Extractor Module
Analyzes job descriptions and calculates skill demand
Compatible with Multi-Source Job Collector (Adzuna, The Muse, Remotive)
"""

import json
import re
from collections import Counter
from typing import Dict, List, Set
from pathlib import Path
from datetime import datetime

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

from skill_database import (
    get_all_skills, 
    get_skill_variations, 
    normalize_skill
)


class SkillExtractor:
    """Extract skills from job descriptions"""
    
    def __init__(self):
        self.all_skills = get_all_skills()
        self.skills_lower = [s.lower() for s in self.all_skills]
    
    
    def extract_from_text(self, text: str) -> List[str]:
        """
        Extract skills from a single text (job description)
        
        Args:
            text: Job description text
            
        Returns:
            List of found skills
        """
        found_skills = set()
        text_lower = text.lower()
        
        # Method 1: Pattern matching with word boundaries
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
            
            # Check variations
            for variation in get_skill_variations(skill):
                pattern = r'\b' + re.escape(variation.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(skill)
        
        # Method 2: NLP-based extraction (if available)
        if nlp and len(text) < 1000000:  # Limit text size for NLP
            try:
                doc = nlp(text[:100000])  # Process first 100k chars
                
                # Extract noun phrases
                for chunk in doc.noun_chunks:
                    normalized = normalize_skill(chunk.text)
                    if normalized:
                        found_skills.add(normalized)
            except:
                pass  # Continue with pattern matching only
        
        return sorted(list(found_skills))
    
    
    def analyze_jobs(self, jobs: List[Dict]) -> Dict:
        """
        Analyze multiple job postings and calculate skill demand
        
        Args:
            jobs: List of job dictionaries (from multi-source collector)
            
        Returns:
            Dictionary with skill statistics
        """
        print(f"\n{'='*60}")
        print(f"📊 ANALYZING {len(jobs)} JOB POSTINGS")
        print(f"{'='*60}\n")
        
        # Track by source
        source_stats = {}
        all_skills_found = []
        jobs_processed = 0
        skills_by_job = {}
        
        for i, job in enumerate(jobs, 1):
            # Get job description and metadata
            description = job.get('description', '')
            title = job.get('title', '')
            source = job.get('source', 'unknown')
            
            # Track source
            if source not in source_stats:
                source_stats[source] = {'total': 0, 'with_skills': 0}
            source_stats[source]['total'] += 1
            
            # Combine title and description for better extraction
            full_text = f"{title}\n{description}"
            
            # Extract skills
            skills = self.extract_from_text(full_text)
            
            if skills:
                all_skills_found.extend(skills)
                jobs_processed += 1
                source_stats[source]['with_skills'] += 1
                skills_by_job[i-1] = {
                    'title': title,
                    'company': job.get('company', ''),
                    'source': source,
                    'skills': skills
                }
            
            # Progress indicator
            if i % 50 == 0:
                print(f"  Processed {i}/{len(jobs)} jobs...")
        
        print(f"\n✅ Processed {jobs_processed} jobs with skills")
        print(f"\n📋 By Source:")
        for source, stats in source_stats.items():
            print(f"  • {source.upper()}: {stats['with_skills']}/{stats['total']} jobs with skills")
        
        # Calculate statistics
        skill_counts = Counter(all_skills_found)
        total_jobs = len(jobs)
        
        # Calculate demand percentages
        skill_demand = []
        for skill, count in skill_counts.items():
            percentage = (count / total_jobs) * 100
            skill_demand.append({
                'skill': skill,
                'count': count,
                'percentage': round(percentage, 2),
                'demand_level': self._categorize_demand(percentage)
            })
        
        # Sort by count (most demanded first)
        skill_demand.sort(key=lambda x: x['count'], reverse=True)
        
        return {
            'total_jobs': total_jobs,
            'jobs_with_skills': jobs_processed,
            'unique_skills': len(skill_counts),
            'total_skill_mentions': sum(skill_counts.values()),
            'source_breakdown': source_stats,
            'skills': skill_demand,
            'top_10_skills': skill_demand[:10],
            'top_20_skills': skill_demand[:20],
            'analyzed_at': datetime.now().isoformat()
        }
    
    
    def _categorize_demand(self, percentage: float) -> str:
        """Categorize demand level based on percentage"""
        if percentage >= 40:
            return "Critical"
        elif percentage >= 20:
            return "High"
        elif percentage >= 10:
            return "Medium"
        else:
            return "Low"
    
    
    def analyze_by_source(self, jobs: List[Dict]) -> Dict[str, Dict]:
        """
        Analyze jobs grouped by source
        
        Args:
            jobs: List of all jobs
            
        Returns:
            Dictionary with analysis for each source
        """
        sources = list(set(j.get('source', 'unknown') for j in jobs))
        results = {}
        
        for source in sources:
            source_jobs = [j for j in jobs if j.get('source', 'unknown') == source]
            if source_jobs:
                print(f"\n{'='*60}")
                print(f"Analyzing {source.upper()} jobs...")
                print(f"{'='*60}")
                results[source] = self.analyze_jobs(source_jobs)
        
        return results
    
    
    def analyze_role_specific(self, jobs: List[Dict], role_name: str) -> Dict:
        """
        Analyze jobs for a specific role
        
        Args:
            jobs: List of all jobs
            role_name: Specific role to filter
            
        Returns:
            Analysis results for that role
        """
        # Filter jobs for this role
        role_jobs = [j for j in jobs if j.get('search_role', '').lower() == role_name.lower()]
        
        if not role_jobs:
            print(f"\n⚠️  No jobs found for role: {role_name}")
            return None
        
        print(f"\n📋 Analyzing {len(role_jobs)} jobs for: {role_name}")
        return self.analyze_jobs(role_jobs)
    
    
    def compare_sources(self, jobs: List[Dict]) -> Dict:
        """
        Compare skill demand across different sources
        
        Args:
            jobs: List of all jobs
            
        Returns:
            Comparison data
        """
        print(f"\n{'='*60}")
        print(f"🔄 COMPARING SOURCES")
        print(f"{'='*60}")
        
        source_analyses = self.analyze_by_source(jobs)
        
        # Find common skills across sources
        all_source_skills = {}
        for source, analysis in source_analyses.items():
            skills = {s['skill']: s['percentage'] for s in analysis['skills'][:20]}
            all_source_skills[source] = skills
        
        return {
            'by_source': source_analyses,
            'comparison': all_source_skills
        }


def load_jobs_from_file(file_path: str) -> List[Dict]:
    """Load jobs from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    # Validate multi-source format
    if jobs and 'source' in jobs[0]:
        sources = list(set(j.get('source', 'unknown') for j in jobs))
        print(f"📂 Loaded multi-source data with: {', '.join(sources)}")
    
    return jobs


def save_analysis_results(results: Dict, output_file: str):
    """Save analysis results to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Analysis saved to: {output_file}")


def display_results(results: Dict):
    """Display analysis results"""
    print("\n" + "="*60)
    print("📊 SKILL DEMAND ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\n📈 Overview:")
    print(f"  • Total Jobs Analyzed: {results['total_jobs']}")
    print(f"  • Jobs with Skills: {results['jobs_with_skills']}")
    print(f"  • Unique Skills Found: {results['unique_skills']}")
    print(f"  • Total Skill Mentions: {results['total_skill_mentions']}")
    
    # Show source breakdown if available
    if 'source_breakdown' in results:
        print(f"\n📋 Source Breakdown:")
        for source, stats in results['source_breakdown'].items():
            print(f"  • {source.upper()}: {stats['with_skills']}/{stats['total']} jobs")
    
    print(f"\n🏆 TOP 20 IN-DEMAND SKILLS:")
    print(f"{'='*60}")
    
    for i, skill_data in enumerate(results['skills'][:20], 1):
        skill = skill_data['skill']
        count = skill_data['count']
        percentage = skill_data['percentage']
        level = skill_data['demand_level']
        
        # Color code by demand level
        emoji = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🔵'
        }.get(level, '⚪')
        
        print(f"{i:2d}. {emoji} {skill:<30} {percentage:>6.1f}% ({count:>3} jobs) - {level}")
    
    print(f"\n{'='*60}")


def create_demand_categories(results: Dict) -> Dict[str, List[str]]:
    """Categorize skills by demand level"""
    categories = {
        'Critical': [],
        'High': [],
        'Medium': [],
        'Low': []
    }
    
    for skill_data in results['skills']:
        level = skill_data['demand_level']
        categories[level].append(skill_data['skill'])
    
    return categories


def display_source_comparison(comparison_data: Dict):
    """Display comparison of skills across sources"""
    print("\n" + "="*60)
    print("🔄 SOURCE COMPARISON")
    print("="*60)
    
    for source, analysis in comparison_data['by_source'].items():
        print(f"\n{source.upper()}:")
        print(f"  Total Jobs: {analysis['total_jobs']}")
        print(f"  Unique Skills: {analysis['unique_skills']}")
        print(f"  Top 5 Skills: {', '.join([s['skill'] for s in analysis['skills'][:5]])}")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    print("\n" + "🎯"*30)
    print("MULTI-SOURCE SKILL DEMAND ANALYZER")
    print("🎯"*30)
    
    # Find JSON files in current directory
    json_files = list(Path('.').glob('multi_source_jobs_*.json'))
    if not json_files:
        json_files = list(Path('.').glob('jobs_*.json'))
    
    if not json_files and len(sys.argv) > 1:
        # File provided as argument
        json_file = sys.argv[1]
    elif json_files:
        # Use most recent JSON file
        json_file = str(max(json_files, key=lambda p: p.stat().st_mtime))
        print(f"\n📂 Found job data file: {json_file}")
    else:
        # Ask user
        json_file = input("\nEnter path to jobs JSON file: ").strip()
    
    try:
        # Load jobs
        print(f"\n📥 Loading jobs from: {json_file}")
        jobs = load_jobs_from_file(json_file)
        print(f"✅ Loaded {len(jobs)} jobs")
        
        # Create extractor
        extractor = SkillExtractor()
        
        # Check data sources
        sources = list(set(j.get('source', 'unknown') for j in jobs))
        roles = list(set(j.get('search_role', 'Unknown') for j in jobs))
        
        print(f"\n📊 Data Overview:")
        print(f"  • Sources: {', '.join(sources)}")
        print(f"  • Roles: {', '.join(roles)}")
        
        # Analysis options
        print(f"\n{'='*60}")
        print("ANALYSIS OPTIONS")
        print(f"{'='*60}")
        print("1. Analyze all jobs together")
        print("2. Analyze by specific role")
        print("3. Analyze by source (compare Adzuna vs Muse vs Remotive)")
        print("4. Full comparison report (all analyses)")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            # All jobs together
            results = extractor.analyze_jobs(jobs)
            output_file = "skill_analysis_all.json"
            display_results(results)
            save_analysis_results(results, output_file)
            
        elif choice == "2":
            # Specific role
            if len(roles) > 1:
                print(f"\n📋 Available roles:")
                for i, role in enumerate(roles, 1):
                    role_count = len([j for j in jobs if j.get('search_role') == role])
                    print(f"  {i}. {role}: {role_count} jobs")
                
                role_num = int(input(f"\nEnter role number (1-{len(roles)}): ")) - 1
                selected_role = roles[role_num]
            else:
                selected_role = roles[0]
            
            results = extractor.analyze_role_specific(jobs, selected_role)
            output_file = f"skill_analysis_{selected_role.replace(' ', '_').lower()}.json"
            
            if results:
                display_results(results)
                save_analysis_results(results, output_file)
                
        elif choice == "3":
            # By source
            comparison = extractor.compare_sources(jobs)
            output_file = "skill_analysis_by_source.json"
            
            display_source_comparison(comparison)
            save_analysis_results(comparison, output_file)
            
        elif choice == "4":
            # Full report
            print(f"\n🔄 Generating full comparison report...")
            
            # Overall analysis
            overall = extractor.analyze_jobs(jobs)
            
            # By source
            by_source = extractor.analyze_by_source(jobs)
            
            # By role (if multiple)
            by_role = {}
            if len(roles) > 1:
                for role in roles:
                    role_analysis = extractor.analyze_role_specific(jobs, role)
                    if role_analysis:
                        by_role[role] = role_analysis
            
            full_report = {
                'overall': overall,
                'by_source': by_source,
                'by_role': by_role,
                'metadata': {
                    'total_jobs': len(jobs),
                    'sources': sources,
                    'roles': roles,
                    'generated_at': datetime.now().isoformat()
                }
            }
            
            output_file = "skill_analysis_full_report.json"
            
            print(f"\n{'='*60}")
            print("📊 OVERALL RESULTS")
            print(f"{'='*60}")
            display_results(overall)
            
            print(f"\n{'='*60}")
            print("🔄 SOURCE COMPARISON")
            print(f"{'='*60}")
            for source, analysis in by_source.items():
                print(f"\n{source.upper()}: Top 5 skills")
                for i, s in enumerate(analysis['skills'][:5], 1):
                    print(f"  {i}. {s['skill']} - {s['percentage']}%")
            
            save_analysis_results(full_report, output_file)
            
        else:
            print("\n❌ Invalid choice")
            sys.exit(1)
        
        # Show categories
        if 'skills' in results if choice != "4" else overall:
            result_to_use = results if choice != "4" else overall
            categories = create_demand_categories(result_to_use)
            print(f"\n📊 Skills by Demand Level:")
            for level, skills in categories.items():
                if skills:
                    print(f"\n  {level}: {len(skills)} skills")
                    if level in ['Critical', 'High']:
                        print(f"    {', '.join(skills[:10])}")
        
        print(f"\n✅ Analysis complete!")
        print(f"\n💡 Tip: Use the JSON output file for further analysis or visualization")
        
    except FileNotFoundError:
        print(f"\n❌ File not found: {json_file}")
        print("\n⚠️  Make sure you have run multi_source_collector.py first!")
        print("   Example: python multi_source_collector.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n")
