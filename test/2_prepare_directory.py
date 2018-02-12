#!/usr/bin/env python3

# find all PDF files in Input
import os
filenames = []
for root, dirs, files in os.walk('Input'):
    files = [filenames.append(root + os.sep + x) for x in files if x.endswith('.pdf')]
print(filenames)

# now prepare those PDF-files for output
import librm.files as rmf
obj = rmf.fileAdder('rM')
for filename in filenames:
    print(filename)
    rm_sub_dir = os.path.dirname(os.path.relpath(filename, 'Input'))
    print('rM directory: {}'.format(rm_sub_dir))
    obj.to_rm(filename, rm_sub_dir, "tmp")
