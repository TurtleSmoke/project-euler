import re
import sys
from collections import defaultdict
from pathlib import Path
import ast


def get_problem_sources(problem_id):
    problem_path = Path() / f"problems/problem_{problem_id:04d}"
    problem_sources = defaultdict(dict)
    for path in problem_path.glob("*.py"):
        module = ast.parse(path.read_text())
        for node in module.body:
            if isinstance(node, ast.FunctionDef):
                problem_sources[path.stem][node.name] = ast.get_source_segment(
                    path.read_text(), node
                )
    return problem_sources


def generate_example(problem_id):
    problem_sources = get_problem_sources(problem_id)
    mdbook_src = Path() / f"mdbook_src/problems/problem_{problem_id:04d}"

    for path in mdbook_src.glob("solution[0-9]*.md"):
        with open(path, "r") as f:
            lines = f.readlines()
        for j, line in enumerate(lines):
            matches = re.match(r"\[//]: # \((\w*)\)", line)
            if matches:
                try:
                    solution, func_name = path.stem, matches.group(1)
                    if func_name not in problem_sources[solution]:
                        solution = "read_file"
                    src_code = problem_sources[solution][func_name]
                    lines[j] = (
                        f"From [{solution}.py](https://github.com/TurtleSmoke/Project-Euler/blob/main/problems/problem_"
                        f"{problem_id:04d}/{solution}.py):\n\n```python\n{src_code}\n```\n"
                    )
                except Exception as e:
                    print(f"Error with the following file: {path}")
                    print(e)
        with open(path, "w") as f:
            f.writelines(lines)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        generate_example(int(sys.argv[1]))
    else:
        problems_path = Path() / "problems/"
        for i in sorted(int(folder.stem[-4:]) for folder in problems_path.glob("*")):
            generate_example(i)
