import os
import shutil
from pathlib import Path

DELIM = """
--------------------------------------------------------------------------------
"""


class FileManager:
    def __init__(self, project_name=None, sprint_name=None, task_name=None):
        self.project_name = project_name
        self.sprint_name = sprint_name
        self.task_name = task_name

        self._root: Path = Path.home() / os.environ.get("MANA_ROOT", "mana/")

    def __call__(self, obj, data):
        getattr(self, f"use_{obj}")(data)

    def use_dir(self, dirpath: Path):
        if not os.path.exists(dirpath):
            dirpath.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        self.use_dir(self._root)
        return self._root

    @property
    def sprints(self) -> Path:
        self.use_dir(self._root / self.project_name / "sprints")
        return self._root / self.project_name / "sprints"

    @property
    def tasks(self) -> Path:
        self.use_dir(self.sprints / self.sprint_name / "tasks")
        return self.sprints / self.sprint_name / "tasks"

    def clear(self):
        shutil.rmtree(self.root / "")

    def get_data():
        return {}

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
        self.use_dir(self.root / name)
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
        self.project_name = data.get("project__name")
        if not (name := data.get("name")):
            raise ValueError("Missing sprint name")
        info = data.get("info")

        self.clear()

        self.use_dir(self.sprints / name)
        with open(self.sprints / name / f"{name}.md", "w+") as project_file:
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
        self.project_name = data.get("sprint__project__name")
        self.sprint_name = data.get("sprint__name")
        if not (name := data.get("name")):
            raise ValueError("Missing task name")
        info = data.get("info")

        self.use_dir(self.tasks / name)
        with open(self.tasks / name / f"{name}.md", "w+") \
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
