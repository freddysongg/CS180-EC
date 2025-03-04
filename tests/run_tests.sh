#!/bin/bash

chmod +x ../print_cov.py

echo "5" > test_input_positive.txt
echo "-5" > test_input_negative.txt
echo "10" > test_input_loop.txt

echo "Testing print_cov.py with simple function..."
../print_cov.py test_functions.py test_input_positive.txt

echo -e "\nRunning Python test suite..."
python3 test_runner.py 