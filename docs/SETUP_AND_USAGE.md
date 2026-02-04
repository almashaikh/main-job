# Skill Gap Analyzer - Setup and Usage Guide

## 🚀 Quick Start

### Step 1: Install Dependencies

```powershell
# Navigate to backend folder
cd c:\dell\Desktop\skillgap\backend

# Install required packages
pip install requests pandas PyPDF2 python-docx spacy

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 2: Verify Installation

```powershell
# Run integration tests
python test_integration.py
```

This will test all modules and their connections. If all tests pass, you're ready to go!

---

## 📋 Complete Workflow

### Method 1: Using Main App (Recommended)

```powershell
python main_app.py
```

Follow the interactive menu:

1. **📥 Collect Job Market Data**
   - Choose quick test (50 jobs) or custom collection
   - Jobs are saved as `jobs_TIMESTAMP.json`

2. **📊 Analyze Market Skill Demand**
   - Select the jobs file you collected
   - Analyzes skill demand from job postings
   - Saves analysis as `skill_analysis.json`

3. **📄 Parse Your Resume**
   - Provide path to your resume (PDF or DOCX)
   - Extracts skills from your resume

4. **🎯 Perform Gap Analysis**
   - Compares your skills with market demand
   - Shows what skills you need to learn
   - Saves results as `gap_analysis_ROLENAME.json`

5. **📑 View Full Report**
   - See comprehensive analysis
   - Export report to text file

---

### Method 2: Individual Module Testing

#### Test 1: Collect Jobs

```powershell
python multi_source_collector.py
```

Options:
- Quick test: 100 jobs
- Medium: 500 jobs
- Large: 1000+ jobs
- Custom: Choose your own parameters

#### Test 2: Analyze Skills

```powershell
python skill_extractor_updated.py
```

- Select a jobs JSON file
- Analyzes skill demand
- Saves results to `skill_analysis.json`

#### Test 3: Parse Resume

```powershell
python resume_parser.py
```

- Provide resume path
- Extracts skills and info
- Displays results

#### Test 4: Gap Analysis

```powershell
python gap_analyzer.py
```

- Provide resume file
- Select skill analysis file
- See your skill gaps

---

## 🧪 Testing the System

### Quick Integration Test

```powershell
# Run comprehensive tests
python test_integration.py
```

This will:
1. ✅ Test module imports
2. ✅ Collect sample jobs (50 jobs)
3. ✅ Analyze skills from jobs
4. ✅ Test resume parsing
5. ✅ Perform gap analysis
6. ✅ Verify main app integration

### Manual Testing Steps

1. **Test Job Collection:**
   ```powershell
   python -c "from multi_source_collector import JobCollector; c = JobCollector(); jobs = c.collect_from_adzuna('Python Developer', 1); print(f'Collected {len(jobs)} jobs')"
   ```

2. **Test Skill Extraction:**
   ```powershell
   python -c "from skill_database import get_all_skills; print(f'Database has {len(get_all_skills())} skills')"
   ```

3. **Test Resume Parser:**
   ```powershell
   python -c "from resume_parser import ResumeParser; p = ResumeParser(); print('Parser initialized with', len(p.all_skills), 'skills')"
   ```

---

## 📂 File Structure

```
backend/
├── main_app.py                   # 🚀 Main application (START HERE)
├── multi_source_collector.py     # Collects jobs from Adzuna API
├── skill_extractor_updated.py    # Analyzes skill demand
├── resume_parser.py              # Parses PDF/DOCX resumes
├── gap_analyzer.py               # Compares skills
├── skill_database.py             # 200+ technical skills
├── test_integration.py           # Integration tests
├── requirements.txt              # Dependencies
├── SETUP_AND_USAGE.md           # This file
└── Generated files:
    ├── jobs_*.json              # Collected job data
    ├── skill_analysis*.json     # Skill demand analysis
    ├── gap_analysis*.json       # Gap analysis results
    └── skill_gap_report*.txt    # Exported reports
