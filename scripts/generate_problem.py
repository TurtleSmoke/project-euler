import html
import os
import re
import sys
from textwrap import dedent

import requests
from bs4 import BeautifulSoup as bs, NavigableString

# Folder
MDBOOK_SRC = "mdbook_src"
MDBOOK_PROBLEMS = f"{MDBOOK_SRC}/problems"
MDBOOK_PROBLEM = lambda n: f"{MDBOOK_PROBLEMS}/problem_{n:04d}"
PYTHON_PROBLEMS = "problems"
PYTHON_PROBLEM = lambda n: f"{PYTHON_PROBLEMS}/problem_{n:04d}"

# Markdown file
SUMMARY_MD = f"{MDBOOK_SRC}/SUMMARY.md"
PROBLEM_MD = lambda n: f"{MDBOOK_PROBLEM(n)}/problem.md"
SOLUTION_MD = lambda n: f"{MDBOOK_PROBLEM(n)}/solution.md"
SOLUTION1_MD = lambda n: f"{MDBOOK_PROBLEM(n)}/solution1.md"

# Python file
PROBLEM_PY = lambda n: f"{PYTHON_PROBLEM(n)}/solution1.py"

# Project Euler URL
BASE_URL = "https://projecteuler.net"
PROBLEMS_URL = f"{BASE_URL}/minimal=problems"
MINIMAL_URL = lambda n: f"{BASE_URL}/minimal={n}"
PROBLEM_URL = lambda n: f"{BASE_URL}/problem={n}"


def render_number(line):
    # Replace .../... with \frac{...}{...}
    line = re.sub(
        r"(\d+|[a-z])/(\d+|[a-z])", r"\\\\( \\\\frac{\g<1>}{\g<2>} \\\\)", line
    )
    # Replace number or operator with \\( ... \\) if there is no "{" before (created by \frac{...}{...})
    line = re.sub(r"([^{])(\d+|[+−\-*^=/<>×!]|[.]{3})", r"\g<1>\\\\( \g<2> \\\\)", line)
    # Replace → with \\( \\rightarrow \\)
    line = re.sub(r"→", r"\\\\( \\\\rightarrow \\\\)", line)

    # Remove \\) \\(
    line = re.sub(r" \\\\\)\s*\\\\\( ", r"", line)
    # Remove \\) \\( wrapping "th"
    line = re.sub(r" \\\\\)\s*(th)\s*\\\\\( ", r"\g<1>", line)
    # Remove - with 'one-hundred'
    line = re.sub(r"\\\\\(\s*([−\-]*)\s*\\\\\)", r"\g<1>", line)
    # Remove - with '1000-digit'
    line = re.sub(r"\\\\\( (\d+)- \\\\\)", r"\\\\( \g<1> \\\\)-", line)
    # Remove - with 'n-digit'
    line = re.sub(r"\\\\\( n- \\\\\)", r"\\\\( n \\\\)-", line)
    # Remove lonely !
    line = re.sub(r"\\\\\(\s*!\s*\\\\\)", r"!", line)

    return line


def replace_tags(line, multiline=False):
    # Replace <br/> with \n
    line = re.sub(r"<br.*/>", r"\n", line)

    # Multiline implies that "line" is wrapped in \\[ ... \\], thus we don't need to wrap it again with \\( ... \\)
    if multiline:
        # Replace <i>...</i> with ...
        line = re.sub(r"<i>([^<]*)</i>", r"\g<1>", line)
        # Replace <sub>...</sub> with _{...} if multiline
        line = re.sub(r"<sub>([^<]*)</sub>", r"_{\g<1>}", line)
        # Replace <sup>...</sup> with ^{...} if multiline
        line = re.sub(r"<sup>([^<]*)</sup>", r"^{\g<1>}", line)
        # Replace <var>...</var> with ...
        line = re.sub(r"<var>([^<]*)</var>", r"\g<1>", line)
        # Remove double new line
        line = re.sub(r"\n\n", r"\n", line)
        # Replace .../... with \frac{...}{...}
        line = re.sub(r"([^\s^/]+)/([^\s^/]+)", r"\\\\frac{\g<1>}{\g<2>}", line)
        # Replace → with \\rightarrow
        line = re.sub(r"→", r"\\\\rightarrow", line)

    # Replace $*...$* with \(...\), equation will be render based on what is inside
    line = re.sub(r"\$*([^$]*)\$*", r"\g<1>", line)
    return line


def get_raw(s):
    return html.unescape(s.decode_contents()).replace("\n\n", "\n").strip("\n").strip()


