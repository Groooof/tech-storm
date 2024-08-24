#!/bin/bash

set -e

success_msg='\033[1;32mDONE\033[0m'
failed_msg='\033[1;31mFAILED\033[0m'

flake_exit_code=0
flake_label='\033[1;34m[flake8]\033[0m'
echo -e "$flake_label Start checking..."
flake8 backend || flake_exit_code=$?
if [ $flake_exit_code -eq 0 ]; then
    echo -e "$flake_label $success_msg"
else
    echo -e "$flake_label $failed_msg"
fi

isort_exit_code=0
isort_label='\033[1;35m[isort]\033[0m'
echo -e "\n$isort_label Start checking..."
isort backend --check-only --diff || isort_exit_code=$?
if [ $isort_exit_code -eq 0 ]; then
    echo -e "$isort_label $success_msg"
else
    echo -e "$isort_label $failed_msg"
fi

black_exit_code=0
black_label='\033[1;33m[black]\033[0m'
echo -e "\n$black_label Start checking..."
black backend --check --diff --color || black_exit_code=$?
if [ $black_exit_code -eq 0 ]; then
    echo -e "$black_label $success_msg"
else
    echo -e "$black_label $failed_msg"
fi

mypy_exit_code=0
mypy_label='\033[1;96m[mypy]\033[0m'
echo -e "\n$mypy_label Start checking..."
mypy backend --install-types --non-interactive || mypy_exit_code=$?
if [ $mypy_exit_code -eq 0 ]; then
    echo -e "$mypy_label $success_msg"
else
    echo -e "$mypy_label $failed_msg"
fi

[[
    $flake_exit_code -eq 0 \
    && $isort_exit_code -eq 0 \
    && $black_exit_code -eq 0 \
    && $mypy_exit_code -eq 0 
]]