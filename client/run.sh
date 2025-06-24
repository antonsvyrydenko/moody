#!/usr/bin/env bash

if [ "$1" = "" ]; then
    echo "Main usage:
    ./run.sh listener - launch mood handler result listener
    ./run.sh mood [sad|upset|angry|happy|curious] - send request for mood handler
    "
else
    case "$1" in
        freeze)
            source venv/bin/activate
            pip freeze | grep -v "pkg-resources" > requirements.txt
        ;;
        listener)
            source venv/bin/activate
            source secrets.file
            python main.py
        ;;
        request)
            source venv/bin/activate
            source secrets.file
            python sender.py $2
    esac
fi
