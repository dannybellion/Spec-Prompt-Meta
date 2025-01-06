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
    
    # Define allowed paths and structure
    repo_root = Path(".")
    
    # Start with root level files
    root_files = [
        repo_root / "README.md",
        *repo_root.glob("*.toml"),
        *repo_root.glob("*.txt"),
    ]
    
    # Track processed paths and folder structure
    processed_paths = set()
    folder_structure = {}
    
    # Process root files first
    for path in sorted(root_files):
        if not should_ignore(path, ignore_patterns) and path not in processed_paths:
            content.append(f"- 📄 `{path.name}`\n")
            processed_paths.add(path)
    
    # Process src directory
    src_path = repo_root / "src"
    if src_path.exists():
        content.append("\n- 📁 **src**/\n")  # Add src folder header
        
        # First collect and sort all valid paths
        valid_paths = []
        for path in sorted(src_path.rglob("*")):
            if not should_ignore(path, ignore_patterns) and "__pycache__" not in str(path):
                valid_paths.append(path)
        
        # Process directories and their files together
        def process_directory(current_path, current_depth=0):
            indent = "  " * current_depth
            
            # Process directories and files
            dirs = []
            files = []
            for path in valid_paths:
                if path.parent == current_path:
                    if path.is_dir() and path not in processed_paths:
                        dirs.append(path)
                    elif not path.is_dir() and path not in processed_paths:
                        files.append(path)
            
            # Process subdirectories first
            for dir_path in sorted(dirs):
                content.append(f"{indent}- 📁 **{dir_path.name}**/\n")
                processed_paths.add(dir_path)
                # Recursively process the subdirectory
                process_directory(dir_path, current_depth + 1)
            
            # Then add files under current directory
            for file in sorted(files):
                content.append(f"{indent}- 📄 `{file.name}`\n")
                processed_paths.add(file)
        
        # Start processing from src directory
        process_directory(src_path)
        
            # Get summary for Python files
            # if path.suffix == '.py':
            #     try:
            #         system_msg = "You are a technical documentation assistant. Provide a brief (<50 words) summary of the Python file contents."
            #         file_content = path.read_text()
            #         summary = get_chat_response(system_msg, file_content, model="gpt-4o-mini")
            #         content.append(f" - {summary}\n")
            #     except Exception as e:
            #         content.append(f" - Error getting summary: {str(e)}\n")
            # else:
            #     content.append("\n")
    
    # Write to file
    with open(output_path, 'w') as f:
        f.writelines(content)
    
    print(f"Repository map generated at: {output_path}")

if __name__ == "__main__":
    generate_repo_map()
