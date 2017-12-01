#!/bin/sh

VENV_DIR='./venv'

# remove egg directories.
rm -rf *.egg-info

# backup ol' virtualenv directory if it exists.
if [ -d $VENV_DIR ]; then
    mv $VENV_DIR "$VENV_DIR.$(date +%s)"
fi

virtualenv --python=python3 $VENV_DIR &&
    echo "Initialized virtualenv, run" &&
    echo "   source $VENV_DIR/bin/activate" &&
    echo "to activate the virtual environment."
