#!/bin/bash
cd "$(dirname "$0")"
export $(grep -v '^#' .env | xargs)
python3 bot.py
