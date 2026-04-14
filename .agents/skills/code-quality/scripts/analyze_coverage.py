#!/usr/bin/env python3
"""
Coverage Analyzer

Analiza coverage reports y sugiere dónde agregar tests.

Usage:
    python analyze_coverage.py --project . --target 85
    python analyze_coverage.py --project . --target 85 --fix
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def analyze_coverage(output: str, target: float) -> dict:
    """Analiza output de coverage y sugiere mejoras."""
    analysis = {
        "total_percent": 0.0,
        "modules": [],
        "low_coverage": [],
        "missing": [],
        "suggestions": [],
    }

    current_module = None
    lines = output.split("\n")

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        if "TOTAL" in line:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    analysis["total_percent"] = float(parts[3].replace("%", ""))
                except ValueError:
                    pass

        if "---" in line and i > 0:
            if lines[i - 1].strip() and not lines[i - 1].startswith("Name"):
                current_module = lines[i - 1].strip()

        if current_module and "%" in line and "---" not in line:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    module_name = current_module.split("/")[-1].replace(".py", "")
                    percent = float(parts[3].replace("%", ""))
                    missing = parts[4] if len(parts) > 4 else ""

                    analysis["modules"].append(
                        {"name": current_module, "percent": percent, "missing": missing}
                    )

                    if percent < target:
                        analysis["low_coverage"].append(
                            {
                                "name": current_module,
                                "percent": percent,
                                "missing": missing,
                            }
                        )
                except (IndexError, ValueError):
                    pass

    gap = target - analysis["total_percent"]
    if gap > 0:
        analysis["suggestions"].append(
            f"Need {gap:.1f}% more coverage to reach target of {target}%"
        )

    return analysis


def generate_test_template(module_name: str, missing_lines: list[str]) -> str:
    """Genera template de tests para un módulo."""
    module = module_name.split("/")[-1].replace(".py", "")
    class_name = "".join(word.capitalize() for word in module.split("_"))

    template = f'''"""Tests for {module} module."""

import pytest
from {module} import *


class Test{class_name}:
    """Test suite for {module} module."""
    
    def test_module_imports(self):
        """Verify module imports correctly."""
        assert True
    
'''

    if missing_lines:
        template += f"""    # TODO: Add tests for missing lines: {", ".join(missing_lines[:5])}
"""

    return template


def main():
    parser = argparse.ArgumentParser(description="Analyze and improve test coverage")
    parser.add_argument("--project", "-p", default=".", help="Project directory")
    parser.add_argument(
        "--target", "-t", type=float, default=85.0, help="Target coverage percentage"
    )
    parser.add_argument(
        "--fix",
        "-f",
        action="store_true",
        help="Generate test templates for low coverage modules",
    )
    parser.add_argument("--module", "-m", help="Analyze specific module")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()

    print(f"📊 Analyzing coverage (target: {args.target}%)...\n")

    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=term",
        "-v",
    ]

    if args.module:
        cmd.extend(["--cov", args.module])

    _, output, _ = run_command(cmd, project_path)

    analysis = analyze_coverage(output, args.target)

    print(f"Current Coverage: {analysis['total_percent']:.1f}%")
    print(f"Target Coverage: {args.target}%\n")

    if analysis["low_coverage"]:
        print("⚠️  Modules below target:\n")
        for mod in sorted(analysis["low_coverage"], key=lambda x: x["percent"]):
            print(f"  {mod['name']}: {mod['percent']:.1f}%")
            print(f"    Missing: {mod['missing']}")
            print()

    if analysis["suggestions"]:
        for suggestion in analysis["suggestions"]:
            print(f"💡 {suggestion}\n")

    if args.fix and analysis["low_coverage"]:
        print("🔧 Generating test templates...\n")

        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        for mod in analysis["low_coverage"]:
            module_name = mod["name"]
            missing = mod["missing"].split(", ") if mod["missing"] else []

            test_name = module_name.replace("/", "_").replace(".py", "") + "_test.py"
            test_path = tests_dir / test_name

            if test_path.exists():
                print(f"  ⏭️  Skipping {test_name} (already exists)")
                continue

            template = generate_test_template(module_name, missing)
            test_path.write_text(template)
            print(f"  ✅ Generated: {test_path}")


if __name__ == "__main__":
    main()
