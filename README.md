# Statement Coverage Tracker

This program tracks and prints statement coverage for Python functions with given test inputs.

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Unzip the `cs180_w25_netid.zip` file.
2. Make the `print_cov.py` script executable:

   ```bash
   chmod +x print_cov.py
   ```

## Usage

Run the program using:

```bash
./print_cov.py <function_file> <input_file>
```

Where:
- `<function_file>` is a Python file containing a single function.
- `<input_file>` is a file containing the test input (can be an integer, string, or array).

### Example

#### Function file (`example.py`):

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

#### Input file (`input.txt`):

```
5
```

#### Run the script:

```bash
./print_cov.py example.py input.txt
```

## Output Format

The output displays each line of the function with:
- A **space (` `)** prefix for executed lines.
- A **hash (`#`)** prefix for non-executed lines.

### Example Output:

```
     1  def factorial(n):
     2      if n <= 1:
     3          return 1
     4      return n * factorial(n - 1)
```

If a line is **not executed**, it appears with a `#`:

```
  #  1  def factorial(n):
  #  2      if n <= 1:
  #  3          return 1
  #  4      return n * factorial(n - 1)
```

## Error Handling

The program includes error handling for:
- **Invalid Python syntax** in the function file.
- **Missing files** (function file or input file).
- **Runtime errors** when executing the function.
- **Execution timeouts** (maximum of 2 minutes).
- **Invalid inputs** (unexpected data types).

## Submission Contents

Your submission should include:
- `coverage_tracker.py` – Main coverage tracking implementation.
- `print_cov.py` – Command-line interface script.
- `README.md` – Usage instructions.

---
