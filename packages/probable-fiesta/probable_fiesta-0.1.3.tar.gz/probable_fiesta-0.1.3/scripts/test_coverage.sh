#!/bin/bash

# Test specific files
coverage run -m unittest tests/app/builder/test_* tests/command/builder/test_* tests/logger/builder/test_* tests/test_* -v
coverage report -m