import os

class Utils:
    @staticmethod
    def change_to_father_directory():
        original_directory = os.getcwd()
        print("Original working directory:", original_directory)
        os.chdir("..")
        updated_directory = os.getcwd()
        print("Updated working directory:", updated_directory)
        return original_directory
    
    @staticmethod
    def change_to_directory(directory):
        return os.chdir(directory)

