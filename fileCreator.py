import os
import argparse
import getpass

def get_input(prompt):
    return input(prompt).strip()

def main():
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--filename', type=str, help='The name of the file')
    parser.add_argument('--server', type=str, help='The server address')
    parser.add_argument('--username', type=str, help='The username')
    parser.add_argument('--outputPath', type=str, help='The output path')

    args = parser.parse_args()

    filename = args.filename or get_input('Enter filename: ')
    server = args.server or get_input('Enter server: ')
    username = args.username or get_input('Enter username: ')
    outputPath = args.outputPath or get_input('Enter output path (leave blank for current directory): ')

    if not outputPath:
        outputPath = os.path.dirname(os.path.abspath(__file__))

    if not outputPath.endswith(os.sep):
        outputPath += os.sep

    password = getpass.getpass('Enter password: ')

    command = f'python script.py {outputPath}{filename}_key.properties {outputPath}{filename}_enc.properties {server} {username} {password}'
    os.system(command)

if __name__ == '__main__':
    main()
