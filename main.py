import ast
import os

def extract_imports_from_file(file_path):
    """Extracts all imports from a given Python file."""
    try:
        with open(file_path, 'r') as file:
            print(f"Opening file: {file_path}")
            tree = ast.parse(file.read(), filename=file_path)
    except (OSError, SyntaxError) as e:
        print(f"Error processing file {file_path}: {e}")
        return set()
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports

def get_imports_from_directory(directory_path):
    """Walks through all Python files in a directory and extracts imports."""
    all_imports = set()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                imports = extract_imports_from_file(file_path)
                all_imports.update(imports)
    return all_imports

def check_imports_installed(imports):
    """Checks whether the required main modules are installed in the environment."""
    missing = []
    modules_to_be_ignored = {"name_of_module_ignored_1", "name_of_module_ignored_2"}
    checked_modules = set()
    
    for package in imports:
        main_module = package.split('.')[0]
        if main_module in modules_to_be_ignored:
            print(f"Ignoring module: {main_module}")
            continue

        if main_module not in checked_modules:
            checked_modules.add(main_module)
            print(f"Checking module: {main_module}")
            try:
                __import__(main_module)
            except ImportError:
                missing.append(main_module)
    
    return missing

# Example usage
directory_path = os.path.dirname(os.path.abspath(__file__))
imports = get_imports_from_directory(directory_path)

print(f"\nTotal imports found: {len(imports)}")
print(imports)

missing_imports = check_imports_installed(imports)

if missing_imports:
    missing_imports = sorted(set(missing_imports))
    print(f"\nThe following main imports are missing:")
    for imp in missing_imports:
        print(f"- {imp}")
    print(f"\nTotal missing imports: {len(missing_imports)}")
else:
    print(f"\nAll imports are installed.\n")
