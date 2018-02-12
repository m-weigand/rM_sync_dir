#!/bin/bash
cd tmp
rsync -avz --progress ./ remarkable:/home/root/.local/share/remarkable/xochitl/
cd ..
ssh remarkable systemctl restart xochitl
