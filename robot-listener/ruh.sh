#!/usr/bin/env bash

robot --console quiet \
      --listener $(pwd)/package/CustomListener.py:true \
      --outputdir ./output/test-run/ \
      --test "Call keywords with a varying number of arguments" \
      ./tests/robot-cheat-sheet.robot