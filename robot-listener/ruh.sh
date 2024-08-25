#!/usr/bin/env bash

robot --console none \
      --listener $(pwd)/package/CustomListener.py \
      --outputdir ./output/test-run/ \
      --test "Call keywords with a varying number of arguments" \
      ./tests/robot-cheat-sheet.robot