import re
import sys
from pathlib import Path


def remove_example(problem_id):
    """Remove code block and add template for future generation"""
    for path in Path("mdbook_src/problems").glob(
        f"problem_{problem_id:04d}/solution[0-9]*.md"
    ):
        with open(path, "r") as f:
            lines = f.readlines()
        keep = []
        current_line = 0
        while current_line < len(lines):
            matches = re.match(r"From \[.*\.py", lines[current_line])
            if matches:
                match = re.match(r"def (\w+)", lines[current_line + 3])
                keep.append(f"[//]: # ({match.group(1)})\n")
                try:
                    while lines[current_line] != "```\n":
                        current_line += 1
                except Exception as e:
                    print(f"Error with the following file: {path}")
                    print(e)
            else:
                keep.append(lines[current_line])
            current_line += 1

        with open(path, "w") as f:
            f.writelines(keep)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        remove_example(int(sys.argv[1]))
    else:
        problems_path = Path() / "problems/"
        for i in sorted(int(folder.stem[-4:]) for folder in problems_path.glob("*")):
            remove_example(i)
