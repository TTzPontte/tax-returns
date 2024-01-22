#!/bin/bash

echo "Find Symlinks"
grep -lr '../layers/common/python/common' src |\
        xargs -I@ bash layers/change_symlink.sh @