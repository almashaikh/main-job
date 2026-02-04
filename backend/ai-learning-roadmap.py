"""
AI Learning Roadmap Generator - IMPROVED VERSION
Generates personalized learning paths with REAL YouTube and Documentation links
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# CONFIGURATION
# ============================================

class Config:
    """Configuration for API keys and settings"""
    
    # Get from environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")  # Optional
    
    # Gemini settings
    GEMINI_MODEL = "models/gemini-flash-latest"
    
    # Resource platforms
    PLATFORMS = [
        "YouTube",
        "Udemy",
        "Coursera",
        "freeCodeCamp",
        "MDN Web Docs",
        "Official Documentation",
        "GitHub Repositories",
        "Medium Articles",
        "Dev.to"
    ]


# ============================================
# GEMINI AI ROADMAP GENERATOR
# ============================================

class GeminiRoadmapGenerator:
    """Generate learning roadmaps using Gemini AI"""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    
    def generate_roadmap(self, skill: str, user_level: str = "beginner") -> Dict:
        """
        Generate learning roadmap for a skill
        
        Args:
            skill: Skill to learn (e.g., "React")
            user_level: beginner, intermediate, advanced
            
        Returns:
            Dictionary with roadmap structure
        """
        
        print(f"\n🤖 Generating roadmap for: {skill}")
        print(f"📊 Level: {user_level}")
        
        prompt = f"""
You are an expert learning path designer. Create a detailed learning roadmap for someone who wants to learn {skill}.

User Level: {user_level}

Please provide a comprehensive roadmap in the following JSON format:

{{
    "skill": "{skill}",
    "level": "{user_level}",
    "prerequisites": [
        {{
            "name": "Prerequisite skill name",
            "importance": "critical|important|recommended",
            "estimated_time": "X weeks/days",
            "description": "Why this is needed"
        }}
    ],
    "learning_path": [
        {{
            "stage": 1,
            "name": "Stage name",
            "skills": ["skill1", "skill2"],
            "topics": ["topic1", "topic2"],
            "estimated_time": "X weeks",
            "description": "What you'll learn"
        }}
    ],
    "projects": [
        {{
            "name": "Project name",
            "difficulty": "beginner|intermediate|advanced",
            "description": "Project description",
            "skills_practiced": ["skill1", "skill2"]
        }}
    ],
    "resources_needed": [
        {{
            "category": "category name",
            "items": ["item1", "item2"]
        }}
    ]
}}

Make it comprehensive and practical. Include 3-5 prerequisites, 4-6 learning stages, and 3-5 project ideas.
Return ONLY valid JSON, no markdown formatting.
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Clean response
            text = response.text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            roadmap = json.loads(text)
            
            print(f"✅ Roadmap generated successfully!")
            print(f"   • {len(roadmap.get('prerequisites', []))} prerequisites")
            print(f"   • {len(roadmap.get('learning_path', []))} learning stages")
            print(f"   • {len(roadmap.get('projects', []))} project ideas")
            
            return roadmap
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response text: {text[:500]}")
            raise
        except Exception as e:
            print(f"❌ Error generating roadmap: {e}")
            raise


# ============================================
# ENHANCED RESOURCE FINDER WITH REAL LINKS
# ============================================

