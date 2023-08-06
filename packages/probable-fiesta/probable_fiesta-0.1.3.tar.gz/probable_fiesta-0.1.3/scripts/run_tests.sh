#!/bin/bash

# Test main folder
#python -m unittest discover -s tests -p "test_*.py"

# Test specific file
python -m unittest tests/app/builder/test_* tests/command/builder/test_* tests/logger/builder/test_* tests/config/builder/test_* tests/cli/builder/test_* tests/test_* -v