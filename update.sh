#!/bin/bash
git add .
git commit -m "${1:-Updated}"
git push

