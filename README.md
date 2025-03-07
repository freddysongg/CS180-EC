# Statement Coverage Tracker

This program tracks and prints statement coverage for Python functions with given test inputs, following the CS180 Extra Credit assignment requirements.

## Features

- Tracks statement coverage for Python functions
- Handles different input types (integers, strings, arrays)
- Manages loops and recursion with 60-second timeout
- Preserves code indentation and structure
- Provides clear coverage visualization

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Unzip the `cs180_w25_fsong009.zip` file:
```bash
unzip cs180_w25_fsong009.zip
```

2. Make the script executable:
```bash
chmod +x print_cov.py
```

## Usage

Run the program with a single command:

```bash
./print_cov.py <function_file> <input_file>
```

Where:
- `<function_file>`: Python file containing a single function
- `<input_file>`: File containing the test input (integer, string, or array)

### Input Format

1. Function file should contain a single Python function:
```python
def example_function(x):
    if x > 0:
        return x + 1
    return x - 1
```

2. Input file should contain a valid Python literal:
```python
5  # for integer input
"hello"  # for string input
[1, 2, 3]  # for array input
```

### Output Format

The output shows each line with:
- A hash (`#`) prefix for non-executed lines
- A space (` `) prefix for executed lines
- Line numbers starting from 1
- Original indentation preserved

Example output:
```
#  1 def example_function(x):
   2     if x > 0:
   3         return x + 1
#  4     return x - 1
```

## Error Handling

The program handles:
1. Invalid syntax in function files
2. Missing or unreadable files
3. Invalid input formats
4. Runtime errors
5. Infinite loops/recursion (60-second timeout)

## Implementation Details

- Uses Python's built-in `sys` and `ast` modules for coverage tracking
- Implements custom trace function for statement coverage
- Handles timeouts using threading
- Preserves code structure and indentation
- Follows assignment output format specifications

## Testing

Run the test suite:
```bash
cd tests
chmod +x run_tests.sh
./run_tests.sh
```

The tests verify:
- Basic function coverage
- Different input types
- Error handling
- Empty line handling
- Timeout functionality
- Indentation preservation

## Examples

### Example 1: Simple Function

Function file (`example.py`):
```python
def capitalize(word):
    if not word:
        return ""
    return word[0].upper() + word[1:]
```

Input file (`input.txt`):
```
"hello"
```

Run:
```bash
./print_cov.py example.py input.txt
```

Output:
```
#  1 def capitalize(word):
   2     if not word:
#  3         return ""
   4     return word[0].upper() + word[1:]
```

### Example 2: Array Input

Function file (`sort.py`):
```python
def sort_array(arr):
    if len(arr) <= 1:
        return arr
    return sorted(arr)
```

Input file (`array_input.txt`):
```
[3, 1, 4, 1, 5]
```

Run:
```bash
./print_cov.py sort.py array_input.txt
```

## Submission Contents

- `coverage_tracker.py`: Core coverage tracking implementation
- `print_cov.py`: Command-line interface
- `tests/`: Test suite and examples
- `README.md`: Usage instructions

## Notes

- Maximum execution time: 60 seconds
- Line numbers start from 1
- Empty lines are skipped in output
- Original code indentation is preserved

---
