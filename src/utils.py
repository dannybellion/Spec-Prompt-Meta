from pathlib import Path

def load_template() -> str:
    """Load the content of spec prompt template file"""
    template_path = Path("context") / "spec-prompt-template.md"
    if template_path.exists():
        return template_path.read_text()
    else:
        print(f"Warning: {template_path} not found")
        return ""

def load_examples() -> str:
    """Load the content of spec prompt examples file"""
    examples_path = Path("context") / "spec-prompt-examples.md"
    if examples_path.exists():
        return examples_path.read_text()
    else:
        print(f"Warning: {examples_path} not found")
        return ""
