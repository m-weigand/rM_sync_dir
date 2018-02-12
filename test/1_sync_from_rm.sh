#!/bin/bash

# test -d rM && rm -r rM

# scp -r remarkable:/home/root/.local/share/remarkable/xochitl/ rM/
rsync -av --progress remarkable:/home/root/.local/share/remarkable/xochitl/ rM/
