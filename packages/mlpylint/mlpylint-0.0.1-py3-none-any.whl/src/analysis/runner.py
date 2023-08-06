import argparse
import os
import time

import astroid

from src.analysis.argument import REGISTERED_CHECKERS, REGISTERED_CHECKERS_ADVICE, ArgumentConfig
from src.analysis.config import ColorConfig
from src.analysis.result import Result


class Runner:
    def __init__(self, path, registered_checkers=None):
        self.path = path
        self.registered_checkers = registered_checkers or []
        self.file_count = 0
        self.file_syntax_error_count = 0

    def read_file_content(self, file_path):
        with open(file_path, 'r') as f:
            source_code = f.read()

        return source_code

    def analyze_file(self, filename):
        try:
            print(f"Analyzing file: {filename}")
            source_code = self.read_file_content(file_path=filename)
            ast_module = astroid.parse(source_code)

            initial_count = len(Result.code_smells)

            for Checker in self.registered_checkers:
                checker = Checker(filename=filename)
                checker.visit(ast_module)

            new_count = len(Result.code_smells) - initial_count
            if new_count > 0:
                print(f'Found {new_count} code smell(s) in {filename}')

        except SyntaxError as e:
            print(f"Syntax error in file {filename}: {str(e)}")
            self.file_syntax_error_count += 1

        except Exception as e:
            print(f"Error analyzing file {filename}: {str(e)}")

    def analyze_directory(self, directory):
        print(f"Analyzing files in directory: {directory}")
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filename = os.path.join(root, file)
                    self.analyze_file(filename)
                    self.file_count += 1

    def run(self):
        if os.path.isfile(self.path) and self.path.endswith('.py'):
            self.analyze_file(self.path)
            self.file_count += 1
        elif os.path.isdir(self.path):
            self.analyze_directory(self.path)
        else:
            print(f'{self.path} is not a valid file or directory path')

        # Print code smells result
        Result.print_code_smells()

        # Research - Print code smells stats
        Result.print_code_smell_stats()

        # Research - Print project stats
        Result.print_project_stats(self.file_count, self.file_syntax_error_count)


def main():
    parser = argparse.ArgumentParser(description='Analyze ML-specific code smells',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='Examples:\n'
                                            '  mlpylint <path>                          # Check for code smells (CS)\n'
                                            '  mlpylint -a,  --advice <path>            # Check for code smells (CS) and include advisory results (CSA)\n'
                                            '  mlpylint -ls, --list-smells              # List all available code smells\n'
                                            '  mlpylint -ds, --describe-smell <id>      # Get code smell description by id\n'
                                            '  mlpylint -c,  --color <path>             # Enable colorized analysis output')

    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        nargs='?',  # makes the argument optional
                        default='',  # sets the default value to an empty string
                        help='File or directory path to analyze')

    parser.add_argument('-a', '--advice', action='store_true',
                        help='Include advice flag for potential code smell areas. Note, these highlight points for '
                             'further review, not definitive issues.')

    parser.add_argument('-ls', '--list-smells', action='store_true',
                        help='List all possible code smells')

    parser.add_argument('-ds', '--describe-smell', type=str, metavar='id',
                        help='Get the description of a specific code smell by its id')

    parser.add_argument('-c', '--color', action='store_true',
                        default=False,
                        help='Enable colorized analysis output')

    args = parser.parse_args()

    # Update the color configuration
    ColorConfig.get_instance(args.color)

    if args.list_smells:
        ArgumentConfig.handle_list_smells()
    elif args.describe_smell:
        ArgumentConfig.handle_describe_smell(args.describe_smell)
    else:
        # Setup analysis
        reg_checkers = REGISTERED_CHECKERS if not args.advice else REGISTERED_CHECKERS + REGISTERED_CHECKERS_ADVICE
        runner = Runner(path=args.path, registered_checkers=reg_checkers)

        # Start runtime timer
        start_time = time.time()

        # Start analysis
        runner.run()

        # End runtime timer
        end_time = time.time()

        # Calculate runtime
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        print(f'# runtime: {minutes}m{seconds}s')


if __name__ == '__main__':
    main()
