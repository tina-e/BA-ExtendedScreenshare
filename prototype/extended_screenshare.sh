#!/bin/sh
while getopts k:m: flag
do
  case "${flag}" in
    k) keyboard=${OPTARG};;
    m) mouse=${OPTARG};;
  esac
done
python3 gui_qt.py $keyboard $mouse