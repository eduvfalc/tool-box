#!/usr/bin/env bash

robot --console quiet \
      --listener $(pwd)/package/CustomListener.py:true \
      --outputdir ./out/test-run/ \
      ./tests/robot-cheat-sheet.robot