"""
Comprehensive Skill Database
Contains 200+ technical skills organized by category
"""

# ============================================
# COMPREHENSIVE SKILL DATABASE
# ============================================

SKILL_DATABASE = {
    
    # PROGRAMMING LANGUAGES
    "programming_languages": [
        "Python", "Java", "JavaScript", "C++", "C#", "C", "Go", "Golang",
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
        "TypeScript", "Rust", "Perl", "Shell", "Bash", "PowerShell",
        "Objective-C", "Dart", "Elixir", "Haskell", "Julia", "VBA"
    ],
    
    # WEB DEVELOPMENT
    "web_frontend": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Next.js", "Svelte",
        "jQuery", "Bootstrap", "Tailwind CSS", "Material UI", "Redux",
        "Webpack", "Vite", "SASS", "LESS", "Responsive Design",
        "Progressive Web Apps", "PWA", "Single Page Application", "SPA"
    ],
    
    "web_backend": [
        "Node.js", "Express.js", "Django", "Flask", "FastAPI", "Spring Boot",
        "ASP.NET", "Ruby on Rails", "Laravel", "Symfony", "RESTful API",
        "GraphQL", "gRPC", "WebSocket", "Microservices", "API Development"
    ],
    
    # DATABASES
    "databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
        "Oracle", "Microsoft SQL Server", "SQLite", "DynamoDB", "Elasticsearch",
        "Neo4j", "CouchDB", "MariaDB", "Firebase", "Firestore",
        "Database Design", "Query Optimization", "Data Modeling"
    ],
    
    # DATA SCIENCE & ML
    "data_science": [
        "Machine Learning", "Deep Learning", "Neural Networks", "NLP",
        "Natural Language Processing", "Computer Vision", "TensorFlow",
        "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "SciPy",
        "Data Analysis", "Data Visualization", "Statistical Analysis",
        "A/B Testing", "Hypothesis Testing", "Time Series Analysis",
        "Predictive Modeling", "Feature Engineering"
    ],
    
    "ml_frameworks": [
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "XGBoost",
        "LightGBM", "CatBoost", "Hugging Face", "OpenCV", "NLTK", "spaCy",
        "Transformers", "BERT", "GPT", "LLM", "Large Language Models",
        "MLflow", "Weights & Biases", "WandB"
    ],
    
    # CLOUD & DEVOPS
    "cloud_platforms": [
        "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP",
        "AWS Lambda", "EC2", "S3", "CloudFormation", "Azure DevOps",
        "Google Cloud Platform", "Heroku", "DigitalOcean", "Netlify", "Vercel"
    ],
    
    "devops": [
        "Docker", "Kubernetes", "Jenkins", "CI/CD", "GitLab CI", "GitHub Actions",
        "Terraform", "Ansible", "Chef", "Puppet", "CircleCI", "Travis CI",
        "Container Orchestration", "Infrastructure as Code", "IaC"
    ],
    
    # VERSION CONTROL & COLLABORATION
    "version_control": [
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Mercurial",
        "Version Control", "Code Review", "Pull Requests", "Branching Strategy"
    ],
    
    # DATA ENGINEERING
    "data_engineering": [
        "Apache Spark", "Hadoop", "Kafka", "Airflow", "ETL", "Data Warehousing",
        "Data Pipeline", "Apache Beam", "Flink", "Hive", "Presto", "Snowflake",
        "Databricks", "Data Lake", "Big Data", "Stream Processing", "Batch Processing"
    ],
    
    # BUSINESS INTELLIGENCE
    "bi_tools": [
        "Tableau", "Power BI", "Looker", "Qlik", "Google Data Studio",
        "Metabase", "Superset", "Business Intelligence", "Data Storytelling",
        "Dashboard Development", "KPI Tracking"
    ],
    
    # MOBILE DEVELOPMENT
    "mobile": [
        "iOS Development", "Android Development", "React Native", "Flutter",
        "Xamarin", "Mobile App Development", "SwiftUI", "Jetpack Compose",
        "Cordova", "Ionic", "Cross-platform Development"
    ],
    
    # TESTING & QA
    "testing": [
        "Unit Testing", "Integration Testing", "Test Automation", "Selenium",
        "Jest", "Pytest", "JUnit", "Mocha", "Cypress", "TestNG",
        "Test-Driven Development", "TDD", "BDD", "Quality Assurance", "QA"
    ],
    
    # SECURITY
    "security": [
        "Cybersecurity", "Information Security", "Network Security",
        "Application Security", "Penetration Testing", "Ethical Hacking",
        "OWASP", "Security Audit", "Vulnerability Assessment", "Encryption",
        "SSL/TLS", "OAuth", "JWT", "Authentication", "Authorization"
    ],
    
    # SYSTEM & NETWORKING
    "systems": [
        "Linux", "Unix", "Windows Server", "System Administration",
        "Network Administration", "TCP/IP", "DNS", "Load Balancing",
        "Nginx", "Apache", "IIS", "VPN", "Firewall"
    ],
    
    # METHODOLOGIES & FRAMEWORKS
    "methodologies": [
        "Agile", "Scrum", "Kanban", "Waterfall", "DevOps", "Lean",
        "Six Sigma", "ITIL", "Project Management", "Product Management",
        "Jira", "Confluence", "Trello", "Asana"
    ],
    
    # DESIGN & UX
    "design": [
        "UI/UX Design", "User Experience", "User Interface Design",
        "Figma", "Adobe XD", "Sketch", "Wireframing", "Prototyping",
        "User Research", "Usability Testing", "Design Thinking",
        "Adobe Photoshop", "Adobe Illustrator", "InVision"
    ],
    
    # BLOCKCHAIN & EMERGING TECH
    "emerging_tech": [
        "Blockchain", "Smart Contracts", "Ethereum", "Solidity", "Web3",
        "Cryptocurrency", "NFT", "DeFi", "IoT", "Internet of Things",
        "AR/VR", "Augmented Reality", "Virtual Reality", "Quantum Computing"
    ],
    
    # SOFT SKILLS (Important for matching)
    "soft_skills": [
        "Communication", "Leadership", "Team Collaboration", "Problem Solving",
        "Critical Thinking", "Time Management", "Analytical Skills",
        "Presentation Skills", "Technical Writing", "Documentation",
        "Stakeholder Management", "Cross-functional Collaboration"
    ],
    
    # OFFICE & PRODUCTIVITY
    "productivity": [
        "Microsoft Office", "Excel", "PowerPoint", "Word", "Google Sheets",
        "Google Workspace", "Slack", "Microsoft Teams", "Zoom",
        "Remote Work", "Virtual Collaboration"
    ],
    
    # ADDITIONAL TECHNICAL SKILLS
    "other_technical": [
        "API Integration", "Web Scraping", "Data Mining", "Regular Expressions",
        "Regex", "JSON", "XML", "YAML", "Markdown", "LaTeX",
        "Debugging", "Code Optimization", "Performance Tuning",
        "Algorithms", "Data Structures", "Object-Oriented Programming", "OOP",
        "Functional Programming", "Design Patterns", "Software Architecture",
        "System Design", "Distributed Systems", "Concurrency", "Multithreading"
    ]
}