```

---

## 🔍 Verifying Output

### 1. Check Job Collection

```powershell
# View collected jobs
python -c "import json; data = json.load(open('jobs_TIMESTAMP.json')); print(f'Total jobs: {len(data)}'); print('Sample:', data[0]['title'])"
```

Expected output:
- Total jobs count
- Sample job title
- Job has required fields: title, company, description, source

### 2. Check Skill Analysis

```powershell
# View skill analysis
python -c "import json; data = json.load(open('skill_analysis.json')); print(f'Total jobs: {data['total_jobs']}'); print(f'Unique skills: {data['unique_skills']}'); print('Top 5 skills:'); [print(f\"{s['skill']}: {s['percentage']:.1f}%\") for s in data['skills'][:5]]"
```

Expected output:
- Total jobs analyzed
- Number of unique skills
- Top skills with percentages

### 3. Check Gap Analysis

```powershell
# View gap analysis
python -c "import json; data = json.load(open('gap_analysis_ROLE.json')); print(f'Match: {data['match_percentage']:.1f}%'); print(f'Readiness: {data['readiness_score']['score']}/100'); print(f'Critical gaps: {len(data['skill_gaps']['critical'])}')"
```

Expected output:
- Match percentage (your skills vs market)
- Readiness score (0-100)
- Number of critical skill gaps

---

## ✅ Success Criteria

Your system is working if:

1. ✅ Job collection returns 50+ jobs with valid data
2. ✅ Skill analysis finds 20+ unique skills
3. ✅ Resume parser extracts 10+ skills from your resume
4. ✅ Gap analysis shows match percentage and recommendations
5. ✅ All JSON files are created and readable
6. ✅ No import errors or crashes

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```powershell
# Reinstall packages
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Issue: "No jobs collected"
- Check internet connection
- Verify Adzuna API credentials in `multi_source_collector.py`
- Try with different role name

### Issue: "Resume parsing failed"
```powershell
# Make sure PDF/DOCX libraries are installed
pip install PyPDF2 python-docx
```

### Issue: "Import error for skill_extractor"
- File is named `skill_extractor_updated.py` (not `skill_extractor.py`)
- Make sure you're in the backend directory

---

## 📊 Sample Output Examples

### Job Collection Output:
```
📥 ADZUNA: Collecting jobs for 'Python Developer'
  Page 1/1... ✅ 50 jobs (Total: 50)
✅ Adzuna: Collected 50 jobs

✅ Successfully collected 50 jobs!
💾 Saved to: jobs_20260118_143022.json
```

### Skill Analysis Output:
```
📊 ANALYZING 50 JOB POSTINGS

Total Jobs Analyzed: 50
Unique Skills Found: 47

TOP 20 IN-DEMAND SKILLS
Rank   Skill                          Jobs       %          Level
----------------------------------------------------------------
1      Python                         45         90.0       Critical
2      SQL                           38         76.0       Critical
3      AWS                           32         64.0       High
4      Docker                        28         56.0       High
5      REST API                      25         50.0       High
```

### Gap Analysis Output:
```
🎯 SKILL GAP ANALYSIS

Target Role: Python Developer
Match Percentage: 65.2%
Readiness Score: 58/100
Readiness Level: Fair

✅ MATCHED SKILLS (15)
  ✅ Python (Demand: 90.0%)
  ✅ SQL (Demand: 76.0%)
  ✅ Git (Demand: 65.0%)

🔴 CRITICAL GAPS (5)
  ⚠️  AWS (Demand: 64.0%)
  ⚠️  Docker (Demand: 56.0%)
  ⚠️  Kubernetes (Demand: 45.0%)

💡 RECOMMENDATIONS:
  1. 📚 Focus on critical missing skills first
  2. ⏱️  Estimated learning time: 1-2 months
  3. 🔴 PRIORITY: Learn AWS, Docker, Kubernetes
```

---

## 🎯 Next Steps After Verification

1. **Collect More Jobs** - Run with more pages for better accuracy
2. **Try Different Roles** - Analyze multiple job roles
3. **Update Your Resume** - Based on gap analysis results
4. **Track Progress** - Re-run analysis after learning new skills
5. **Export Reports** - Share analysis with mentors/advisors

---

## 📞 Support

If you encounter issues:
1. Run `python test_integration.py` to identify the problem
2. Check the error messages carefully
3. Verify all dependencies are installed
4. Make sure all files are in the backend folder

---

## 🎉 Success!

Once all tests pass and you can run the complete workflow, you have:
- ✅ A working job market analyzer
- ✅ Automated skill gap identification
- ✅ Personalized learning recommendations
- ✅ Career development insights

**Start with:** `python main_app.py`
