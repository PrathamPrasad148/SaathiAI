"""
Saathi AI 2.0 CLI Entry Point
"""

import sys
from saathi.cli.doctor import run_doctor

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "doctor":
        run_doctor()
    else:
        print("Saathi AI 2.0 CLI")
        print("Run 'python -m saathi doctor' to execute system diagnostics.")

if __name__ == "__main__":
    main()

