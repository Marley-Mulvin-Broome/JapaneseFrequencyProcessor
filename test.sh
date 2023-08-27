#!/bin/bash

which pytest > /dev/null || { echo "Pytest not found, can't run tests."; exit 1; }

# coverage report settings
cov_report=html
required_coverage=95
open_report=false
generate_report=false
report=""
save_report=false

while getopts "r:c:hogs" opt; do
  case $opt in
    h)
        echo "Usage: [-ogs] test.sh [-r <required coverage>] [-c <coverage report type>]"
        echo "-o opens the coverage report in a browser after running tests. Requires -g"
        echo "-g generates a coverage report"
        echo "-s saves test coverage report to 'pytest-coverage.txt and pytest.xml"
        exit 0
        ;;
    r)
      required_coverage=$OPTARG
      ;;
    c)
      cov_report=$OPTARG
      ;;
    g)
      generate_report=true
      ;;
    o)
      open_report=true
      ;;
    s)
      save_report=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ "$open_report" = true ] && [ "$generate_report" = false ] ; then
  echo "Can't open report without generating it. Use -g to generate a report."
  exit 1
fi

if [ "$generate_report" = true ] && [ "$save_report" = false ]; then
  report="--cov=src/jpfreq --cov-branch --cov-report=$cov_report --cov-fail-under=$required_coverage"
elif [ "$generate_report" = true ] && [ "$save_report" = true ]; then
  report="--cov=src/jpfreq --cov-branch --cov-fail-under=$required_coverage --junitxml=pytest.xml --cov-report=term-missing --cov-fail-under=$required_coverage"
fi

exit_code=0

# runs coverage with a html report
# fails if cov < required_coverage
result=$(pytest -n auto $report tests/)
exit_code=$? 

if [ "$save_report" = true ] ; then
  echo "$result" > pytest-coverage.txt
fi

echo "$result"

ruff src/jpfreq/*.py || exit_code=$?


if [ "$open_report" = true ] ; then
  open htmlcov/index.html
fi

exit $exit_code