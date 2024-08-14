#!/usr/bin/env bash

robot --listener $(pwd)/package/CustomListener.py \
      --outputdir ./output/test-run/ \
      ./tests/*.robot