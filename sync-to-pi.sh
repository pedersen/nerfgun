#!/usr/bin/env bash

rsync -avP --exclude=btemu.egg-info --exclude=.idea --exclude=.git --exclude=sync-to-pi.sh --exclude=__pycache__ ./ nerfgun:nerfgun/
