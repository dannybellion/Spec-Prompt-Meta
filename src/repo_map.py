from pathlib import Path
import fnmatch
import os

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
    
    # Walk through repository
    repo_root = Path(".")
    for path in sorted(repo_root.rglob("*")):
        # Skip git directory and ignored files
        if ".git" in path.parts or should_ignore(path, ignore_patterns):
            continue
            
        # Calculate relative path and indentation level
        rel_path = path.relative_to(repo_root)
        depth = len(rel_path.parts) - 1
        indent = "  " * depth
        
        # Add to content
        if path.is_dir():
            content.append(f"{indent}- 📁 **{path.name}**/\n")
        else:
            content.append(f"{indent}- 📄 `{path.name}`\n")
    
    # Write to file
    with open(output_path, 'w') as f:
        f.writelines(content)
    
    print(f"Repository map generated at: {output_path}")

if __name__ == "__main__":
    generate_repo_map()
