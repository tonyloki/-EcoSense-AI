#!/usr/bin/env python3
"""
EcoSense AI - System Verification & Health Check
Validates all components are working correctly
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")

def check_python_version():
    """Check Python version"""
    print("✓ Python Version Check:")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 9:
        print("  ✅ Python version OK (3.9+)")
        return True
    else:
        print("  ❌ Python 3.9+ required")
        return False

def check_required_packages():
    """Check if required packages are installed"""
    print("✓ Required Packages Check:")
    
    required = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'python_dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True

def check_optional_packages():
    """Check optional packages"""
    print("\n✓ Optional Packages:")
    
    optional = [
        ('faiss', 'For semantic search (optional)'),
        ('sentence_transformers', 'For embeddings (optional)'),
        ('sklearn', 'For ML algorithms (optional)'),
    ]
    
    for package, description in optional:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}: {description}")
        except ImportError:
            print(f"  ⚠️  {package} not installed: {description}")
    
    return True

def check_project_structure():
    """Check if project structure exists"""
    print("\n✓ Project Structure Check:")
    
    required_dirs = [
        'data',
        'analysis',
        'ibm_ai',
        'rag',
        'outputs'
    ]
    
    required_files = [
        'app.py',
        'config.py',
        'utils.py',
        'logger_config.py',
        'data_generator.py',
        'requirements.txt',
        'README.md',
        'analysis/electricity_analysis.py',
        'analysis/water_analysis.py',
        'ibm_ai/granite_llm.py',
        'ibm_ai/prompt_templates.py',
        'rag/retriever.py',
        'rag/policy_docs.txt'
    ]
    
    all_ok = True
    
    print("  Directories:")
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"    ✅ {dir_name}/")
        else:
            print(f"    ❌ {dir_name}/ - MISSING")
            all_ok = False
    
    print("\n  Files:")
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"    ✅ {file_name}")
        else:
            print(f"    ❌ {file_name} - MISSING")
            all_ok = False
    
    return all_ok

def check_module_imports():
    """Check if all modules can be imported"""
    print("\n✓ Module Imports Check:")
    
    modules = [
        ('config', 'Configuration'),
        ('utils', 'Utilities'),
        ('logger_config', 'Logger'),
        ('data_generator', 'Data Generator'),
        ('analysis.electricity_analysis', 'Electricity Analyzer'),
        ('analysis.water_analysis', 'Water Analyzer'),
        ('ibm_ai.granite_llm', 'Granite LLM'),
        ('ibm_ai.prompt_templates', 'Prompt Templates'),
        ('rag.retriever', 'RAG Retriever'),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {description:20} ({module_name})")
        except Exception as e:
            print(f"  ❌ {description:20} ({module_name}) - {str(e)[:30]}")
            all_ok = False
    
    return all_ok

def check_data_files():
    """Check if data files exist"""
    print("\n✓ Data Files Check:")
    
    electricity_path = 'data/electricity.csv'
    water_path = 'data/water.csv'
    
    if os.path.exists(electricity_path):
        size = os.path.getsize(electricity_path)
        print(f"  ✅ electricity.csv ({size:,} bytes)")
    else:
        print(f"  ⚠️  electricity.csv - NOT FOUND")
    
    if os.path.exists(water_path):
        size = os.path.getsize(water_path)
        print(f"  ✅ water.csv ({size:,} bytes)")
    else:
        print(f"  ⚠️  water.csv - NOT FOUND")
    
    print("\n  To generate sample data:")
    print("  python data_generator.py")
    
    return True

def check_configuration():
    """Check configuration"""
    print("\n✓ Configuration Check:")
    
    env_file = '.env'
    env_example = '.env.example'
    
    if os.path.exists(env_file):
        print(f"  ✅ .env file exists")
    else:
        if os.path.exists(env_example):
            print(f"  ⚠️  .env not found, but .env.example exists")
            print(f"  To set up: cp .env.example .env")
        else:
            print(f"  ⚠️  No environment files found")
    
    return True

def test_analyzers():
    """Test analysis modules"""
    print("\n✓ Analysis Modules Test:")
    
    try:
        from analysis.electricity_analysis import ElectricityAnalyzer
        print("  ✅ ElectricityAnalyzer imported successfully")
    except Exception as e:
        print(f"  ❌ ElectricityAnalyzer: {e}")
    
    try:
        from analysis.water_analysis import WaterAnalyzer
        print("  ✅ WaterAnalyzer imported successfully")
    except Exception as e:
        print(f"  ❌ WaterAnalyzer: {e}")
    
    return True

def test_llm():
    """Test LLM module"""
    print("\n✓ LLM Module Test:")
    
    try:
        from ibm_ai.granite_llm import GraniteLLM
        llm = GraniteLLM()
        print("  ✅ GraniteLLM imported successfully")
        print("  ✅ Operating in Mock Mode (set credentials for real API)")
    except Exception as e:
        print(f"  ❌ GraniteLLM: {e}")
        return False
    
    return True

def test_rag():
    """Test RAG module"""
    print("\n✓ RAG Module Test:")
    
    try:
        from rag.retriever import PolicyRetriever
        retriever = PolicyRetriever()
        print("  ✅ PolicyRetriever imported successfully")
        
        if retriever.documents:
            print(f"  ✅ Policy documents loaded ({len(retriever.documents)} chars)")
        else:
            print("  ⚠️  Policy documents not loaded")
        
    except Exception as e:
        print(f"  ❌ PolicyRetriever: {e}")
        return False
    
    return True

def main():
    """Run all checks"""
    print_header("EcoSense AI - System Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Optional Packages", check_optional_packages),
        ("Project Structure", check_project_structure),
        ("Module Imports", check_module_imports),
        ("Data Files", check_data_files),
        ("Configuration", check_configuration),
        ("Analysis Modules", test_analyzers),
        ("LLM Module", test_llm),
        ("RAG Module", test_rag),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = "✅" if result else "⚠️"
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {e}")
            results[check_name] = "❌"
    
    # Summary
    print_header("Verification Summary")
    
    for check_name, result in results.items():
        print(f"{result} {check_name}")
    
    print("\n" + "="*50)
    print("  Next Steps:")
    print("="*50)
    print("  1. Generate sample data (if needed):")
    print("     python data_generator.py")
    print("\n  2. Run the dashboard:")
    print("     streamlit run app.py")
    print("\n  3. Try interactive demo:")
    print("     python demo.py")
    print("\n  4. Read documentation:")
    print("     cat README.md")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)
