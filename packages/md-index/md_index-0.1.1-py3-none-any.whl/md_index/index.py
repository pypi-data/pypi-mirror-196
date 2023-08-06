from pathlib import Path
from typing import List

folders_ignore = ["docs", "tests", "site", "src", "dist", "build"]


def generate_index(dir: Path, output_dir: Path, depth: int, url_prefix: str):
    """Generate a markdown index for the given directory."""
    ensure_yml()
    make_homepage(dir, output_dir, required=True)
    folders = get_folders(dir)
    if depth == 1:
        for folder in folders:
            index_path = output_dir / f"{folder.name}.md"
            make_index(folder, index_path, url_prefix)
    elif depth == 2:
        for folder in folders:
            make_homepage(folder, output_dir / folder.name)
            sub_folders = get_folders(folder)
            for sub_folder in sub_folders:
                index_path = output_dir / folder.name / f"{sub_folder.name}.md"
                make_index(sub_folder, index_path, url_prefix)


def make_index(dir: Path, index_path: Path, url_prefix: str):
    """Make a file-list markdown file for the given directory."""
    with open(index_path, "w", encoding="utf-8") as f:
        readme_path = dir / "README.md"
        if readme_path.is_file():
            f.write(readme_path.read_text(encoding="utf-8") + "\n\n")
        else:
            f.write(f"# {dir.name}\n")
        f.write("## File list\n\n")
        files_str = get_file_tree(dir, url_prefix)
        f.write(files_str)


def make_homepage(dir: Path, output_dir: Path, required=False):
    """Make a homepage markdown file for the site."""
    readme_path = dir / "README.md"
    index_path = output_dir / "index.md"
    output_dir.mkdir(parents=True, exist_ok=True)
    if readme_path.is_file():
        readme_str = readme_path.read_text(encoding="utf-8")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(readme_str)
    elif required:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"# File Index\n")


def ensure_yml():
    yml_path = Path.cwd() / "mkdocs.yml"
    if not yml_path.is_file():
        with open(yml_path, "w", encoding="utf-8") as f:
            f.write("site_name: File Index\n")
            f.write("theme: readthedocs\n")


def get_folders(dir: Path) -> List[Path]:
    """Return a list of folders in the given directory."""
    folders = dir.glob("*")
    folders = [
        folder
        for folder in folders
        if folder.is_dir()
        and not folder.name.startswith(".")
        and folder.name not in folders_ignore
    ]
    folders.sort(key=lambda x: x.name)
    return folders


def get_file_tree(path: Path, url_prefix: str, depth: int = -1, tree_str: str = ""):
    if path.is_file():
        if path.name == "README.md":
            return tree_str
        path_str = str(path).replace("\\", "/")
        tree_str += "    " * depth + f"- [{path.name}]({url_prefix}{path_str})\n"
    elif path.is_dir():
        if depth != -1:
            tree_str += (
                "    " * depth + "- " + str(path.relative_to(path.parent)) + "\n"
            )
        for cp in sorted(path.iterdir(), key=lambda x: x.stem):
            tree_str = get_file_tree(cp, url_prefix, depth + 1, tree_str)
    return tree_str
