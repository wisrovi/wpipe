#!/usr/bin/env python3
"""
README Generator - Generate professional README.md

Usage:
    python generate_readme.py --project . --output README.md
"""

import argparse
import subprocess
from pathlib import Path


def detect_stack(project_path: Path) -> dict:
    """Detect technology stack from project files."""
    stack = {
        "language": "Python",
        "framework": None,
        "database": None,
        "testing": "pytest",
        "logging": "loguru",
    }

    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text().lower()
        if "fastapi" in content:
            stack["framework"] = "FastAPI"
        elif "flask" in content:
            stack["framework"] = "Flask"
        elif "django" in content:
            stack["framework"] = "Django"

    if (project_path / "requirements.txt").exists():
        reqs = (project_path / "requirements.txt").read_text().lower()
        if "postgresql" in reqs or "psycopg" in reqs:
            stack["database"] = "PostgreSQL"
        elif "mysql" in reqs:
            stack["database"] = "MySQL"
        elif "sqlite" in reqs:
            stack["database"] = "SQLite"

    return stack


def generate_readme(project_path: Path, stack: dict) -> str:
    """Generate README.md content."""
    name = project_path.name.replace("-", " ").replace("_", " ").title()

    readme = f"""# {name}

[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)

## 🚀 Quick Start

```bash
git clone <repo>
cd {project_path.name}
make install
make test
```

## ✨ Features

- **Feature 1**: Description
- **Feature 2**: Description
- **Code Quality**: Pylint ≥ 9.0
- **Security**: Bandit compliant

## 📊 Architecture

```mermaid
graph TB
    User --> API --> Service --> Database
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | {stack["language"]} |
| Framework | {stack.get("framework", "N/A")} |
| Database | {stack.get("database", "N/A")} |
| Testing | {stack["testing"]} |
| Logging | {stack["logging"]} |

## 📦 Installation

```bash
make install
```

## 📖 Usage

```bash
make help      # Show all commands
make lint      # Run linters
make test      # Run tests
make run       # Run application
```

## 🧪 Testing

```bash
make test
```

## 📚 Documentation

Full documentation available at [docs/](docs/)

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

## Author

**[Author]**
AI Solutions Architect & Technology Evangelist
"""

    return readme


def main():
    parser = argparse.ArgumentParser(description="Generate README.md")
    parser.add_argument("--project", "-p", default=".", help="Project directory")
    parser.add_argument("--output", "-o", default="README.md", help="Output file")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()
    stack = detect_stack(project_path)
    readme = generate_readme(project_path, stack)

    output_path = Path(args.output)
    output_path.write_text(readme)

    print(f"✅ Generated: {output_path}")


if __name__ == "__main__":
    main()
