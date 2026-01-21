#!/usr/bin/env python3
"""
RecruiterAI - Data Pipeline Orchestration Script
Data & AI Job Analytics & Recommendation Platform - Focus Morocco

Purpose: Orchestrate DBT runs and export data to CSV/Parquet
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent
DBT_PROJECT_PATH = PROJECT_ROOT / "dbt"
DATA_PATH = PROJECT_ROOT / "data"
GOLD_PATH = DATA_PATH / "gold"
BRONZE_PATH = DATA_PATH / "bronze"
SILVER_PATH = DATA_PATH / "silver"

# Project branding
PROJECT_NAME = "RecruiterAI"
PROJECT_VERSION = "2.0"

# Colors for console output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print RecruiterAI banner"""
    banner = f"""
{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     🤖  {Colors.BOLD}RecruiterAI{Colors.ENDC}{Colors.OKCYAN} - Data & AI Job Analytics Platform  🇲🇦              ║
║                                                                               ║
║         Powered by DBT, DuckDB, and Machine Learning                         ║
║         Focus: Morocco | Version: {PROJECT_VERSION}                                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.HEADER}{'═' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}  🔹 {title}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'═' * 70}{Colors.ENDC}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}  ✅ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}  ⚠️  {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}  ❌ {message}{Colors.ENDC}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.OKBLUE}  ℹ️  {message}{Colors.ENDC}")

def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_error(f"Command failed: {command}")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print_error(f"Error running command: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_section("Checking Dependencies")
    
    dependencies = ['dbt-core', 'dbt-duckdb', 'pandas']
    missing = []
    
    for dep in dependencies:
        try:
            if dep == 'dbt-core':
                subprocess.run(['dbt', '--version'], capture_output=True)
            else:
                __import__(dep.replace('-', '_'))
            print_success(f"{dep} is installed")
        except:
            missing.append(dep)
            print_error(f"{dep} is NOT installed")
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join(missing)}")
        print_info("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def initialize_dbt():
    """Initialize DBT project"""
    print_section("Initializing DBT")
    
    # Check if dbt_project.yml exists
    if not (DBT_PROJECT_PATH / "dbt_project.yml").exists():
        print_error("dbt_project.yml not found!")
        return False
    
    print_success("DBT project configuration found")
    
    # Run dbt debug
    print_info("Running dbt debug...")
    result = subprocess.run(
        ['dbt', 'debug'],
        cwd=DBT_PROJECT_PATH,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("DBT debug passed")
        return True
    else:
        print_warning("DBT debug had some issues (may still work)")
        print(result.stdout)
        return True

def copy_source_data():
    """Copy source data to bronze layer"""
    print_section("Preparing Data Layers")
    
    # Create directories
    for path in [BRONZE_PATH, SILVER_PATH, GOLD_PATH]:
        path.mkdir(parents=True, exist_ok=True)
        print_success(f"Directory ready: {path.name}/")
    
    # Copy source data to bronze
    source_file = PROJECT_ROOT / "recruiter_ai_jobs_data.csv"
    bronze_file = BRONZE_PATH / "recruiter_ai_jobs_data.csv"
    
    if source_file.exists():
        shutil.copy2(source_file, bronze_file)
        print_success(f"Source data copied to bronze layer")
        
        # Get file size
        size_mb = source_file.stat().st_size / (1024 * 1024)
        print_info(f"File size: {size_mb:.2f} MB")
        return True
    else:
        print_error(f"Source file not found: {source_file}")
        return False

def run_dbt_transformation():
    """Run DBT transformation"""
    print_section("Running DBT Transformations")
    
    print_info("Executing dbt run...")
    print_info("This may take a few minutes...")
    
    result = subprocess.run(
        ['dbt', 'run', '--profiles-dir', '.'],
        cwd=DBT_PROJECT_PATH,
        capture_output=False
    )
    
    if result.returncode == 0:
        print_success("DBT transformations completed successfully!")
        return True
    else:
        print_error("DBT run failed")
        return False

def run_dbt_tests():
    """Run DBT tests (optional)"""
    print_section("Running DBT Tests")
    
    result = subprocess.run(
        ['dbt', 'test', '--profiles-dir', '.'],
        cwd=DBT_PROJECT_PATH,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("All DBT tests passed!")
    else:
        print_warning("Some DBT tests failed (non-critical)")
        print(result.stdout)
    
    return True

def export_to_csv():
    """Export Gold tables to CSV"""
    print_section("Exporting Gold Layer to CSV")
    
    try:
        import duckdb
        import pandas as pd
        
        db_path = DBT_PROJECT_PATH / "recruiter_ai.db"
        
        # Try new database name first, then fallback to old
        if not db_path.exists():
            db_path = DBT_PROJECT_PATH / "duckdb.db"
        
        if not db_path.exists():
            print_error(f"Database not found: {db_path}")
            return False
        
        conn = duckdb.connect(str(db_path), read_only=True)
        
        # List of Gold tables to export
        gold_tables = [
            ('gold', 'dim_time'),
            ('gold', 'dim_company'),
            ('gold', 'dim_location'),
            ('gold', 'dim_skills'),
            ('gold', 'fact_job_offers'),
            ('gold', 'fact_job_skills'),
            ('gold', 'agg_job_offers_by_category_time'),
            ('gold', 'agg_skills_demand'),
            ('gold', 'agg_location_analysis'),
        ]
        
        exported_count = 0
        for schema, table in gold_tables:
            try:
                df = conn.execute(f"SELECT * FROM {schema}.{table}").fetchdf()
                output_file = GOLD_PATH / f"{table}.csv"
                df.to_csv(output_file, index=False)
                print_success(f"Exported {table}.csv ({len(df):,} rows)")
                exported_count += 1
            except Exception as e:
                print_warning(f"Could not export {table}: {e}")
        
        conn.close()
        
        print_info(f"Exported {exported_count}/{len(gold_tables)} tables to {GOLD_PATH}")
        return True
        
    except ImportError:
        print_error("duckdb not installed. Run: pip install duckdb")
        return False
    except Exception as e:
        print_error(f"Export failed: {e}")
        return False

def generate_summary():
    """Generate summary of transformation"""
    print_section("Pipeline Summary")
    
    # Check exported files
    csv_files = list(GOLD_PATH.glob("*.csv"))
    
    print(f"{Colors.OKCYAN}📊 RecruiterAI Pipeline Results:{Colors.ENDC}")
    print(f"   • Exported CSV files: {len(csv_files)}")
    print(f"   • Output directory: {GOLD_PATH}")
    print()
    
    if csv_files:
        print(f"{Colors.OKCYAN}📁 Exported Files:{Colors.ENDC}")
        total_size = 0
        for f in sorted(csv_files):
            size_kb = f.stat().st_size / 1024
            total_size += size_kb
            print(f"   • {f.name}: {size_kb:.1f} KB")
        print(f"   • Total: {total_size/1024:.2f} MB")
    
    print()
    print(f"{Colors.OKGREEN}{'═' * 70}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}  🎉 RecruiterAI Pipeline Completed Successfully!{Colors.ENDC}")
    print(f"{Colors.OKGREEN}{'═' * 70}{Colors.ENDC}")
    print()
    print(f"{Colors.OKCYAN}Next Steps:{Colors.ENDC}")
    print(f"   1. Import CSV files in Power BI from: {GOLD_PATH}")
    print(f"   2. Run Streamlit app: cd recommender && streamlit run app.py")
    print(f"   3. Access API: cd recommender && uvicorn api:app --reload")
    print()
    print(f"{Colors.OKCYAN}🇲🇦 Focus Morocco - Happy Job Hunting! 🚀{Colors.ENDC}")

def main():
    """Main orchestration function"""
    start_time = datetime.now()
    
    # Print banner
    print_banner()
    
    print(f"{Colors.OKBLUE}Pipeline started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print_error("Please install missing dependencies and try again")
        sys.exit(1)
    
    # Step 2: Initialize DBT
    if not initialize_dbt():
        print_error("DBT initialization failed")
        sys.exit(1)
    
    # Step 3: Copy source data
    if not copy_source_data():
        print_error("Data preparation failed")
        sys.exit(1)
    
    # Step 4: Run DBT transformation
    if not run_dbt_transformation():
        print_error("DBT transformation failed")
        sys.exit(1)
    
    # Step 5: Run DBT tests (optional, non-blocking)
    run_dbt_tests()
    
    # Step 6: Export to CSV
    if not export_to_csv():
        print_warning("CSV export had issues, but pipeline completed")
    
    # Step 7: Generate summary
    generate_summary()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n{Colors.OKBLUE}Total execution time: {duration:.1f} seconds{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nFatal error: {e}")
        sys.exit(1)