# ============================================
# SKILL VARIATIONS & SYNONYMS
# ============================================

SKILL_VARIATIONS = {
    # Programming Language Variations
    "JavaScript": ["JS", "Javascript", "ECMAScript", "ES6", "ES2015"],
    "TypeScript": ["TS"],
    "Python": ["Python3", "Python 3"],
    "C++": ["CPP", "C Plus Plus"],
    "C#": ["C Sharp", "CSharp"],
    "Go": ["Golang"],
    
    # Framework Variations
    "React": ["ReactJS", "React.js"],
    "Vue.js": ["Vue", "VueJS"],
    "Node.js": ["NodeJS", "Node"],
    "Next.js": ["NextJS"],
    "Express.js": ["Express", "ExpressJS"],
    "Spring Boot": ["Spring", "Spring Framework"],
    "ASP.NET": ["ASP.NET Core", "DotNet", ".NET"],
    
    # Database Variations
    "PostgreSQL": ["Postgres", "PSQL"],
    "MongoDB": ["Mongo"],
    "Microsoft SQL Server": ["MS SQL", "MSSQL", "SQL Server"],
    
    # ML/AI Variations
    "Machine Learning": ["ML"],
    "Deep Learning": ["DL"],
    "Natural Language Processing": ["NLP"],
    "Computer Vision": ["CV"],
    "Large Language Models": ["LLM", "LLMs"],
    
    # Cloud Variations
    "Amazon Web Services": ["AWS"],
    "Google Cloud Platform": ["GCP", "Google Cloud"],
    "Azure": ["Microsoft Azure"],
    
    # DevOps Variations
    "CI/CD": ["Continuous Integration", "Continuous Deployment"],
    "Infrastructure as Code": ["IaC"],
    
    # Other Variations
    "UI/UX": ["UI/UX Design", "User Experience Design"],
    "REST": ["RESTful", "REST API"],
    "Object-Oriented Programming": ["OOP"],
    "Test-Driven Development": ["TDD"],
    "Behavior-Driven Development": ["BDD"]
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_all_skills():
    """Get flat list of all skills"""
    all_skills = []
    for category, skills in SKILL_DATABASE.items():
        all_skills.extend(skills)
    return all_skills


def get_skill_variations(skill):
    """Get all variations of a skill name"""
    variations = [skill]
    if skill in SKILL_VARIATIONS:
        variations.extend(SKILL_VARIATIONS[skill])
    return variations


def normalize_skill(skill_text):
    """Normalize skill name to standard form"""
    skill_text = skill_text.strip().lower()
    
    # Check if it's a variation
    for standard_name, variations in SKILL_VARIATIONS.items():
        if skill_text in [v.lower() for v in variations]:
            return standard_name
        if skill_text == standard_name.lower():
            return standard_name
    
    # Check in main database
    all_skills = get_all_skills()
    for skill in all_skills:
        if skill_text == skill.lower():
            return skill
    
    return None


def get_skills_by_category(category):
    """Get skills for a specific category"""
    return SKILL_DATABASE.get(category, [])


# ============================================
# STATISTICS
# ============================================

def get_database_stats():
    """Get statistics about the skill database"""
    total_skills = len(get_all_skills())
    total_categories = len(SKILL_DATABASE)
    total_variations = sum(len(v) for v in SKILL_VARIATIONS.values())
    
    return {
        "total_skills": total_skills,
        "total_categories": total_categories,
        "total_variations": total_variations,
        "categories": list(SKILL_DATABASE.keys())
    }


if __name__ == "__main__":
    # Test the database
    stats = get_database_stats()
    print("="*60)
    print("SKILL DATABASE STATISTICS")
    print("="*60)
    print(f"\nTotal Skills: {stats['total_skills']}")
    print(f"Total Categories: {stats['total_categories']}")
    print(f"Total Variations: {stats['total_variations']}")
    
    print("\n📋 Categories:")
    for i, category in enumerate(stats['categories'], 1):
        skill_count = len(SKILL_DATABASE[category])
        print(f"  {i}. {category}: {skill_count} skills")
    
    print("\n✅ Skill database loaded successfully!")
