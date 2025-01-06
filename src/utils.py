from pathlib import Path
from jinja2 import Template

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

def render_prompt(template: str, examples: str, transcript: str, repo_map: str) -> str:
    """Render the Jinja2 template with provided template, examples and transcript"""
    with open('src/prompt.j2') as f:
        template_content = f.read()
    
    jinja_template = Template(template_content)
    return jinja_template.render(
        template=template,
        examples=examples,
        transcript=transcript,
        repo_map=repo_map
    )


