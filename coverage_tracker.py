import sys
import ast
import signal
import traceback
from typing import Any, Callable, List, Set, Tuple


class StatementCoverageTracker:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self.executed_lines: Set[int] = set()
        self.source_lines: List[str] = []
        self.line_offset: int = 0

    def trace_function(self, frame: Any, event: str, arg: Any) -> Callable:
        """Trace function to track executed lines"""
        if event == "line":
            # Adjust for the line offset when the function is not at the start of file
            self.executed_lines.add(frame.f_lineno - self.line_offset)
        return self.trace_function

    def timeout_handler(self, signum: int, frame: Any) -> None:
        """Handle timeout for long-running code"""
        raise TimeoutError("Execution exceeded maximum time limit of 2 minutes")

    def run_with_coverage(
        self, func: Callable, input_value: Any
    ) -> Tuple[List[str], Set[int]]:
        """Execute the function with the given input and track statement coverage"""
        # Set up timeout
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(self.timeout)

        try:
            # Set up the trace
            sys.settrace(self.trace_function)

            # Execute the function
            func(input_value)

            # Clear the trace
            sys.settrace(None)

            # Clear the alarm
            signal.alarm(0)

        except TimeoutError:
            sys.settrace(None)
            signal.alarm(0)
            print("Warning: Execution timed out after 2 minutes")
        except Exception as e:
            sys.settrace(None)
            signal.alarm(0)
            print(f"Error during execution: {str(e)}")
            traceback.print_exc()

        return self.source_lines, self.executed_lines

    def format_coverage(self, source_lines: List[str], executed_lines: Set[int]) -> str:
        """Format the coverage output according to specifications"""
        output = []
        for i, line in enumerate(source_lines, start=1):
            # Skip empty lines
            if not line.strip():
                continue
            # Determine if line was executed
            prefix = " " if i in executed_lines else "#"
            output.append(f"{prefix} {i} {line}")
        return "\n".join(output)

    def analyze_function(self, func_source: str, input_value: Any) -> str:
        """Analyze the function and return formatted coverage output"""
        # Parse the source to get line information
        tree = ast.parse(func_source)

        # Find the function definition
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.line_offset = node.lineno - 1
                break

        # Store source lines
        self.source_lines = func_source.splitlines()

        # Create function object from source
        namespace = {}
        exec(func_source, namespace)
        func = namespace[tree.body[0].name]  # Get the function object

        # Run the function with coverage tracking
        source_lines, executed_lines = self.run_with_coverage(func, input_value)

        # Format and return the coverage output
        return self.format_coverage(source_lines, executed_lines)
