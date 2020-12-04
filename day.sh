#!/bin/zsh

if [ $# -eq 0 ]
then
    echo "usage: $0 DAY_NUM [test]"
    exit 0
fi

day_script="./src/day$1.py"
day_input="./input/day$1.txt"

if [  "$2" = "test" ]
then
    echo "Running tests for day $1"
    day_input=""
else
    echo "Running solution for day $1"
fi

python3 "$day_script" "$day_input"
