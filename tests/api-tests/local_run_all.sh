#!/bin/sh
#
set -e

currentFile=$(basename "$0")

if [ -f "./.envrc" ]; then
  source ./.envrc
fi

for file in local_*.sh; do
  if [ "$file" == "$currentFile" ]; then
    continue
  elif [ -x "$file" ]; then
    "./$file"
  else
    echo "$file can't be executed, check your file permissions 'ls -al'"
    echo "Abandoning Tests"
    exit
  fi
done

echo "Environment variables (including your password) will not persist after this terminal is closed"
