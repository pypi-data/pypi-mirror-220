import os
import ast
import sys
import pymsgbox as msgbox


class SecretChecker:

    def __init__(
            self, 
            secrets=None, 
            file_path=None, 
            folder_name="", 
            env_list=["master", "prod", "production"], 
            button_values = ["OK", "Cancel"], 
            button_cancel_values=["No", "Cancel"],
            env_key_list = ["env", "environment"] 
        ):
        
        self.file_path = file_path
        self.env_list = env_list
        self.button_display_options = button_values
        self.secrets = secrets
        self.button_cancel_values = button_cancel_values

        if self.file_path and not folder_name:
            print("if file path but no folder")
            self._check_secrets_with_specific_values()
        elif secrets:
            print("checking secret value")
            self._go_through_secrets()
        elif not folder_name: 
            print("need to fetch all the files in the current directory")
            self._fetch_all_files_in_same_directory()
        else:
            print("need to fetch all files of a specific folder : ", folder_name)
            self._fetch_all_files_in_folder(folder_name)


    def _go_through_secrets(self):
        for secret in self.secrets:
            secret_val = self.secrets[secret]
            if any(word in str(secret_val).lower() for word in self.env_list):
                self._check_for_secret_values_and_display_prompt(secret, secret_val)
    

    def _fetch_all_files_in_same_directory(self):
        current_directory = os.getcwd()
        files_list = [os.path.join(current_directory, file) for file in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, file))]
        self._iterate_through_files(files_list)
    

    def _fetch_all_files_in_folder(self, folder_name="app"):
        
        current_directory, files_list = os.getcwd(), []

        self.file_path = os.path.join(current_directory, folder_name)

        for root, dirs, files in os.walk(self.file_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")  # Skip files in the __pycache__ directory
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        
        self._iterate_through_files(files_list)

    
    def _iterate_through_files(self, files):

        for file in files:
            self.file_path = file
            self._check_secrets_with_specific_values()


    def _check_secrets_with_specific_values(self):
        
        with open(self.file_path, 'r') as file:
            print("file path : ", self.file_path)
            tree, constants = ast.parse(file.read()), []

            for node in ast.walk(tree):
                if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                    and target.id.isupper()
                ):
                    target = node.targets[0]
                    try:
                        secret_val = ast.literal_eval(node.value)
                    except Exception as e:
                        secret_val = node.value
                    self._check_for_secret_values_and_display_prompt(target.id, secret_val)
                    constants.append(target.id)
    

    def _check_for_secret_values_and_display_prompt(self, key, secret_val):

        if any(word in str(secret_val).lower() for word in self.env_list):
            display_file_data = "found in" + self.file_path if self.file_path else ""
            button_val = msgbox.confirm(f"SECRET {key} = {secret_val} {display_file_data}. Do you wish to continue?", "Accessing ", buttons=self.button_display_options)
        
            if button_val in self.button_cancel_values: sys.exit(1)