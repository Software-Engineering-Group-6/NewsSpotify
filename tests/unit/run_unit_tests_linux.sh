#!/usr/bin/env bash
# Which python binary to use
PY_BIN=python3
# which files are we testing
TO_TEST=("track.py" "csv_reader.py" "spotify_interface.py")

# Run all unit tests
for t in "${TO_TEST[@]}"
do
    $PY_BIN "test_${t}"
    echo ""
done
