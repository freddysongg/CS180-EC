#!/usr/bin/env python3
import sys
from coverage_tracker import StatementCoverageTracker


def read_function(filename: str) -> str:
    """Read the function source from a file"""
    with open(filename, "r") as f:
        return f.read()


def read_input(filename: str) -> str:
    """Read the test input from a file"""
    with open(filename, "r") as f:
        return eval(f.read().strip())


def main():
    if len(sys.argv) != 3:
        print("Usage: ./print_cov.py <function_file> <input_file>")
        sys.exit(1)

    function_file = sys.argv[1]
    input_file = sys.argv[2]

    try:
        func_source = read_function(function_file)
        test_input = read_input(input_file)

        tracker = StatementCoverageTracker()
        coverage_output = tracker.analyze_function(func_source, test_input)

        print(coverage_output)

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: Invalid Python syntax in function file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
