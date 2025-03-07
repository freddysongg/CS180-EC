import sys
import ast
from typing import Any, Callable, List, Set, Tuple
import threading


class StatementCoverageTracker:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.executed_lines: Set[int] = set()
        self.source_lines: List[str] = []
        self.line_offset: int = 0
        self.timed_out = False

    def trace_function(self, frame: Any, event: str, arg: Any) -> Callable:
        """Trace function to track executed lines"""
        if event == "line":
            self.executed_lines.add(frame.f_lineno - self.line_offset)
        return self.trace_function

    def timeout_handler(self):
        """Cross-platform timeout handler"""
        self.timed_out = True
        sys.settrace(None)
        thread = threading.current_thread()
        if thread is not threading.main_thread():
            thread._target = None
            import _thread

            _thread.interrupt_main()

    def run_with_coverage(
        self, func: Callable, input_value: Any
    ) -> Tuple[List[str], Set[int]]:
        """Execute the function with the given input and track statement coverage"""
        self.timed_out = False
        timer = threading.Timer(self.timeout, self.timeout_handler)

        try:
            timer.start()
            sys.settrace(self.trace_function)
            func(input_value)
        except KeyboardInterrupt:
            self.timed_out = True
        except ZeroDivisionError as e:
            result = self.format_coverage(self.source_lines, self.executed_lines)
            print("\nCoverage before error:")
            print(result)
            raise
        except Exception as e:
            pass
        finally:
            timer.cancel()
            sys.settrace(None)
            if self.timed_out:
                result = self.format_coverage(self.source_lines, self.executed_lines)
                print("\nCoverage before timeout:")
                print(result)
                raise TimeoutError("Function execution timed out")

        return self.source_lines, self.executed_lines

    def format_coverage(self, source_lines: List[str], executed_lines: Set[int]) -> str:
        """Format the coverage output according to specifications"""
        output = []

        for i, line in enumerate(source_lines, start=1):
            if not line.strip():
                continue

            prefix = " " if i in executed_lines else "#"

            formatted_line = f"{prefix} {i:2d}{line}"
            output.append(formatted_line)

        return "\n".join(output)

    def analyze_function(self, func_source: str, input_value: Any) -> str:
        """Analyze the function and return formatted coverage output"""
        try:
            tree = ast.parse(func_source)
        except SyntaxError as e:
            raise SyntaxError(f"Invalid Python syntax: {str(e)}")

        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.line_offset = node.lineno - 1
                    break

            self.source_lines = func_source.splitlines()

            namespace = {}
            exec(func_source, namespace)
            func = namespace[tree.body[0].name]
            source_lines, executed_lines = self.run_with_coverage(func, input_value)

            return self.format_coverage(source_lines, executed_lines)
        except (TimeoutError, ZeroDivisionError) as e:
            raise
        except Exception as e:
            raise type(e)(str(e))
