"""
Job Collector - Adzuna API
Collects jobs from Adzuna API (India's largest job aggregator)
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class JobCollector:
    """Collect jobs from Adzuna API"""
    
    def __init__(self):
        # Adzuna API Credentials
        self.adzuna_app_id = "28172709"
        self.adzuna_app_key = "66743682dbb92536948653f3da9b05c9"
        
        # API Base URL
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs/in/search"
        
        # Statistics
        self.stats = {
            'adzuna': {'attempted': 0, 'collected': 0, 'failed': 0}
        }
    
    
    # ============================================
    # ADZUNA API
    # ============================================
    
    def collect_from_adzuna(self, role: str, pages: int = 5, location: str = "India", page_offset: int = 0) -> List[Dict]:
        """
        Collect jobs from Adzuna API
        
        Args:
            role: Job role to search
            pages: Number of pages (50 jobs per page)
            location: Location to search in (default: India)
            page_offset: Starting page offset (for pagination)
            
        Returns:
            List of job dictionaries
        """
        
        print(f"\n{'='*60}")
        print(f"📥 ADZUNA: Collecting jobs for '{role}' in {location}")
        print(f"{'='*60}")
        
        jobs = []
        
        # Determine location parameter for Adzuna API
        location_param = None
        if location.lower() != "india":
            location_param = location
        
        for page in range(1 + page_offset, pages + 1 + page_offset):
            self.stats['adzuna']['attempted'] += 1
            
            url = f"{self.adzuna_base_url}/{page}"
            
            params = {
                "app_id": self.adzuna_app_id,
                "app_key": self.adzuna_app_key,
                "what": role,
                "results_per_page": 50,
                "sort_by": "date"
            }
            
            # Add location parameter if specified
            if location_param:
                params["where"] = location_param
            
            try:
                print(f"  Page {page}/{pages + page_offset}...", end=" ")
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    page_jobs = data.get('results', [])
                    
                    if not page_jobs:
                        print("❌ No more jobs")
                        break
                    
                    # Normalize Adzuna data format
                    for job in page_jobs:
                        normalized = {
                            'source': 'adzuna',
                            'id': job.get('id', f"adzuna_{len(jobs)}"),
                            'title': job.get('title', ''),
                            'company': job.get('company', {}).get('display_name', ''),
                            'location': job.get('location', {}).get('display_name', location),
                            'description': job.get('description', ''),
                            'salary_min': job.get('salary_min'),
                            'salary_max': job.get('salary_max'),
                            'created': job.get('created', ''),
                            'redirect_url': job.get('redirect_url', ''),
                            'contract_type': job.get('contract_type', 'Full-time'),
                            'category': job.get('category', {}).get('label', 'Technology'),
                            'search_role': role,
                            'search_location': location,
                            'collected_at': datetime.now().isoformat()
                        }
                        jobs.append(normalized)
                    
                    self.stats['adzuna']['collected'] += len(page_jobs)
                    print(f"✅ {len(page_jobs)} jobs (Total: {len(jobs)})")
                    
                elif response.status_code == 429:
                    print("⚠️  Rate limit reached")
                    self.stats['adzuna']['failed'] += 1
                    break
                else:
                    print(f"❌ Error {response.status_code}")
                    self.stats['adzuna']['failed'] += 1
                
                # Respect rate limits
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.stats['adzuna']['failed'] += 1
                continue
        
        print(f"✅ Adzuna: Collected {len(jobs)} jobs")
        return jobs
    
    
        return jobs
    
    
    # ============================================
    # MULTI-ROLE COLLECTION
    # ============================================
    
    def collect_multiple_roles(self, roles: List[str], pages_per_role: int = 2) -> List[Dict]:
        """Print collection statistics"""
        
        print("\n" + "="*60)
        print("📊 COLLECTION STATISTICS")
        print("="*60)
        
        total_collected = sum(s['collected'] for s in self.stats.values())
        total_attempted = sum(s['attempted'] for s in self.stats.values())
        total_failed = sum(s['failed'] for s in self.stats.values())
        
        print(f"\nTotal Jobs Collected: {total_collected}")
        print(f"Total Requests: {total_attempted}")
        print(f"Failed Requests: {total_failed}")
        
        print("\n📋 By Source:")
        for source, stats in self.stats.items():
            print(f"\n  {source.upper()}:")
            print(f"    Collected: {stats['collected']}")
            print(f"    Requests: {stats['attempted']}")
            print(f"    Failed: {stats['failed']}")
            
            if stats['attempted'] > 0:
                success_rate = (stats['collected'] / (stats['attempted'] * 50)) * 100
                print(f"    Success Rate: {success_rate:.1f}%")
    
    
    def print_stats(self):
        """Alias for print_statistics for compatibility"""
        self.print_statistics()
    
    
    def collect_multiple_roles(self, roles: List[str], pages_per_role: int = 2) -> List[Dict]:
        """
        Collect jobs for multiple roles from Adzuna
        
        Args:
            roles: List of job roles
            pages_per_role: Number of pages per role
            
        Returns:
            Combined list of jobs
        """
        print("\n" + "🚀"*30)
        print("MULTI-ROLE JOB COLLECTION")
        print("🚀"*30)
        print(f"\nRoles: {', '.join(roles)}")
        print(f"Pages per role: {pages_per_role}")
        print(f"Expected jobs: ~{len(roles) * pages_per_role * 50}")
        
        all_jobs = []
        
        for role in roles:
            try:
                jobs = self.collect_from_adzuna(role, pages=pages_per_role)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"\n⚠️  Failed to collect for '{role}': {e}")
                continue
        
        return all_jobs


# ============================================
# HELPER FUNCTIONS
# ============================================

def save_jobs(jobs: List[Dict], prefix: str = "multi_source_jobs") -> str:
    """Save jobs to JSON and CSV files"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_filename = f"{prefix}_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved JSON: {json_filename}")
    
    # Try to save as CSV (if pandas available)
    try:
        import pandas as pd
        
        # Extract key fields
        data = []
        for job in jobs:
            data.append({
                'source': job.get('source', ''),
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'description': job.get('description', '')[:500],  # First 500 chars
                'url': job.get('url', ''),
                'search_role': job.get('search_role', ''),
                'created': job.get('created', '')
            })
        
        df = pd.DataFrame(data)
        csv_filename = f"{prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        print(f"💾 Saved CSV: {csv_filename}")
        
    except ImportError:
        print("ℹ️  Install pandas for CSV export: pip install pandas")
    
    return json_filename


