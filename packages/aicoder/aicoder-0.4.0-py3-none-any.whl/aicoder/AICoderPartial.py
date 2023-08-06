import logging
from typing import List
import colorlog
import subprocess
import os
from time import sleep
from github import Github
from AICoderPrompts import MODIFY_FILE, FILE_FROM_TEMPALTES, ASK_FOR_FILE
from AICoder import AICoder

# Setting up logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))

logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class AICoderPartial(AICoder):
    """Class that generates code using OpenAI's API"""
    
    def __init__(self, prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
        super().__init__(prompt, api_key, github_token, model)


    def modify_file(self, file_path: str, prompt: str, orig_branch: str, to_branch: str, repo_name:str):
        """Function that modifies a file based on the prompt and creates a PR with the changes"""

        if orig_branch:
            self.change_branch(orig_branch)

        # Prepare message
        logger.info(f"Modifying file {file_path}...")
        with open(file_path, "r") as f:
            file_content = f.read()
        msg = MODIFY_FILE.replace("__FILE_PATH__", file_path).replace("__PROMPT__", prompt).replace("__FILE_CONTENT__", file_content)

        # Get new content
        new_content = self.contact(msg)
        new_content = self.remove_fences(new_content)

        # Write new content
        with open(file_path, "w") as f:
            f.write(new_content)
        
        # If branch, create PR
        if orig_branch and repo_name:
            commit_msg = f"File {os.path.basename(file_path)} modified by AICoder"
            commit_body = f"AICoder modified the file {file_path} according to this input:\n{prompt}"
            self.create_pull_request(commit_msg, commit_body, orig_branch, to_branch, repo_name)

    def gen_file_from_templates(self, template_file_paths: List[str], final_file_path: str, prompt: str, orig_branch: str, to_branch: str, repo_name:str):
        """Function that generates a file from a template"""

        if orig_branch:
            self.change_branch(orig_branch)

        # Create needed folders
        self.create_folder(final_file_path)

        # Prepare message
        logger.info(f"Generating {final_file_path} file from templates {', '.join(template_file_paths)}...")
        msg = FILE_FROM_TEMPALTES.replace("__FINAL_FILE_PATH__", final_file_path).replace("__PROMPT__", prompt)
        for f_path in template_file_paths:
            with open(f_path, "r") as f:
                f_path_content = f.read()
                msg += f"\nThe template file {f_path} has the following content:\n\n{f_path_content}\n\n"
        
        # Get new content
        new_content = self.contact(msg)
        new_content = self.remove_fences(new_content)

        # Write new content
        with open(final_file_path, "w") as f:
            f.write(new_content)

        # If branch, create PR
        if orig_branch and repo_name:
            commit_msg = f"File {os.path.basename(final_file_path[:46])} created by AICoder"
            commit_body = f"AICoder created the file {final_file_path} based on the files {', '.join(template_file_paths)} according to this input:\n{prompt}"
            self.create_pull_request(commit_msg, commit_body, orig_branch, to_branch, repo_name)


    def change_branch(self, orig_branch: str):
        """Function that changes the branch"""

        # Set git user.name and user.email if they are not set
        subprocess.run(["git", "config", "user.name", "aicoder"], check=True)
        subprocess.run(["git", "config", "user.email", "aicoder@aicoderhub.ai"], check=True)

        # Fetch the remote branches
        subprocess.run(["git", "fetch"], check=True)

        # Check if the branch exists locally
        result = subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{orig_branch}"])

        if result.returncode != 0:
            # The branch does not exist locally, so create it
            subprocess.run(["git", "checkout", "-b", orig_branch], check=True)
            logger.info(f"Branch {orig_branch} created")

            # Check if the branch exists remotely
            result = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", orig_branch])
            if result.returncode == 0:
                # The branch exists remotely, so set up tracking and pull the latest changes
                subprocess.run(["git", "branch", "--set-upstream-to", f"origin/{orig_branch}", orig_branch], check=True)
                subprocess.run(["git", "config", "pull.rebase", "false"], check=True)
                subprocess.run(["git", "pull", "--no-edit"], check=True)
                logger.info(f"Downloaded the latest changes from branch {orig_branch}")
        else:
            # The branch exists locally, so check it out and pull the latest changes
            subprocess.run(["git", "checkout", orig_branch], check=True)
            subprocess.run(["git", "config", "pull.rebase", "false"], check=True)
            subprocess.run(["git", "pull", "--no-edit"], check=True)
            logger.info(f"Branch {orig_branch} checked out and updated")



    def create_pull_request(self, commit_message: str, commit_body: str, orig_branch: str, to_branch: str, repo_name: str):
        """Function that creates a pull request"""

        github = Github(self.github_token)
        repo = github.get_repo(repo_name)

        # Set git user.name and user.email if they are not set
        subprocess.run(["git", "config", "user.name", "aicoder"], check=True)
        subprocess.run(["git", "config", "user.email", "aicoder@aicoderhub.ai"], check=True)

        # Commit changes to the new branch
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message[:70]], check=True)

        # Get the HTTPS URL of the origin remote, and replace "https://" with "https://token@"
        origin_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).strip().decode()
        new_origin_url = origin_url.replace("https://", f"https://{self.github_token}@")
        
        # Push the changes
        push_result = subprocess.run(["git", "push", "--set-upstream", new_origin_url, orig_branch], text=True, capture_output=True)
        if push_result.returncode != 0:
            print(f"Failed to push the changes to the origin {new_origin_url}: ", push_result.stderr)
            return

        # Create a pull request
        sleep(1)
        logger.info(f"Creating a pull request to repo {repo_name}, from branch {orig_branch} to branch {to_branch}...")
        pr = repo.create_pull(
            title=commit_message,
            body=commit_body,
            head=orig_branch,
            base=to_branch
        )

        logger.info(f"Pull request created: {pr.html_url}")

        # Set the origin URL back to the original URL
        push_result = subprocess.run(["git", "push", "--set-upstream", origin_url, orig_branch], text=True, capture_output=True)
