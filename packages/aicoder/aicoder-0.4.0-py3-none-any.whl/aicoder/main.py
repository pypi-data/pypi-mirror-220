import argparse
import os
import sys
import string
import random
import requests
import logging
import colorlog
import subprocess
from concurrent.futures import ThreadPoolExecutor
from aicoder.AICoderFull import AICoderFull
from aicoder.AICoderPartial import AICoderPartial

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))
logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def is_git_repo():
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def full_generator(prompt: str, api_key: str, model: str="gpt-4"):
    if os.path.isdir("generated"):
        os.system("rm -rf generated")
    aicoderfull = AICoderFull(prompt, api_key, "", model)
    aicoderfull.generate_program()

def file_generator(prompt: str, api_key: str, github_token: str, model: str, template_files: list, final_file_path: str, orig_branch: str, to_branch: str, repo_name: str):
    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.gen_file_from_templates(template_files, final_file_path, prompt, orig_branch, to_branch, repo_name)

def enhancer(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    aicoderpartial = AICoderPartial(prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, prompt, orig_branch, to_branch, repo_name)

def add_comments(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    final_prompt = "Given some code, add useful comments to it inside the code to easily understand what it does."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, to_branch, repo_name)

def check_security(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    final_prompt = "Given some code, search for security vulnerabilities and potential backdoors on it and if any, create a new code fixing it (if possible). Return only the fixed code with the comments. If you changed anything, add at the end of the code comments explaining the changes."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, to_branch, repo_name)

def optimize_file(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    final_prompt = "Given some code, optimize it without loosing functionality. Return a code that keeping the same functionality and respecting the class and function names, it's more clean and beautiful, simple, don't have duplice code, don't have code smells and is more efficient if possible. "
    final_prompt += "Don't remove comments, just improve them if possible. If you cannot improve the code just return the same code. If you changed anything, add at the end of the code comments explaining the changes. "
    final_prompt += "Be careful with chunks of code that looks similar but aren't exactly the same, even if part of the code can be improved the different functionalities must be keeped."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, to_branch, repo_name)

def fix_bugs(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    final_prompt = "Given some code and keeping the same functionality fix all the bugs in it. Also, don't remove comments, just improve them if possible."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, to_branch, repo_name)

def todoer(prompt: str, api_key: str, github_token: str, model: str, file_path: list, orig_branch: str, to_branch: str, repo_name: str):
    final_prompt = "Given some code, check all the TODOs and remove them adding the code that performs the functionality mentioned inside the TODO comment. If you need more information about any TODO, ask for more information inside the TODO comment and leave the comment in the code."
    if prompt:
        final_prompt = "\n" + prompt
    aicoderpartial = AICoderPartial(final_prompt, api_key, github_token, model)
    aicoderpartial.modify_file(file_path, final_prompt, orig_branch, to_branch, repo_name)

def add_common_arguments(parser):
    parser.add_argument('--api-key', default=None, type=str, help='Input API key')
    parser.add_argument('--model', default="gpt-4", type=str, help='Model to use')
    parser.add_argument('--prompt', default=None, type=str, help='Input prompt. It can be string, a file path or a url.')

def get_git_org_repo_name():
    command = ['bash', '-c', 'git config --get remote.origin.url | sed -nE \'s/.*github.com[:\/]([^\/]*)\/(.*)\.git/\\1\\/\\2/p\'']
    return subprocess.check_output(command).strip().decode()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")  

    full_generator_parser = subparsers.add_parser('full-generator', help='Generate a full program from the prompt.')
    file_generator_parser = subparsers.add_parser('file-generator', help='Generate a file based on others as templates.')
    file_enhancer_parser = subparsers.add_parser('file-enhancer', help='Enhance a file based on the given prompt.')
    file_commentor_parser = subparsers.add_parser('file-comments', help='Ask to add comments to a file.')
    file_security_parser = subparsers.add_parser('file-security', help='Ask to search security vulnerabilities and backdoors in a file.')
    file_optimizer_parser = subparsers.add_parser('file-optimizer', help='Ask to optimize a file in terms of clean code and efficiency.')
    file_bug_fixer_parser = subparsers.add_parser('file-bugfixer', help='Ask to fix bugs in a file.')
    file_todoer_parser = subparsers.add_parser('file-todoer', help='Ask to complete the TODOs inside the code.')

    for subparser in [full_generator_parser, file_generator_parser, file_enhancer_parser, file_commentor_parser, file_security_parser, file_optimizer_parser, file_bug_fixer_parser, file_todoer_parser]:
        add_common_arguments(subparser)

    file_generator_parser.add_argument('--template-files', type=str, help='Comma separated list of template files')
    file_generator_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_generator_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_generator_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_generator_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    file_generator_parser.add_argument('--file-path', default=None, type=str, help='File path to generate')
    
    file_enhancer_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to enhance')
    file_enhancer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_enhancer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_enhancer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_enhancer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_commentor_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to add comments')
    file_commentor_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_commentor_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_commentor_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_commentor_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    file_security_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to search vulnerabilities')
    file_security_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_security_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_security_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_security_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    file_security_parser.add_argument('--only-ask', default=None, type=str, help='Indicate that you only want to ask for security problems, not to change the code.')
    
    file_optimizer_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to optimize')
    file_optimizer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_optimizer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_optimizer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_optimizer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    file_optimizer_parser.add_argument('--only-ask', default=None, type=str, help='Indicate that you only want to ask for optimizations, not to change the code.')

    file_bug_fixer_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to fix bugs')
    file_bug_fixer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_bug_fixer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_bug_fixer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_bug_fixer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    file_bug_fixer_parser.add_argument('--only-ask', default=None, type=str, help='Indicate that you only want to ask for the bugs, not fix them.')

    file_todoer_parser.add_argument('--paths', type=str, help='Comma separated list of file paths to complete TODOs')
    file_todoer_parser.add_argument('--github-token', default=None, type=str, help='Github token')
    file_todoer_parser.add_argument('--orig-branch', default=None, type=str, help='Branch to upload the changes.')
    file_todoer_parser.add_argument('--to-branch', default=None, type=str, help='Branch to send the PR to.')
    file_todoer_parser.add_argument('--repo-name', default=None, type=str, help='Indicate the name of the repo: org_name/repo_name')
    
    args = parser.parse_args()
    prompt = os.environ.get("INPUT_PROMPT") or (args.prompt if hasattr(args,"prompt") else None)
    api_key = os.environ.get("INPUT_OPENAI_API_KEY") or (args.api_key if hasattr(args,"api_key") else None)
    model = os.environ.get("INPUT_MODEL") or (args.model if hasattr(args,"model") else None)
    github_token = os.environ.get("GITHUB_TOKEN")

    if args.mode in ["file-generator", "file-enhancer", "file-comments", "file-security", "file-optimizer", "file-bugfixer", "file-todoer"]:
        github_token = os.environ.get("GITHUB_TOKEN") or args.github_token
        orig_branch = os.environ.get("ORIGIN_BRANCH") or args.orig_branch
        to_branch = os.environ.get("TO_BRANCH") or args.to_branch
        repo_name = os.environ.get("GITHUB_REPOSITORY") or args.repo_name or get_git_org_repo_name()

        if args.mode == "file-generator":
            template_files = os.environ.get("TEMPLATE_FILES") or args.template_files
            template_files = list(template_files.strip().split(","))
            final_file_path = os.environ.get("FINAL_FILE_PATH") or args.file_path
            if not template_files or not final_file_path:
                logger.error("Error: Missing template_files or final_file_path.")
                parser.print_help()
                sys.exit(1)
                
        elif args.mode in ["file-enhancer", "file-comments", "file-security", "file-optimizer", "file-bugfixer", "file-todoer"]:
            check_paths = os.environ.get("CHECK_PATHS") or args.paths
            check_paths = list(check_paths.split(","))
            if not check_paths:
                logger.error("Error: Missing check_paths.")
                parser.print_help()
                sys.exit(1)
            
    if not prompt and not args.mode in ["file-comments", "file-security", "file-optimizer", "file-bugfixer", "file-todoer"]:
        logger.error("Error: Missing prompt.")
        parser.print_help()
        sys.exit(1)
    
    if not api_key:
        logger.error("Error: Missing API key.")
        parser.print_help()
        sys.exit(1)
    
    if prompt and os.path.isfile(prompt):
        logger.info(f"Prompt read from {prompt}")
        with open(prompt, "r") as f:
            prompt = f.read()
    
    elif prompt and prompt.startswith("http"):
        logger.info(f"Prompt downloaded from {prompt}")
        prompt = requests.get(prompt).text
    
    if args.mode == 'full-generator':
        full_generator(prompt, api_key, model)
        exit(0)
    
    if not github_token:
        logger.warning("No Github token. PRs cannot be created automatically.")
    
    if github_token and not is_git_repo():
        logger.error("Error: Current directory isn't a git repository. Stopping.")
        exit(1)
    
    if github_token and not orig_branch:
        logger.error("Error: No orig branch. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    if github_token and not to_branch:
        logger.error("Error: No to branch. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    if github_token and not repo_name:
        logger.error("Error: No repo name. PRs cannot be created automatically. Stopping.")
        exit(1)
    
    elif args.mode == 'file-generator':
        file_generator(prompt, api_key, github_token, model, template_files, final_file_path, orig_branch, to_branch, repo_name)
        exit(0)
    
    elif args.mode in ['file-enhancer', 'file-comments', 'file-security', 'file-optimizer', 'file-bugfixer', 'file-todoer']:
        if args.mode == 'file-enhancer':
            f = enhancer
        elif args.mode == 'file-comments':
            f = add_comments
        elif args.mode == 'file-security':
            f = check_security
        elif args.mode == 'file-optimizer':
            f = optimize_file
        elif args.mode == 'file-bugfixer':
            f = fix_bugs
        elif args.mode == 'file-todoer':
            f = todoer
        
        for file_path in check_paths:
            if os.path.isfile(file_path):
                logger.info(f"Given path {file_path} is a file.")
                f(prompt, api_key, github_token, model, file_path, orig_branch, to_branch, repo_name)
        
            elif os.path.isdir(file_path):
                logger.info(f"Given path {file_path} is a folder.")
                with ThreadPoolExecutor(max_workers=3) as executor:
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            logger.info(f"Checking file: {file_path}")
                            executor.submit(f, prompt, api_key, github_token, model, os.path.join(root, file), orig_branch, to_branch, repo_name)
            else:
                logger.error(f"Given path {file_path} is neither a file nor a folder.")

        exit(0)

if __name__ == "__main__":
    main()