def display_sample_jobs(jobs: List[Dict], count: int = 5):
    """Display sample jobs"""
    
    print(f"\n{'='*60}")
    print(f"📋 SAMPLE JOBS (First {count})")
    print(f"{'='*60}")
    
    for i, job in enumerate(jobs[:count], 1):
        print(f"\n{i}. [{job['source'].upper()}] {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Description: {job['description'][:100]}...")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function"""
    
    print("\n" + "🎯"*30)
    print("MULTI-SOURCE JOB COLLECTOR")
    print("🎯"*30)
    print("\nSources: Adzuna + The Muse + Remotive")
    
    # Get user input
    print("\n" + "="*60)
    print("COLLECTION OPTIONS")
    print("="*60)
    
    print("\n1. Quick test (100 jobs from all sources)")
    print("2. Medium collection (500 jobs)")
    print("3. Large collection (1000+ jobs)")
    print("4. Custom")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    collector = JobCollector()
    
    if choice == "1":
        # Quick test
        role = "Python Developer"
        jobs = collector.collect_all_sources(
            role=role,
            adzuna_pages=1,
            muse_pages=1,
            include_remotive=True
        )
        
    elif choice == "2":
        # Medium
        role = input("\nEnter job role: ").strip()
        jobs = collector.collect_all_sources(
            role=role,
            adzuna_pages=5,
            muse_pages=5,
            include_remotive=True
        )
        
    elif choice == "3":
        # Large
        role = input("\nEnter job role: ").strip()
        jobs = collector.collect_all_sources(
            role=role,
            adzuna_pages=10,
            muse_pages=10,
            include_remotive=True
        )
        
    else:
        # Custom
        role = input("\nEnter job role: ").strip()
        adzuna_pages = int(input("Adzuna pages (1 page = 50 jobs): ").strip())
        muse_pages = int(input("Muse pages (1 page = 20 jobs): ").strip())
        include_remotive = input("Include Remotive? (y/n): ").strip().lower() == 'y'
        
        jobs = collector.collect_all_sources(
            role=role,
            adzuna_pages=adzuna_pages,
            muse_pages=muse_pages,
            include_remotive=include_remotive
        )
    
    if jobs:
        # Print statistics
        collector.print_statistics()
        
        # Display samples
        display_sample_jobs(jobs)
        
        # Save jobs
        filename = save_jobs(jobs)
        
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"\n📁 Files created:")
        print(f"  • {filename}")
        print(f"\n🎯 Next steps:")
        print(f"  1. Run skill_extractor.py to analyze skills")
        print(f"  2. Use {filename} as input")
        
    else:
        print("\n❌ No jobs collected")
    
    print("\n")


if __name__ == "__main__":
    main()
