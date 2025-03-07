#!/usr/bin/env python3
import os
import sys
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from coverage_tracker import StatementCoverageTracker


def create_temp_file(content):
    """Create a temporary file with given content"""
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    temp.write(content)
    temp.close()
    return temp.name


def run_test(func_source, test_input, expect_error=False):
    """Run a test and optionally verify expected coverage"""
    try:
        tracker = StatementCoverageTracker()
        result = tracker.analyze_function(func_source, test_input)

        if expect_error:
            print("\nWarning: Expected error did not occur")
            return None

        print(f"\nTest Input: {test_input}")
        print("Coverage Output:")
        print(result)
        return result

    except (SyntaxError, ZeroDivisionError, TimeoutError) as e:
        if expect_error:
            print(f"\nExpected error occurred: {type(e).__name__}: {str(e)}")
            return "ERROR_EXPECTED"
        print(f"\nUnexpected error: {type(e).__name__}: {str(e)}")
        return None

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        return None


def test_simple_function():
    print("\n=== Testing simple_function ===")
    with open(Path(__file__).parent / "test_functions.py", "r") as f:
        source = f.read()

    # Test positive input
    assert run_test(
        """def simple_function(x):
    if x > 0:
        return x + 1
    else:
        return x - 1""",
        5,
    )

    # Test negative input
    assert run_test(
        """def simple_function(x):
    if x > 0:
        return x + 1
    else:
        return x - 1""",
        -5,
    )


def test_recursive_function():
    print("\n=== Testing recursive_function ===")
    # Test normal recursion
    assert run_test(
        """def recursive_function(n):
    if n <= 1:
        return 1
    return n * recursive_function(n - 1)""",
        5,
    )


def test_loop_function():
    print("\n=== Testing loop_function ===")
    assert run_test(
        """def loop_function(n):
    result = 0
    for i in range(n):
        result += i
    return result""",
        5,
    )


def test_timeout():
    print("\n=== Testing timeout handling ===")
    result = run_test(
        """def infinite_loop(n):
    while True:
        n += 1""",
        1,
        expect_error=True,
    )
    
    assert result == "ERROR_EXPECTED", "Timeout test should pass"
    print("✓ Timeout handled correctly")


def test_complex_branches():
    print("\n=== Testing complex branches ===")
    # Test different branches
    for test_input in [-1, 0, 5, 15]:
        assert run_test(
            """def complex_branches(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    elif x < 10:
        return 1
    else:
        return 2""",
            test_input,
        )


def test_different_input_types():
    print("\n=== Testing different input types ===")
    # Test with string
    assert run_test(
        """def string_function(s):
    if len(s) > 0:
        return s.upper()
    return ''""",
        "hello",
    )

    # Test with array
    assert run_test(
        """def array_function(arr):
    if len(arr) > 0:
        return sum(arr)
    return 0""",
        [1, 2, 3],
    )


def test_empty_lines():
    print("\n=== Testing empty line handling ===")
    source = """def function_with_spaces(x):

    if x > 0:
        
        return x

    return 0"""

    result = run_test(source, 5)
    if result is None:
        assert False, "Test failed to run"

    output_lines = result.split("\n")
    for line in output_lines:
        assert line.strip(), f"Found empty line in output: '{line}'"

    line_numbers = []
    for line in output_lines:
        try:
            num = int(line[2:4])
            line_numbers.append(num)
        except ValueError:
            continue

    expected = [1, 3, 5, 7]  
    assert (
        line_numbers == expected
    ), f"Line numbers mismatch. Expected {expected}, got {line_numbers}"

    for line in output_lines:
        if "return x" in line:
            code_part = line[4:] 
            assert code_part.startswith(
                "        "
            ), f"Incorrect indentation in line: {line}"


def test_indentation():
    print("\n=== Testing indentation preservation ===")
    assert run_test(
        """def nested_function(x):
    if x > 0:
        if x > 10:
            return 2
        return 1
    return 0""",
        15,
    )


def test_error_cases():
    print("\n=== Testing error cases ===")

    print("\nTesting syntax error:")
    result = run_test("def bad_syntax(x:", 5, expect_error=True)
    assert result == "ERROR_EXPECTED", "Syntax error test should pass"

    print("\nTesting runtime error:")
    result = run_test(
        """def error_function(x):
    return x / 0""",
        5,
        expect_error=True,
    )
    assert result == "ERROR_EXPECTED", "Runtime error test should pass"

    print("✓ Error cases handled correctly")


def main():
    test_simple_function()
    test_recursive_function()
    test_loop_function()
    test_complex_branches()
    test_different_input_types()
    test_error_cases()
    test_empty_lines()
    test_indentation()
    test_timeout()
    print("\nAll tests completed!")


if __name__ == "__main__":
    main()
