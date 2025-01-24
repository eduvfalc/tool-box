#!/usr/bin/env bash

robot --console quiet \
      --listener $(pwd)/package/Listener.py \
      --outputdir ./out/test-run/ \
      ./tests/test.robot