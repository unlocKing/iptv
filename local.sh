#!/bin/bash

# source: https://github.com/back-to/iptv
# script to document all changes of playlist.m3u and data.py
# in another private git folder which is located at ../../local/iptv
# Guide:
# create a folder at ../../local/iptv
# type 'git init' into the terminal to create an empty git folder there

cp -v playlist.m3u ../../local/iptv/playlist.m3u
cp -v data.py ../../local/iptv/data.py

cd ../../local/iptv

if [[ `git status --porcelain` ]]; then
  # Changes
  git add playlist.m3u data.py
  git commit -m "UPDATE"
else
  # No changes
  echo "No changes"
fi

cd ../../livecli/iptv

echo "DONE"
