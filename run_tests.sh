#!/bin/bash

echo "Running tests..."
pytest --maxfail=4 --disable-warnings -q

SUCCESS=$(pytest --maxfail=1 --disable-warnings -q | grep -c "PASSED")
FAILED=$(pytest --maxfail=1 --disable-warnings -q | grep -c "FAILED")

echo "Tests completed."
echo "Successful tests: $SUCCESS"
echo "Failed tests: $FAILED"
