from typing import Any, Dict, List, Union

from jinja2 import (
    Template,
    Environment,
    PackageLoader,
    select_autoescape,
    TemplateNotFound,
    TemplateError,
    TemplateRuntimeError,
)

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.git import Git
from lupin_grognard.core.tools.utils import die, info, write_file


class Changelog:
    def __init__(self, commit_list: List[str]):
        self.commit_list = commit_list
        self.git = Git()

    def generate(self) -> None:
        """Generate changelog"""
        project_url = self.git.get_remote_origin_url()
        project_name = self._get_project_name(project_url=project_url)
        info(msg=f"Collecting data from {project_name}")
        classified_commits = self._classify_commits()
        self._generate_markdown_file(
            classified_commits=classified_commits,
            project_name=project_name,
            project_url=project_url,
        )

    def _get_project_name(self, project_url) -> str:
        """Get project name from project url"""
        return project_url.split("/")[-1]

    def _get_local_template(self) -> Template:
        try:
            env = Environment(
                loader=PackageLoader("lupin_grognard", "templates"),
                autoescape=select_autoescape(),
                trim_blocks=True,  # Removes unnecessary spaces before and after blocks and loop
                lstrip_blocks=True,  # Removes unnecessary spaces before blocks and loop
            )
            return env.get_template("changelog.j2")
        except TemplateNotFound:
            die(msg="Template 'lupin_grognard/templates/changelog.j2' not found")

    def _generate_markdown_file(
        self,
        classified_commits: Dict,
        project_name: str,
        project_url: str,
    ) -> None:
        """Generate changelog markdown file from template with version and commits"""
        template = self._get_local_template()
        context = {
            "tree": classified_commits,
            "project_name": project_name,
            "project_url": project_url,
        }
        info(msg="Generating changelog file from lupin_grognard/templates/changelog.j2")
        try:
            markdown_str = template.render(context)
        except (TemplateError, TemplateRuntimeError) as e:
            die(msg=f"Error rendering Jinja2 template: {e}")
        write_file(file="CHANGELOG.md", content=markdown_str)
        info(msg="Changelog file generated")

    def _classify_commits(self) -> List[Dict[str, Any]]:
        """
        Classify commits by version and by type and scope
        Returns:
            ListList[Dict[str, Any]]: List of version with commits classified by type and scope

            Example:
            [
                {
                    "version": "v1.0.0",
                    "date": "2020-02-20",
                    "commits": {
                        "feature": {
                            "added": [
                                "Add new feature",
                            ],
                            "changed": [
                                "change new feature",
                            ],
                            "removed": [
                                "remove new feature",
                            ],
                        },
                        "fix": [
                            "Fix bug",
                        ],
                        "other": [
                            "add README.md",
                        ],
                    },
                },
            ]
        """
        versioned_commits = self._classify_commits_by_version()
        for v in versioned_commits:
            classified_commits = self._classify_commits_by_type_and_scope(v["commits"])
            v["commits"] = classified_commits
        self._display_number_of_commits_found_for_changelog(
            versioned_commits=versioned_commits
        )
        return versioned_commits

    def _classify_commits_by_version(self) -> List[Dict[str, List[Commit]]]:
        versions = []
        current_version = {}
        tag_list = self.git.get_tags()
        for c in self.commit_list:
            commit = Commit(c)
            for tag in tag_list:
                if commit.hash in tag[1]:
                    info(msg=f"Found tag {tag[0]}")
                    commit_tag = tag[0]
                    date_tag = tag[2]
                    if current_version:
                        versions.append(current_version)
                    current_version = {
                        "version": commit_tag,
                        "date": date_tag,
                        "commits": [],
                    }
                    current_version["commits"].append(commit)
                    break
            else:
                if not current_version:
                    current_version = {
                        "version": "Unreleased",
                        "date": "",
                        "commits": [],
                    }
                current_version["commits"].append(commit)
        if current_version:
            versions.append(current_version)
        return versions

    def _get_parents_hash_and_close_issues_for_commit(
        self, commit: Commit
    ) -> Union[List, List]:
        """Get parents and close issues for commit

        Args:
            commit (Commit): Commit object

            Returns:
                Union[List, List]: List of parents without index 0 and list of close issues"""
        parents_hash = commit.parents[1:]
        close_issues = commit.closes_issues if commit.closes_issues else []
        return parents_hash, close_issues

    def _is_commit_related_to_closed_issue(
        self, commit: Commit, commit_parents: List, close_issues: List
    ) -> bool:
        for index, hash in enumerate(commit_parents):
            if hash == commit.hash:
                if close_issues:
                    return close_issues[index]
        return ""

    def _append_title_with_matched_issue_for_feat_and_fix_type(
        self, commits: List[str], commit: Commit, match_issue: str
    ) -> None:
        """Append commit without type scope with matched issue for commit type feat and fix"""
        url = self.git.get_remote_origin_url()
        url_issue = (
            f"[#{match_issue}]({url}/-/issues/{match_issue})" if match_issue else ""
        )
        commits.append(f"{commit.title_without_type_scope} {url_issue}")

    def _append_title_with_matched_issue_for_other_type(
        self, commits: List[str], commit: Commit, match_issue: str
    ) -> None:
        """Append commit with type and matched issue for other commit type"""
        url = self.git.get_remote_origin_url()
        url_issue = (
            f"[#{match_issue}]({url}/-/issues/{match_issue})" if match_issue else ""
        )
        commits.append(f"{commit.title} {url_issue}")

    def _classify_commits_by_type_and_scope(
        self, commits: List[Commit]
    ) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
        """Classify commits by type and scope and exclude merge commits"""
        commits_feat_add, commits_feat_change, commits_feat_remove = [], [], []
        commits_fix, commits_other = [], []
        commit_parents, close_issues, match_issue = "", "", ""

        for commit in commits:
            if commit.title.startswith("Merge"):
                (
                    commit_parents,
                    close_issues,
                ) = self._get_parents_hash_and_close_issues_for_commit(commit=commit)
            if commit_parents:
                match_issue = self._is_commit_related_to_closed_issue(
                    commit=commit,
                    commit_parents=commit_parents,
                    close_issues=close_issues,
                )
            match (commit.type, commit.scope):
                case ("feat", "(add)"):
                    self._append_title_with_matched_issue_for_feat_and_fix_type(
                        commits=commits_feat_add, commit=commit, match_issue=match_issue
                    )
                case ("feat", "(change)"):
                    self._append_title_with_matched_issue_for_feat_and_fix_type(
                        commits=commits_feat_change,
                        commit=commit,
                        match_issue=match_issue,
                    )
                case ("feat", "(remove)"):
                    self._append_title_with_matched_issue_for_feat_and_fix_type(
                        commits=commits_feat_remove,
                        commit=commit,
                        match_issue=match_issue,
                    )
                case ("fix", None):
                    self._append_title_with_matched_issue_for_feat_and_fix_type(
                        commits=commits_fix, commit=commit, match_issue=match_issue
                    )
                case (_, _) if commit.type is not None:
                    self._append_title_with_matched_issue_for_other_type(
                        commits=commits_other, commit=commit, match_issue=match_issue
                    )
        return self._create_commit_dict(
            commits_feat_add=commits_feat_add,
            commits_feat_change=commits_feat_change,
            commits_feat_remove=commits_feat_remove,
            commits_fix=commits_fix,
            commits_other=commits_other,
        )

    def _create_commit_dict(
        self,
        commits_feat_add: List[str],
        commits_feat_change: List[str],
        commits_feat_remove: List[str],
        commits_fix: List[str],
        commits_other: List[str],
    ) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
        result = {}
        if commits_feat_add or commits_feat_change or commits_feat_remove:
            result["feature"] = {}
            if commits_feat_add:
                result["feature"]["added"] = commits_feat_add
            if commits_feat_change:
                result["feature"]["changed"] = commits_feat_change
            if commits_feat_remove:
                result["feature"]["removed"] = commits_feat_remove
        if commits_fix:
            result["fix"] = commits_fix
        if commits_other:
            result["other"] = commits_other
        return result

    def _display_number_of_commits_found_for_changelog(
        self, versioned_commits: List[Dict[str, List[str]]]
    ) -> None:
        total = 0
        for v in versioned_commits:
            total += len(v.get("commits", {}).get("feature", {}).get("added", []))
            total += len(v.get("commits", {}).get("feature", {}).get("changed", []))
            total += len(v.get("commits", {}).get("feature", {}).get("removed", []))
            total += len(v.get("commits", {}).get("fix", []))
            total += len(v.get("commits", {}).get("other", []))
        info(msg=f"Found {total} commits")
