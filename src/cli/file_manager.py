import os
import shutil
from pathlib import Path

DELIM = """
--------------------------------------------------------------------------------
"""


class FileManager:
    def __init__(self):
        self._root: Path = Path.home() / os.environ.get("MANA_ROOT", "mana/")

    def __call__(self, obj, data):
        getattr(self, f"use_{obj}")(data)

    @property
    def root(self):
        if not os.path.exists(self._root):
            os.mkdir(self._root)
        return self._root

    def clear(self):
        shutil.rmtree(self.root / "")

    def make_header(
        self,
        name: str,
        state: str,
        owner: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> str:
        string = f"# {name}\n"
        string += f"## {state}\n"
        string += f"### {owner}\n"
        if start_date and end_date:
            string += f"####{start_date} - {end_date}\n"
        return string

    def format_comment(self, comment: str) -> str:
        return f"""
{DELIM}
{comment.get("user__username")}@{comment.get("created_at")}

{comment.get("text")}

"""

    def use_project(self, data: dict):
        if not (name := data.get("name")):
            raise ValueError("Missing project name")
        info = data.get("info")

        self.clear()
        os.mkdir(self.root / name)
        with open(self.root / name / f"{name}.md", "w+") as project_file:
            project_file.write(self.make_header(
                name,
                data.get("state", "(Draft)"),
                data.get("owner__name"),
                data.get("start_date"),

            ))
            project_file.write(DELIM)
            project_file.write(f"\n{info}")
            for comment in data.get("comments", []):
                project_file.write(self.format_comment(comment))

    def use_sprint(self, data: dict):
        if not (name := data.get("name")):
            raise ValueError("Missing sprint name")
        info = data.get("info")

        self.clear()
        os.mkdir(self.root / "sprints" / name)
        with open(self.root / "sprints" / name / f"{name}.md", "w+") as project_file:
            project_file.write(self.make_header(
                name,
                data.get("state", "(Draft)"),
                data.get("owner__name"),
                data.get("start_date"),

            ))
            project_file.write(DELIM)
            project_file.write(f"\n{info}")
            for comment in data.get("comments", []):
                project_file.write(self.format_comment(comment))

    def use_task(self, data: dict):
        if not (name := data.get("name")):
            raise ValueError("Missing task name")
        info = data.get("info")

        self.clear()
        os.mkdir(self.root / "sprints" / data.get("sprint__name") / "tasks" / name)
        with open(self.root / "sprints" / data.get("sprint__name") / "tasks" / name / f"{name}.md", "w+") \
                as project_file:
            project_file.write(self.make_header(
                name,
                data.get("state", "(Draft)"),
                data.get("owner__name"),
                data.get("start_date"),

            ))
            project_file.write(DELIM)
            project_file.write(f"\n{info}")
            for comment in data.get("comments", []):
                project_file.write(self.format_comment(comment))
