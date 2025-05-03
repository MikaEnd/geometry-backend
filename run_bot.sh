#!/bin/bash
cd "$(dirname "$0")"
export $(grep -v '^#' ~/telegram_bot/.env | xargs)
python3 bot.py
