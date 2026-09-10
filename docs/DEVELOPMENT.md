# Saathi AI 2.0 — Development & Testing Guide

This document outlines developer guidelines, file utilities, testing standards, and error handling practices for the Saathi AI 2.0 codebase.

---

## 1. Development Principles

1. **Standard Python Packages**: Use modular Python modules inside `saathi/` rather than creating monolithic scripts.
2. **Robust Error Handling**: Wrap file reads and external HTTP/Ollama requests in explicit try-except blocks with clean fallback states.
3. **Automated Testing**: Ensure all new modules include unit tests in `tests/test_saathi_2.py`.

---

## 2. File Utilities (`saathi.tools.file_utils.FileUtils`)

```python
from saathi.tools import FileUtils
from pathlib import Path

# Safe JSON Reading
data = FileUtils.read_json(Path("data/config.json"))

# Safe CSV Reading
rows = FileUtils.read_csv(Path("data/sample.csv"))

# Safe Text Reading
content = FileUtils.read_text_safe(Path("notes.txt"))
```

---

## 3. Running Unit Tests

To run the complete test suite:
```cmd
py -3.12 -m unittest discover -s tests -p "test_*.py"
```

To run system diagnostics:
```cmd
py -3.12 -m saathi doctor
```

