from pathlib import Path
import fnmatch
import os
from models import get_chat_response

def should_ignore(path: Path, ignore_patterns: list) -> bool:
    """Check if path matches any gitignore patterns."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(str(path), pattern):
            return True
    return False

def parse_gitignore(gitignore_path: Path) -> list:
    """Parse .gitignore file and return list of patterns."""
    if not gitignore_path.exists():
        return []
    
    patterns = []
    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line.replace('/', os.sep))
    return patterns

def generate_repo_map(output_path: str = "output/repo_map.md") -> None:
    """
    Generate a markdown file describing the repository structure.
    
    Args:
        output_path: Path where to save the markdown file
    """
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(exist_ok=True)
    
    # Get gitignore patterns
    ignore_patterns = parse_gitignore(Path(".gitignore"))
    
    # Start with repo description
    content = ["# Repository Map\n\n"]
    content.append("## Directory Structure\n\n")
    
    # Define allowed paths
    repo_root = Path(".")
    allowed_paths = [
        repo_root / "src",
        repo_root / "README.md",
    ]
    
    # Add root .toml and .txt files
    allowed_paths.extend(repo_root.glob("*.toml"))
    allowed_paths.extend(repo_root.glob("*.txt"))
    
    # Process src directory
    for base_path in allowed_paths:
        if base_path.is_dir():
            paths = sorted(base_path.rglob("*"))
        else:
            paths = [base_path]
            
        for path in paths:
            # Skip ignored files
            if should_ignore(path, ignore_patterns):
                continue
                
            # Calculate relative path and indentation level
        rel_path = path.relative_to(repo_root)
        depth = len(rel_path.parts) - 1
        indent = "  " * depth
        
        # Add to content
        if path.is_dir():
            content.append(f"{indent}- 📁 **{path.name}**/\n")
        else:
            content.append(f"{indent}- 📄 `{path.name}`")
        
            # Get summary for Python files
            if path.suffix == '.py':
                try:
                    system_msg = "You are a technical documentation assistant. Provide a brief (<50 words) summary of the Python file contents."
                    file_content = path.read_text()
                    summary = get_chat_response(system_msg, file_content, model="gpt-4o-mini")
                    content.append(f" - {summary}\n")
                except Exception as e:
                    content.append(f" - Error getting summary: {str(e)}\n")
            else:
                content.append("\n")
    
    # Write to file
    with open(output_path, 'w') as f:
        f.writelines(content)
    
    print(f"Repository map generated at: {output_path}")

if __name__ == "__main__":
    generate_repo_map()
