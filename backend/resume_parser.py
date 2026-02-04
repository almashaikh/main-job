"""
Resume Parser Module
Extracts text and skills from PDF and DOCX resumes
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional

# PDF parsing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# DOCX parsing
try:
    from docx import Document
except ImportError:
    Document = None

# NLP
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

from skill_database import (
    get_all_skills, 
    get_skill_variations, 
    normalize_skill,
    SKILL_DATABASE
)


class ResumeParser:
    """Parse resumes and extract skills"""
    
    def __init__(self):
        self.all_skills = get_all_skills()
        self.skills_lower = [s.lower() for s in self.all_skills]
        
    
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse resume file (PDF or DOCX)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary with extracted information
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self._extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            text = self._extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Extract information
        result = {
            'raw_text': text,
            'skills': self.extract_skills(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'name': self._extract_name(text),
            'experience_years': self._estimate_experience(text),
            'education': self._extract_education(text)
        }
        
        return result
    
    
    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
        
        return text.strip()
    
    
    def _extract_text_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        if Document is None:
            raise ImportError("python-docx not installed. Run: pip install python-docx")
        
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX: {e}")
    
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using pattern matching
        
        Args:
            text: Resume text
            
        Returns:
            List of found skills
        """
        found_skills = set()
        text_lower = text.lower()
        
        # Method 1: Direct pattern matching
        for skill in self.all_skills:
            # Create pattern that matches whole words
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
            
            # Check variations
            for variation in get_skill_variations(skill):
                pattern = r'\b' + re.escape(variation.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(skill)
        
        # Method 2: NLP-based extraction (if spaCy available)
        if nlp:
            doc = nlp(text)
            
            # Extract noun phrases and check against skills
            for chunk in doc.noun_chunks:
                normalized = normalize_skill(chunk.text)
                if normalized:
                    found_skills.add(normalized)
            
            # Extract named entities (ORG, PRODUCT could be technologies)
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                    normalized = normalize_skill(ent.text)
                    if normalized:
                        found_skills.add(normalized)
        
        return sorted(list(found_skills))
    
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Indian phone pattern
        phone_patterns = [
            r'\b\+91[\s-]?\d{10}\b',  # +91-9876543210
            r'\b\d{10}\b',             # 9876543210
            r'\b\d{5}[\s-]\d{5}\b',    # 98765-43210
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from text (first few non-empty lines)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if lines:
            # Usually name is in first 1-2 lines
            first_line = lines[0]
            
            # Remove common resume headers
            headers = ['resume', 'curriculum vitae', 'cv']
            if first_line.lower() not in headers:
                # Check if it looks like a name (2-4 words, each capitalized)
                words = first_line.split()
                if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    return first_line
        
        return None
    
    
    def _estimate_experience(self, text: str) -> Optional[float]:
        """Estimate years of experience from text"""
        text_lower = text.lower()
        
        # Pattern: "X years of experience"
        patterns = [
            r'(\d+)[\s-]*(?:\+)?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)[\s-]*(?:\+)?\s*years?',
            r'(\d+)[\s-]*(?:\+)?\s*yrs?\s+(?:of\s+)?experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return float(match.group(1))
        
        # Count date ranges (e.g., "2018 - 2021")
        date_pattern = r'(20\d{2})\s*[-–—]\s*(20\d{2}|present|current)'
        dates = re.findall(date_pattern, text_lower)
        
        if dates:
            # Get current year dynamically
            from datetime import datetime
            current_year = datetime.now().year
            
            # Find the earliest start and latest end to avoid counting overlaps
            start_years = []
            end_years = []
            
            for start, end in dates:
                start_years.append(int(start))
                end_years.append(current_year if end in ['present', 'current'] else int(end))
            
            # Calculate experience from earliest start to latest end
            if start_years and end_years:
                earliest_start = min(start_years)
                latest_end = max(end_years)
                total_years = latest_end - earliest_start
                
                return float(total_years)
        
        return None
    
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education degrees"""
        degrees = []
        text_lower = text.lower()
        
        degree_keywords = [
            'b.tech', 'btech', 'bachelor of technology',
            'm.tech', 'mtech', 'master of technology',
            'bsc', 'b.sc', 'bachelor of science',
            'msc', 'm.sc', 'master of science',
            'mba', 'master of business administration',
            'phd', 'ph.d', 'doctorate',
            'be', 'b.e', 'bachelor of engineering',
            'me', 'm.e', 'master of engineering',
            'bca', 'bachelor of computer application',
            'mca', 'master of computer application'
        ]
        
        for degree in degree_keywords:
            if degree in text_lower:
                degrees.append(degree.upper())
        
        return list(set(degrees))
    
    
    def get_skill_categories(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize found skills"""
        categorized = {}
        
        for category, category_skills in SKILL_DATABASE.items():
            found = [s for s in skills if s in category_skills]
            if found:
                categorized[category] = found
        
        return categorized


# ============================================
# HELPER FUNCTIONS
# ============================================

def parse_resume(file_path: str) -> Dict:
    """
    Simple function to parse resume
    
    Args:
        file_path: Path to resume file
        
    Returns:
        Parsed resume data
    """
    parser = ResumeParser()
    return parser.parse_file(file_path)


def display_resume_info(resume_data: Dict):
    """Display parsed resume information"""
    print("\n" + "="*60)
    print("📄 RESUME ANALYSIS")
    print("="*60)
    
    if resume_data.get('name'):
        print(f"\n👤 Name: {resume_data['name']}")
    
    if resume_data.get('email'):
        print(f"📧 Email: {resume_data['email']}")
    
    if resume_data.get('phone'):
        print(f"📱 Phone: {resume_data['phone']}")
    
    if resume_data.get('experience_years'):
        print(f"💼 Experience: ~{resume_data['experience_years']} years")
    
    if resume_data.get('education'):
        print(f"\n🎓 Education: {', '.join(resume_data['education'])}")
    
    skills = resume_data.get('skills', [])
    print(f"\n🔧 Skills Found: {len(skills)}")
    
    if skills:
        # Categorize skills
        parser = ResumeParser()
        categorized = parser.get_skill_categories(skills)
        
        for category, cat_skills in categorized.items():
            print(f"\n  📁 {category.replace('_', ' ').title()}:")
            for skill in cat_skills:
                print(f"     • {skill}")
    
    print("\n" + "="*60)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "🎯"*30)
    print("RESUME PARSER")
    print("🎯"*30)
    
    if len(sys.argv) > 1:
        # File path provided as argument
        file_path = sys.argv[1]
    else:
        # Ask user
        file_path = input("\nEnter path to resume (PDF/DOCX): ").strip()
    
    try:
        print(f"\n📂 Parsing: {file_path}")
        result = parse_resume(file_path)
        display_resume_info(result)
        
        print(f"\n✅ Resume parsed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have installed:")
        print("  pip install PyPDF2 python-docx spacy")
        print("  python -m spacy download en_core_web_sm")
