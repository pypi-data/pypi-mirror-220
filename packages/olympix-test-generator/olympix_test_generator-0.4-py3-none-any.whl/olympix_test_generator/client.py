import requests
import argparse
import os
from dotenv import load_dotenv
import inquirer

BASE_URL = 'https://generate-sol-tests.olympixdevsectools.com'  # Flask runs on port 5000 by default

# Declare global variables
file_content = ""
contract_name = ""
function_name = ""
opix_api_key = ""

def get_opix_api_key() -> bool:
    global opix_api_key  # Use global variable

    opix_api_key = os.getenv('OLYMPIX_API_KEY')
    if opix_api_key is None:
        print("'OLYMPIX_API_KEY' not found.")
        return False
    else:
        select_sol_file()
        return True

def select_sol_file():
    global file_content, contract_name, function_name  # Use global variables

    # Get a list of all .sol files and directories in the current directory
    files_and_dirs = [f for f in os.listdir() if f.endswith('.sol') or os.path.isdir(f)]
    files_and_dirs.append('..')  # Add option to go up one directory

    # Define the questions
    questions = [
        inquirer.List('file',
                      message="Select a .sol file or a directory",
                      choices=files_and_dirs,
                      ),
    ]

    # Get the user's answer
    answers = inquirer.prompt(questions)

    # If a directory is selected, change the current directory and call this function again
    if os.path.isdir(answers['file']):
        os.chdir(answers['file'])
        select_sol_file()
    elif answers['file'] == '..':
        os.chdir('..')
        select_sol_file()
    else:
        # Print the selected file
        print(f"You selected {answers['file']}")
        with open(answers['file'], 'r') as f:
            file_content = f.read()
        contract_name = input("Enter the name of the contract to test: ")
        function_name = input("Enter the name of the function to test: ")

def main():
    parser = argparse.ArgumentParser(description='Generate a test contract for a given smart contract')
    subparsers = parser.add_subparsers(dest='command')

    # add commands
    generate_parser = subparsers.add_parser('generate')

    args = parser.parse_args()

    if args.command == 'generate':
        found_key = get_opix_api_key()
        if not found_key:
            exit(1)
        
        print("Generating test contract. This may take a few seconds...")
        headers = {
            'Authorization': f'Bearer {opix_api_key}'
        }

        data = {
            'file_content': file_content, 
            'contract_name': contract_name, 
            'function_name': function_name
            }

        response = requests.post(f'{BASE_URL}/generate', headers=headers, json=data)
        if response.json()['is_authenticated'] == False:
            print("Invalid API Key")
            exit(1)
        print(response.json()['test'])

if __name__ == "__main__":
    main()