def render_problem_content(content_html):
    soup = bs(content_html, "html.parser")
    rendered_content = []
    for s in soup:
        if isinstance(s, NavigableString):
            if s.strip():
                if s.strip().startswith("$$") and s.strip().endswith("$$"):
                    rendered_content.append(
                        "\\\\[\n" + replace_tags(str(s.strip()), True) + "\n\\\\]"
                    )
            continue
        line = get_raw(s)
        if s.find("img"):
            img = s.find("img")
            img["src"] = f"{BASE_URL}/" + img["src"]
            line = str(img.wrap(soup.new_tag("p", **{"style": "text-align: center;"})))
        elif s.name == "blockquote":
            line = "".join([("\n" if tag.name == "br" else "") + tag.text for tag in s])
            line = (r"\\\\" + "\n").join([l for l in line.split("\n") if l])
            line = (
                "\\\\[\n\\begin{align}\n"
                + replace_tags(line, True)
                + "\\end{align}\n\\\\]"
            )
        elif s.has_attr("class") and (
            "center" in s["class"] or "margin_left" in s["class"]
        ):
            if s.find({"span": "class=red"}):
                reds = s.find_all({"span": "class=red"})
                for red in reds:
                    line = line.replace(str(red), f"\\color{{red}}{{{red.text}}}")

            line = replace_tags(line, True)
            line = (r"\\\\\\\\" + "\n").join([l for l in line.split("\n") if l])
            line = "\\\\[\n" + replace_tags(line, True) + "\n\\\\]"
        else:
            if len(s.find_all()) > 0:
                # List of (line, must_render)
                new_line = []
                for random_tag in s:
                    if random_tag.name == "b":
                        new_line.append((f"**{random_tag.text}**", False))
                    elif random_tag.name == "a":
                        # If link is absolute, use it, else append BASE_URL
                        base = (
                            ""
                            if random_tag["href"].startswith("https://")
                            else f"{BASE_URL}/"
                        )
                        new_line.append(
                            (f"[{random_tag.text}]({base}{random_tag['href']})", False)
                        )
                    elif random_tag.name == "dfn":
                        new_line.append((f"*{random_tag.text}*", False))
                    elif random_tag.name == "var":
                        new_line.append((f"\\\\( {random_tag.text} \\\\)", True))
                    elif random_tag.name == "br":
                        new_line.append(("\n", True))
                    elif random_tag.name == "li":
                        new_line.append((f"- {random_tag.text}", False))
                    else:
                        new_line.append((random_tag.text, True))

                merged_rendered = []
                for i, (text, render) in enumerate(new_line):
                    # If both previous and current must be rendered, merge them
                    if i > 0 and merged_rendered[-1][1] and render:
                        merged_rendered[-1] = (merged_rendered[-1][0] + text, True)
                    else:
                        merged_rendered.append((text, render))
                merged_rendered = [
                    render_number(text) if render else text
                    for text, render in merged_rendered
                ]
                line = "".join(merged_rendered)
            else:
                line = replace_tags(render_number(line))

        rendered_content.append(line)

    return "> " + "\n\n".join(rendered_content).replace("\n", "\n> ") + "\n"


class Problem:
    """
    Create template for markdown/python
    """

    def __init__(self, qid):
        self.id = qid
        self.title = (
            requests.get(PROBLEMS_URL, timeout=5).text.split("\n")[qid].split("##")[1]
        )
        self.content = requests.get(MINIMAL_URL(qid), timeout=5).text
        self.rendered_content = render_problem_content(self.content)
        self.pe_problem_url = PROBLEM_URL(qid)
        self.function_name = (
            self.title.lower().replace(" ", "_").replace("-", "_").replace("'", "")
        )

        # Path for markdown files
        self.summary_md = SUMMARY_MD
        self.problem_md = PROBLEM_MD(qid)
        self.solution_md = SOLUTION_MD(qid)
        self.solution1_md = SOLUTION1_MD(qid)

        # Path for python files
        self.solution1_py = PROBLEM_PY(qid)

    def generate_problem_content(self):
        with open(self.problem_md, "w") as f:
            f.writelines(
                [
                    f"# [{self.title}]({self.pe_problem_url})\n\n",
                    self.rendered_content,
                ]
            )

    def generate_problem_solution1(self):
        with open(self.solution1_md, "w") as f:
            f.write(
                dedent(
                    """
                    # Brute force
                    """
                ).lstrip("\n")
            )

    def generate_problem_solution(self):
        with open(self.solution_md, "w") as f:
            # pylint: disable=trailing-whitespace
            f.write(
                dedent(
                    """
                        # Solution

                        ---

                        > 

                        ---
                    """
                ).lstrip("\n")
            )

    def generate_problem_summary(self):
        with open(self.summary_md, "r") as f:
            summary = f.readlines()

        rm_prefix = lambda s: s.replace(f"{MDBOOK_SRC}/", "")

        summary.insert(
            -2,
            dedent(
                f"""
                    - [Problem {self.id}: {self.title}]({rm_prefix(self.problem_md)})
                        - [Brute force]({rm_prefix(self.solution1_md)})
                        - [Solution]({rm_prefix(self.solution_md)})
                """
            )
            .replace("\n", "\n    ", 3)
            .lstrip("\n"),  # Hack to indent the lines
        )

        with open(self.summary_md, "w") as f:
            f.write("".join(summary))

    def generate_problem_python(self):
        with open(self.solution1_py, "w") as f:
            f.write(
                dedent(
                    f"""
                    def {self.function_name}():
                        pass


                    if __name__ == "__main__":
                        print({self.function_name}())
                    """
                ).lstrip("\n")
            )


def generate_problem(n):
    os.makedirs(MDBOOK_PROBLEM(n))
    os.makedirs(PYTHON_PROBLEM(n))
    problem = Problem(n)
    problem.generate_problem_content()
    problem.generate_problem_solution()
    problem.generate_problem_summary()
    problem.generate_problem_python()
    problem.generate_problem_solution1()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate.py <problem_id>")
        sys.exit(1)
    generate_problem(int(sys.argv[1]))
