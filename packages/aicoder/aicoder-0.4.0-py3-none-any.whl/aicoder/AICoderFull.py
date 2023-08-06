import logging
import colorlog
import json
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from time import sleep
from AICoderPrompts import GET_ALL_FILES, GET_FILE_CONTENTS
from AICoder import AICoder, ALL_IMPORTS, IMPORTS_LOCK

# Set up logging with colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))

# Create a logger for this module
logger = colorlog.getLogger('file_generator')
if not logger.hasHandlers():
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class AICoderFull(AICoder):
    """Class that generates code using OpenAI's API"""
    
    def __init__(self, prompt: str, api_key: str, github_token: str, model: str="gpt-4"):
        super().__init__(prompt, api_key, github_token, model)
    

    def get_files_to_generate(self, extra_content=""):
        """Function that asks the model to return the file names to generate the program"""

        logger.info("Generating list of files...")
        msg = GET_ALL_FILES + extra_content
        files_to_generate = self.contact(msg)
        try:
            # Try to parse the response as JSON
            all_files = json.loads(self.remove_fences(files_to_generate))
        except Exception as e:
            # If parsing fails, try to fix the JSON
            all_files = self.fix_json(msg, files_to_generate, str(e))
        
        # Check for file extension imbalance and file location
        file_extensions = [".h", ".m", ".c", ".cpp"]
        for ext in file_extensions:
            if self.check_file_extension(all_files, ext):
                extra_content = self.generate_extra_content(files_to_generate, ext)
                return self.get_files_to_generate(extra_content=extra_content)
        
        if self.check_file_location(all_files):
            extra_content = self.generate_extra_content(files_to_generate, "/generated/")
            return self.get_files_to_generate(extra_content=extra_content)
        
        return self.confirm_files(all_files)
        
    def check_file_extension(self, all_files, extension):
        # Check if more than 75% of the files have the same extension
        return len([file for file in all_files if file["path"].endswith(extension)]) > len(all_files) * 0.75 and len(all_files) > 3

    def check_file_location(self, all_files):
        # Check if any file is not in the /generated/ directory
        return any("/generated/" not in f["path"] for f in all_files)

    def generate_extra_content(self, files_to_generate, extension):
        # Generate extra content for the next request based on the previous response
        extra_content = "\nLast time I asked your response was:\n" + files_to_generate
        extra_content += "\n\nDon't forget to include the " + ("header" if extension == ".h" else "implementation") + " files."
        return extra_content

    def confirm_files(self, all_files):
        # Confirm the list of files with the user
        print("Files to generate: ", json.dumps(all_files, indent=4))
        print("Is this ok? (Y/n)")
        user_input = input()
        if user_input.lower() in ["no", "n"]:
            print("I'll try to generate the files again... Tell me the problem:")
            extra_content = "\n" + input()
            return self.get_files_to_generate(extra_content=extra_content)
        return all_files

    def wait_on_dependencies(self, file: dict) -> str:
        """Function that waits until all the dependencies are generated"""

        cont = 0
        all_exists = True
        while cont < 50:
            all_exists = self.check_dependencies(file, cont, all_exists)
            if all_exists:
                break
        return self.get_dependencies_content(file)

    def generate_file(self, file: dict, files_to_generate: list, extra_content:str = ""):
        """Function that generates the files given a list of files to generate"""

        global ALL_IMPORTS, IMPORTS_LOCK
        
        file_path = file["path"]
        is_main = "/main." in file["path"]

        # Create the folders
        self.create_folder(file_path)

        # Get the dependencies if not main. Wait until all the dependencies are generated.
        dependencies_content = ""
        if not is_main:
            dependencies_content = self.wait_on_dependencies(file)
        
        # Generate the code
        msg = GET_FILE_CONTENTS.replace("__FILE_PATH__", file_path).replace("__FILES_JSON__", json.dumps(files_to_generate, indent=4)) + dependencies_content + extra_content
        file_content = self.contact(msg, p_info_msg=False)

        # Even if we asked to not return this marks it might return them
        file_content = self.remove_fences(file_content)

        # Check for todos
        if self.check_for_todos(file_content):
            logger.warning(f"Found TODOs in {file_path}")
            return self.generate_file(file=file, files_to_generate=files_to_generate)

        # Ask if main is as expected
        if is_main:
            print("This is the main file content:\n", file_content)
            print("")
            print("Is this ok or where you expecting something different? (Y/n)")
            user_input = input()
            if user_input.lower() in ["no", "n"]:
                print("I'll try to generate the files again... Tell me the problem in one line:")
                extra_content = "\n\nLast time I asked your response was: " + file_content
                extra_content += "\n\n" + input()
                return self.generate_file(file=file, files_to_generate=files_to_generate, extra_content=extra_content)
        
        # Save the file
        self.write_file(file_path, file_content)

        # Get imports
        file_imports = self.extract_imports(file_content)
        if file_imports:
            with IMPORTS_LOCK:
                ALL_IMPORTS[file_path] = file_imports

        return file_content

    def check_dependencies(self, file, cont, all_exists):
        # Check if all dependencies exist
        for dep in file["dependencies"]:
            if not os.path.exists(dep):
                all_exists = False
                logger.info(f"Sleeping from {file['path']} the dependency: {dep}")
                sleep(10)
                if cont > 48:
                    logger.warning(f"The dependency {dep} of {file['path']} doesn't exist.")
                cont += 1
        return all_exists

    def get_dependencies_content(self, file):
        # Get the content of all dependencies
        dependencies_content = ""
        for dep in file["dependencies"]:
            if os.path.exists(dep):
                with open(dep, "r") as f:
                    dependencies_content += "\n\nThis is the content of the dependency file '" + file["path"] + "':\n" + f.read()
        return dependencies_content

    def generate_program(self):
        """Function that generates a full program from 0"""

        # Get files to generate
        files_to_generate = self.get_files_to_generate()

        # Order files to generated from less amount of dependencies to more
        files_to_generate = sorted(files_to_generate, key=lambda x: len(x["dependencies"]))
        
        # Generate main file
        files_to_generate = self.generate_main_file(files_to_generate)
        
        # Initialize a ThreadPoolExecutor and a progress bar
        with tqdm(total=len(files_to_generate[1:]), desc="Generating files", unit="file") as pbar:
            sleep(0.1) #Allow the progress bar to be displayed
            with ThreadPoolExecutor(max_workers=3) as executor: # 3 is ok, don't oversaturate the server
                # Submit tasks to the executor
                futures = {executor.submit(self.generate_file, file, files_to_generate): file for file in files_to_generate[1:]}

                # As the futures complete, update the progress bar
                for future in concurrent.futures.as_completed(futures):
                    # Retrieve the file that this future was associated with
                    file = futures[future]

                    try:
                        # If the future completed without raising an exception,
                        # its result is returned by future.result()
                        future.result()
                    except Exception as exc:
                        logger.error(f"{file} generated an exception: {exc}")
                    else:
                        pbar.update(1)  # update progress bar

        # Try to compile the program
        self.try_to_compile()

        # Try to run the program
        self.try_to_run()

    def generate_main_file(self, files_to_generate):
        # Generate the main file first
        main_file_found = False
        for file in files_to_generate:
            if "/main." in file["path"].lower():
                logger.info("Generating main file...")
                main_file_content = self.generate_file(file, files_to_generate)
                files_to_generate.remove(file)
                file["description"] = file["description"] + "\nMain file content:\n" + main_file_content
                files_to_generate.insert(0, file)
                main_file_found = True
                break
        
        if not main_file_found:
            raise Exception("No main file found")
        return files_to_generate
