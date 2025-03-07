#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from coverage_tracker import StatementCoverageTracker

def test_capitalize_example():
    print("\n=== Testing Example 1: capitalize function ===")
    source = '''def capitalize(sentence: str) -> str:
    """
    Capitalizes the first letter of a sentence or word.
    """
    from string import ascii_lowercase, ascii_uppercase
    if not sentence:
        return ""
    # Create a dictionary that maps lowercase letters to uppercase letters
    # Capitalize the first character if it's a lowercase letter
    # Concatenate the capitalized character with the rest of the string
    lower_to_upper = dict(zip(ascii_lowercase, ascii_uppercase))
    return lower_to_upper.get(sentence[0], sentence[0]) + sentence[1:]'''

    test_input = "hello world"
    
    tracker = StatementCoverageTracker()
    result = tracker.analyze_function(source, test_input)
    
    print(f"\nTest Input: {test_input}")
    print("Coverage Output:")
    print(result)
    
    expected_lines = [
        "# 1 def capitalize(sentence: str) -> str:",
        "# 2     \"\"\"",
        "# 3     Capitalizes the first letter of a sentence or word.",
        "# 4     \"\"\"",
        " 5     from string import ascii_lowercase, ascii_uppercase",
        " 6     if not sentence:",
        "# 7         return \"\"",
        "# 8     # Create a dictionary that maps lowercase letters to uppercase letters",
        "# 9     # Capitalize the first character if it's a lowercase letter",
        "# 10     # Concatenate the capitalized character with the rest of the string",
        " 11     lower_to_upper = dict(zip(ascii_lowercase, ascii_uppercase))",
        " 12     return lower_to_upper.get(sentence[0], sentence[0]) + sentence[1:]"
    ]
    
    result_lines = result.split('\n')
    assert len(result_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines, got {len(result_lines)}"
    
    for i, (expected, actual) in enumerate(zip(expected_lines, result_lines)):
        assert expected.strip() == actual.strip(), \
            f"Line {i+1} mismatch:\nExpected: {expected}\nGot: {actual}"
    
    print("✓ Example 1 output matches assignment exactly")

def test_bubble_sort_example():
    print("\n=== Testing Example 2: bubble_sort_recursive function ===")
    source = '''def bubble_sort_recursive(collection: List[Any]) -> List[Any]:
    """It is similar iterative bubble sort but recursive.
    :param collection: mutable ordered sequence of elements
    :return: the same list in ascending order
    """
    from typing import Any, List
    length = len(collection)
    swapped = False
    for i in range(length - 1):
        if collection[i] > collection[i + 1]:
            collection[i], collection[i + 1] = collection[i + 1], collection[i]
            swapped = True
    return collection if not swapped else bubble_sort_recursive(collection)'''

    test_input = [-23, 0, 6, -4, 34]
    
    tracker = StatementCoverageTracker()
    result = tracker.analyze_function(source, test_input)
    
    print(f"\nTest Input: {test_input}")
    print("Coverage Output:")
    print(result)
    
    expected_lines = [
        "# 1 def bubble_sort_recursive(collection: List[Any]) -> List[Any]:",
        "# 2     \"\"\"It is similar iterative bubble sort but recursive.",
        "# 3     :param collection: mutable ordered sequence of elements",
        "# 4     :return: the same list in ascending order",
        "# 5     \"\"\"",
        " 6     from typing import Any, List",
        " 7     length = len(collection)",
        " 8     swapped = False",
        " 9     for i in range(length - 1):",
        " 10         if collection[i] > collection[i + 1]:",
        " 11             collection[i], collection[i + 1] = collection[i + 1], collection[i]",
        " 12             swapped = True",
        " 13     return collection if not swapped else bubble_sort_recursive(collection)"
    ]
    
    result_lines = result.split('\n')
    assert len(result_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines, got {len(result_lines)}"
    
    for i, (expected, actual) in enumerate(zip(expected_lines, result_lines)):
        assert expected.strip() == actual.strip(), \
            f"Line {i+1} mismatch:\nExpected: {expected}\nGot: {actual}"
    
    print("✓ Example 2 output matches assignment exactly")

def main():
    try:
        test_capitalize_example()
        test_bubble_sort_example()
        print("\n✓ All example tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 