import re
from pathlib import Path

ATLAS = "D:/atlas-project/atlas-project"

print(f"Working in {ATLAS}")

pyproject = Path("D:/atlas-project/atlas-project/pyproject.toml")
print(f"Reading {pyproject}")
print(f"Modifying {pyproject}")
text = pyproject.read_text()
text = re.sub(r'(?m)^atlas = ".*"$', 'atlas = "atlas.cli:main"', text)

sections = {
    "tool.ruff.lint": """[tool.ruff.lint]
select = [
    "E",   # pycodestyle: style errors
    "F",   # pyflakes: unused or undefined names
    "I",   # isort: import order
    "B",   # bugbear: likely bugs
    "UP",  # pyupgrade: modern syntax
]""",
    "tool.pytest.ini_options": """[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=atlas" """,
}

for name, section in sections.items():
    pattern = rf"(?ms)^\[{re.escape(name)}\]\n.*?(?=^\[|\Z)"
    text = re.sub(pattern, "", text)
    text = f"{text.rstrip()}\n\n{section}\n"

pyproject.write_text(text)
#assert 'atlas = "atlas.cli:main"' in text
print("pyproject.toml updated")