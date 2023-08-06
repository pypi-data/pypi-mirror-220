import logging
import colorlog
import openai
import json
import os
import re
import subprocess
from threading import Lock
from AICoderPrompts import PERSONALITY, PROGRAM_TO_GENERATE, FINAL_CLARIFICATIONS, ERROR_FIX, GET_ERRORS_JSON, COMPILATION_COMMAND

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))

logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

ALL_IMPORTS = {}
IMPORTS_LOCK = Lock()

class AICoder():
    """Class that generates code using OpenAI's API"""
    
    def __init__(self, prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
        self.prompt = prompt
        self.api_key = api_key
        self.github_token = github_token
        self.model = model
        self.program_specs = PROGRAM_TO_GENERATE + prompt
        openai.api_key = api_key
    
    def contact(self, prompt: str, p_info_msg: bool = True) -> str:
        """Function that asks the model"""

        if p_info_msg:
            logger.info(f"Asking OpenAI: {prompt[:50]}...")

        messages = [
            {"role": "system", "content": PERSONALITY},
            {"role": "system", "content": self.program_specs},
            {"role": "user", "content": prompt},
            {"role": "system", "content": FINAL_CLARIFICATIONS}
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0
        )

        all_text = response["choices"][0]["message"]["content"]

        return all_text
    

    def remove_fences(self, text: str) -> str:
        """Function that removes code fences from the response"""

        text = text.strip()
        if len(text.split("```")) == 3:
            text = "\n".join(text.split("```")[1].split("\n")[1:])
        
        elif len(text.split("```")) > 3:
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:])
            if text.endswith("```"):
                text = "\n".join(text.split("\n")[:-1])
            
            logger.info(f"The response had more than 3 code fences: " + text)
        
        return text

    def fix_json(self, orig_text: str, orig_response: str, json_error: str) -> str:
        """Function that asks to fix a given json"""

        all_msg = f"{orig_text}\n\n You already gave this reponse:\n{orig_response}\n\nWhich resulted in this error:\n{json_error}\n\nPlease fix it and respond with a valid json."
        response = self.contact(all_msg)
        response = self.remove_fences(response)
        return json.loads(response)

    def check_for_todos(self, text: str) -> bool:
        """Function that checks if the response has TODOs"""

        for line in text.splitlines():
            if re.match(r'[/#\*]\s*todo', line, re.IGNORECASE):
                return True
        return False

    def create_folder(self, file_path: str):
        """Given a file path create all the folders needed using mkdir"""

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    def write_file(self, file_path: str, file_content: str):
        """Given a file path and the content create the file"""

        with open(file_path, "w") as f:
            f.write(file_content)
    
    def extract_imports(self, file_content: str) -> list:
        """Given a file content return a list with all the imports"""

        imports = []
        for line in file_content.split("\n"):
            if re.match(r'^[^\s]*(import|include|require|require_once|include_once|use |from [\w\.]+ import)', line):
                imports.append(line)
            elif re.match(r'=\s+require', line): # const asd, asd2 = require("asd")
                imports.append(line)
        
        # In golang imports are multiline so this function should also be able to find those imports. Example: import (\n"fmt"\n"math"
        pattern = r'import\s*\((.*?)\)'
        multiline_imports = re.findall(pattern, file_content, re.DOTALL)
        for multiline_import in multiline_imports:
            imports.append(multiline_import)
        
        return imports

    def try_to_compile(self):
        """Function that tries to compile the program"""

        global ALL_IMPORTS

        msg_imports = f"These are all the imports files are using: {json.dumps(ALL_IMPORTS, indent=4)}\n\n"
        compilation_command = self.contact(COMPILATION_COMMAND + "\n\n" + msg_imports)
        compilation_command = self.remove_fences(compilation_command)
        compilation_command = json.loads(compilation_command)["command"]

        if not compilation_command:
            logger.info("The program doesn't need to be compiled")
            return

        print("This is the compilation command: ", compilation_command)
        print("Is this ok? If not, you will be asked for a command (Y/n)")
        user_input = input()
        if user_input.lower() in ["no", "n"]:
            print("Ok, do you want to indicate a compilation command? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                logger.info("Ok, the program won't be compiled")
                return
            
            else:
                print("Indicate the compilation command in 1 line:")
                compilation_command = input()
        
        # Compile the program
        print(f"Do you want to run: '{compilation_command}' ? (Y/n)")
        user_input = input()
        if user_input.lower() in ["no", "n"]:
            logger.info("Ok, the program won't be compiled")
            return
        else:
            self.fix_errors_per_file_auto(compilation_command)


    def fix_errors_per_file_auto(self, command_to_run):
        """Function that ask the model to fix the errors per file after running a command"""

        # execute getting the stdout and stderr
        logger.info(f"Running '{command_to_run}' ...")
        process = subprocess.Popen(command_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

        # Print the results
        logger.info(f"[+] stdout: {stdout}\n")
        logger.info("====================================")
        print()
        logger.warning(f"[+] stderr: {stderr}\n")

        if not stderr:
            logger.info("No errors found, the program should work now!")
            return

        # Get errors organized
        msg = GET_ERRORS_JSON.replace("__RAW_ERRORS__", stderr).replace("__COMMAND__", command_to_run)
        errors = self.contact(msg)
        errors = self.remove_fences(errors)
        try:
            errors = json.loads(errors)
        except Exception as e:
            errors = self.fix_json(msg, errors, str(e))

        # Remove empty errors
        for err in errors:
            if not err["errors_text"]:
                errors.remove(err)
        
        # Errors found
        logger.info("These are the errors found:")
        print(json.dumps(errors, indent=4))

        for err in errors:
            # Get the file path
            file_path = err["file_path"]
            logger.info(f"Fixing errors in {file_path} ...")

            # Ask user if he wants to fix the errors
            print("Do you want to fix that errors? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                logger.info("Ok, not fixing that file")
                continue

            # Get the file content
            with open(file_path, "r") as f:
                file_content = f.read()

            err_text = "\n".join(err["errors_text"])
            
            # Fix the errors
            fixed_content = self.contact(ERROR_FIX.replace("__FILE_PATH__", file_path).replace("__ERROR_TEXT__", err_text).replace("__FILE_CONTENT__", file_content))
            self.write_file(file_path, fixed_content)

        if errors:
            # Ask the user if he wants to try to compile again
            print("Do you want to try to compile again? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                logger.info("Ok, not trying to compile again")
            else:
                return self.fix_errors_per_file_auto(command_to_run)
            
            self.fix_errors_per_file_manual(command_to_run)

    
    def fix_errors_per_file_manual(self, command_to_run):
        """Function that ask the model to fix the errors per file manually"""

        logger.info("Let's fix the errors manually")
        print("Do you want to fix anything else? (y/N)")
        user_input = input()
        if not user_input.lower() in ["yes", "y"]:
            logger.info("Ok, not fixing anything else. Hopefully the program will work now!")
        
        else:
            file_path = ""
            while not os.path.exists(file_path):
                # Ask for the file path to fix
                print("Indicate the file path to fix (it must exist):")
                file_path = input()
            
            with open(file_path, "r") as f:
                file_contents = f.read()
            
            # Ask for the error(s) to fix
            print("Indicate the error(s) to fix (copy paste from the output):")
            err_lines = []
            while True:
                line = input()
                if line:
                    err_lines.append(line)
                else:
                    break
            err_text = '\n'.join(err_lines)

            # Ask for the fix
            logger.info("Asking for the fix...")
            fixed_content = self.contact(ERROR_FIX.replace("__FILE_PATH__", file_path).replace("__ERROR_TEXT__", err_text).replace("__FILE_CONTENT__", file_contents))
            self.write_file(file_path, fixed_content)

            # Ask user to restart automatic fixing or manual fixing or finish
            print("Do you want to retry the compilation? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                logger.info("Ok, the program won't be compiled")
                return
            
            self.fix_errors_per_file_auto(command_to_run)


    def try_to_run(self):
        """Function that tries to run the program"""

        # Ask if the user whish to run the program
        print("Do you want to try to run the program? (Y/n)")
        user_input = input()
        if user_input.lower() in ["no", "n"]:
            logger.info("Ok, the program won't be run")
        
        else:
            # Ask for the command to run
            print("Indicate the command to run in 1 line:")
            command_to_run = input()

            # Execute getting the stdout and stderr
            self.fix_errors_per_file_auto(command_to_run)