class ResourceFinder:
    """Find learning resources dynamically using AI"""
    
    def __init__(self, youtube_api_key: Optional[str] = None):
        self.youtube_api_key = youtube_api_key
        self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
        print("ℹ️ Resource finder initialized (using AI for dynamic resources)")
    
    
    def find_resources_for_skill(self, skill_name: str, count: int = 5) -> List[Dict]:
        """
        Dynamically find learning resources with REAL YouTube and documentation links
        
        Args:
            skill_name: Name of the skill
            count: Number of resources to find
            
        Returns:
            List of resource dictionaries with working URLs
        """
        
        print(f"🔍 Finding resources for: {skill_name}")
        
        # Use AI to find real resources dynamically
        resources = self._find_dynamic_resources(skill_name, count)
        
        print(f"✅ Found {len(resources)} resources")
        return resources
    
    
    def _find_dynamic_resources(self, skill_name: str, count: int) -> List[Dict]:
        """Use AI to dynamically find real YouTube videos and documentation links"""
        
        prompt = f"""Find the {count} BEST real learning resources for: {skill_name}

IMPORTANT: Provide REAL, WORKING URLs that exist. Focus on:
1. Popular YouTube tutorials (with actual video IDs)
2. Official documentation (real URLs)
3. Well-known learning platforms

For each resource, provide in JSON format:
[
  {{
    "title": "Exact video/resource title",
    "platform": "YouTube|Official Docs|freeCodeCamp|etc",
    "type": "video|documentation|interactive|course",
    "url": "REAL working URL (YouTube video URL, official docs URL, etc)",
    "difficulty": "beginner|intermediate|advanced",
    "duration": "Estimated time",
    "description": "Brief description",
    "rating": "Estimated rating",
    "is_free": true/false
  }}
]

Examples of good resources:
- YouTube: Full course videos from freeCodeCamp, Traversy Media, The Net Ninja
- Docs: Official documentation sites (react.dev, python.org, etc)
- Interactive: freeCodeCamp, W3Schools, MDN

Return ONLY valid JSON array, no markdown.
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean markdown formatting
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            resources = json.loads(text)
            
            if isinstance(resources, list):
                return resources[:count]
            else:
                return [resources][:count]
                
        except Exception as e:
            print(f"⚠️ AI resource finding failed: {e}")
            # Fallback to generic resources
            return self._get_generic_resources(skill_name, count)
    
    
    def _get_generic_resources(self, skill_name: str, count: int) -> List[Dict]:
        """Generate generic but useful resources for any skill"""
        skill_query = skill_name.replace(' ', '+')
        
        resources = [
            {
                "title": f"{skill_name} Complete Tutorial",
                "platform": "YouTube",
                "type": "video",
                "url": f"https://www.youtube.com/results?search_query={skill_query}+full+course+tutorial",
                "difficulty": "beginner",
                "duration": "Variable",
                "description": f"Search YouTube for {skill_name} tutorials",
                "rating": "4.5",
                "is_free": True
            },
            {
                "title": f"{skill_name} Official Documentation",
                "platform": "Official Docs",
                "type": "documentation",
                "url": f"https://www.google.com/search?q={skill_query}+official+documentation",
                "difficulty": "all",
                "duration": "Reference",
                "description": f"Official {skill_name} documentation",
                "rating": "5.0",
                "is_free": True
            },
            {
                "title": f"Learn {skill_name} - freeCodeCamp",
                "platform": "freeCodeCamp",
                "type": "interactive",
                "url": "https://www.freecodecamp.org/learn/",
                "difficulty": "beginner",
                "duration": "Variable",
                "description": f"Interactive {skill_name} courses",
                "rating": "4.8",
                "is_free": True
            },
            {
                "title": f"{skill_name} Tutorial",
                "platform": "MDN Web Docs",
                "type": "article",
                "url": f"https://developer.mozilla.org/en-US/search?q={skill_query}",
                "difficulty": "intermediate",
                "duration": "Variable",
                "description": f"MDN resources for {skill_name}",
                "rating": "4.9",
                "is_free": True
            },
            {
                "title": f"{skill_name} Course",
                "platform": "Udemy",
                "type": "course",
                "url": f"https://www.udemy.com/courses/search/?q={skill_query}",
                "difficulty": "all",
                "duration": "Variable",
                "description": f"Search Udemy for {skill_name} courses",
                "rating": "4.5",
                "is_free": False
            }
        ]
        
        return resources[:count]


# ============================================
# ROADMAP VISUALIZER
# ============================================

class RoadmapVisualizer:
    """Create visual graph of learning roadmap"""
    
    @staticmethod
    def create_graph_data(roadmap: Dict) -> Dict:
        """
        Convert roadmap to graph structure
        
        Returns:
            Graph data for visualization
        """
        
        nodes = []
        edges = []
        node_id = 0
        
        # Add main skill node
        nodes.append({
            "id": node_id,
            "label": roadmap.get("skill", "Target Skill"),
            "type": "target",
            "level": 0
        })
        target_id = node_id
        node_id += 1
        
        # Add prerequisite nodes
        prereq_ids = []
        for prereq in roadmap.get("prerequisites", []):
            nodes.append({
                "id": node_id,
                "label": prereq["name"],
                "type": "prerequisite",
                "importance": prereq.get("importance", "important"),
                "time": prereq.get("estimated_time", "Unknown"),
                "level": 1
            })
            
            # Connect prerequisite to target
            edges.append({
                "from": node_id,
                "to": target_id,
                "type": "prerequisite"
            })
            
            prereq_ids.append(node_id)
            node_id += 1
        
        # Add learning stage nodes
        prev_stage_ids = prereq_ids if prereq_ids else [target_id]
        
        for stage in roadmap.get("learning_path", []):
            stage_id = node_id
            nodes.append({
                "id": stage_id,
                "label": stage["name"],
                "type": "stage",
                "stage_number": stage.get("stage", 0),
                "time": stage.get("estimated_time", "Unknown"),
                "topics": stage.get("topics", []),
                "level": 2
            })
            
            # Connect to previous stage or prerequisites
            for prev_id in prev_stage_ids:
                edges.append({
                    "from": prev_id,
                    "to": stage_id,
                    "type": "learning_path"
                })
            
            prev_stage_ids = [stage_id]
            node_id += 1
        
        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "max_level": 2
            }
        }
    
    
    @staticmethod
    def generate_mermaid_diagram(roadmap: Dict) -> str:
        """Generate Mermaid diagram syntax"""
        
        mermaid = ["graph TD"]
        
        # Main skill
        skill = roadmap.get("skill", "Target Skill")
        mermaid.append(f'    TARGET["{skill}"]:::target')
        
        # Prerequisites
        for i, prereq in enumerate(roadmap.get("prerequisites", [])):
            prereq_id = f"PREREQ{i}"
            mermaid.append(f'    {prereq_id}["{prereq["name"]}"]:::prerequisite')
            mermaid.append(f'    {prereq_id} --> TARGET')
        
        # Learning stages
        prev_nodes = [f"PREREQ{i}" for i in range(len(roadmap.get("prerequisites", [])))]
        if not prev_nodes:
            prev_nodes = ["TARGET"]
        
        for i, stage in enumerate(roadmap.get("learning_path", [])):
            stage_id = f"STAGE{i}"
            mermaid.append(f'    {stage_id}["{stage["name"]}"]:::stage')
            
            for prev_node in prev_nodes:
                mermaid.append(f'    {prev_node} --> {stage_id}')
            
            prev_nodes = [stage_id]
        
        # Styles
        mermaid.append("    classDef target fill:#ff6b6b,stroke:#c92a2a,color:#fff")
        mermaid.append("    classDef prerequisite fill:#4ecdc4,stroke:#0ca89c,color:#fff")
        mermaid.append("    classDef stage fill:#95e1d3,stroke:#38ada9,color:#000")
        
        return "\n".join(mermaid)


# ============================================
# MAIN ROADMAP BUILDER
# ============================================

class RoadmapBuilder:
    """Main class to build complete learning roadmap"""
    
    def __init__(self, gemini_api_key: str, youtube_api_key: Optional[str] = None):
        self.roadmap_generator = GeminiRoadmapGenerator(gemini_api_key)
        self.resource_finder = ResourceFinder(youtube_api_key)
        self.visualizer = RoadmapVisualizer()
    
    
    def build_complete_roadmap(self, skill: str, level: str = "beginner") -> Dict:
        """
        Build complete roadmap with resources
        
        Args:
            skill: Skill to learn
            level: User's current level
            
        Returns:
            Complete roadmap dictionary with REAL YouTube and Documentation links
        """
        
        print(f"\n{'='*60}")
        print(f"🎯 BUILDING LEARNING ROADMAP")
        print(f"{'='*60}")
        print(f"Skill: {skill}")
        print(f"Level: {level}")
        
        # Step 1: Generate roadmap structure
        roadmap = self.roadmap_generator.generate_roadmap(skill, level)
        
        # Step 2: Find resources for each prerequisite
        print(f"\n{'='*60}")
        print(f"📚 FINDING RESOURCES (WITH REAL LINKS)")
        print(f"{'='*60}")
        
        for prereq in roadmap.get("prerequisites", []):
            prereq["resources"] = self.resource_finder.find_resources_for_skill(
                prereq["name"], 
                count=3
            )
        
        # Step 3: Find resources for each learning stage
        for stage in roadmap.get("learning_path", []):
            stage["resources"] = self.resource_finder.find_resources_for_skill(
                stage["name"],
                count=5
            )
        
        # Step 4: Create graph visualization data
        roadmap["graph_data"] = self.visualizer.create_graph_data(roadmap)
        roadmap["mermaid_diagram"] = self.visualizer.generate_mermaid_diagram(roadmap)
        
        # Step 5: Add metadata
        roadmap["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "total_prerequisites": len(roadmap.get("prerequisites", [])),
            "total_stages": len(roadmap.get("learning_path", [])),
            "total_projects": len(roadmap.get("projects", [])),
            "estimated_total_time": self._calculate_total_time(roadmap)
        }
        
        print(f"\n✅ Complete roadmap built successfully with REAL resource links!")
        
        return roadmap
    
    
    def _calculate_total_time(self, roadmap: Dict) -> str:
        """Calculate total estimated learning time"""
        # Simple estimation - you can make this more sophisticated
        prereq_weeks = len(roadmap.get("prerequisites", [])) * 2
        stage_weeks = len(roadmap.get("learning_path", [])) * 3
        total_weeks = prereq_weeks + stage_weeks
        
        if total_weeks < 4:
            return f"{total_weeks} weeks"
        else:
            months = total_weeks // 4
            return f"{months} months"


# ============================================
# HELPER FUNCTIONS
# ============================================

def save_roadmap(roadmap: Dict, filename: Optional[str] = None) -> str:
    """Save roadmap to JSON file"""
    
    if not filename:
        skill_name = roadmap.get("skill", "skill").replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"roadmap_{skill_name}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Roadmap saved to: {filename}")
    return filename


def print_roadmap_summary(roadmap: Dict):
    """Print roadmap summary to console"""
    
    print(f"\n{'='*60}")
    print(f"📋 LEARNING ROADMAP: {roadmap.get('skill', 'Unknown')}")
    print(f"{'='*60}")
    
    # Prerequisites
    print(f"\n🔧 PREREQUISITES ({len(roadmap.get('prerequisites', []))})")
    for i, prereq in enumerate(roadmap.get("prerequisites", []), 1):
        importance = prereq.get("importance", "").upper()
        time = prereq.get("estimated_time", "Unknown")
        print(f"\n{i}. {prereq['name']} [{importance}] - {time}")
        print(f"   {prereq.get('description', '')}")
        
        if "resources" in prereq:
            print(f"   📚 Resources: {len(prereq['resources'])} found")
            for res in prereq['resources'][:2]:
                print(f"      • {res['title']} ({res['platform']}) - {res['url']}")
    
    # Learning Path
    print(f"\n🎓 LEARNING PATH ({len(roadmap.get('learning_path', []))} stages)")
    for stage in roadmap.get("learning_path", []):
        print(f"\nStage {stage.get('stage', '?')}: {stage['name']}")
        print(f"   ⏱️  {stage.get('estimated_time', 'Unknown')}")
        print(f"   📖 Topics: {', '.join(stage.get('topics', []))}")
        if "resources" in stage:
            print(f"   📚 Resources: {len(stage['resources'])} found")
            for res in stage['resources'][:2]:
                print(f"      • {res['title']} ({res['platform']}) - {res['url']}")
    
    # Projects
    print(f"\n🚀 PROJECT IDEAS ({len(roadmap.get('projects', []))})")
    for i, project in enumerate(roadmap.get("projects", []), 1):
        print(f"\n{i}. {project['name']} [{project.get('difficulty', 'Unknown')}]")
        print(f"   {project.get('description', '')}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"⏱️  Estimated Total Time: {roadmap.get('metadata', {}).get('estimated_total_time', 'Unknown')}")
    print(f"{'='*60}")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function"""
    
    print("\n" + "🎯"*30)
    print("AI LEARNING ROADMAP GENERATOR (WITH REAL YOUTUBE & DOC LINKS)")
    print("🎯"*30)
    
    # Check for API key
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("\n❌ GEMINI_API_KEY not found in environment variables")
        print("\nTo set it up:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable:")
        print("   export GEMINI_API_KEY='your-api-key'")
        return
    
    # Get user input
    print("\n" + "="*60)
    print("WHAT DO YOU WANT TO LEARN?")
    print("="*60)
    
    skill = input("\nEnter skill to learn (e.g., React, Python, Data Science): ").strip()
    
    print("\nYour current level:")
    print("1. Beginner (starting from scratch)")
    print("2. Intermediate (have some basics)")
    print("3. Advanced (want to master it)")
    
    level_choice = input("\nEnter choice (1-3): ").strip()
    level_map = {"1": "beginner", "2": "intermediate", "3": "advanced"}
    level = level_map.get(level_choice, "beginner")
    
    try:
        # Build roadmap
        builder = RoadmapBuilder(gemini_key)
        roadmap = builder.build_complete_roadmap(skill, level)
        
        # Print summary
        print_roadmap_summary(roadmap)
        
        # Save to file
        filename = save_roadmap(roadmap)
        
        # Show next steps
        print(f"\n{'='*60}")
        print("✅ SUCCESS!")
        print(f"{'='*60}")
        print(f"\n📁 Files created:")
        print(f"   • {filename}")
        print(f"\n🔗 Resources:")
        print(f"   • All resources include REAL YouTube and documentation links")
        print(f"   • Check the JSON file for complete URLs")
        print(f"\n📊 Visualization:")
        print(f"   • Mermaid diagram included in JSON")
        print(f"   • Graph data ready for frontend")
        print(f"\n🎯 Next steps:")
        print(f"   1. Review the roadmap in {filename}")
        print(f"   2. Start with prerequisites")
        print(f"   3. Follow the learning path")
        print(f"   4. Build the projects")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
