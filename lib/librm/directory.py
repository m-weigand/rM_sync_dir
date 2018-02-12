# create directories on the rM
import os
import uuid
import datetime
import json


def create_dir(name, parent=None, dir_uuid=None, write_to_disc=False,
               outdir=None):
    if dir_uuid is None:
        dir_uuid = str(uuid.uuid4())
    print('using uuid:', dir_uuid)

    if parent is None:
        parent = ''
    content = {}

    metadata = {
        "deleted": False,
        "lastModified": datetime.datetime.now().strftime('%s') + '000',
        "metadatamodified": True,
        "modified": True,
        "parent": parent,
        "pinned": False,
        "synced": False,
        "type": "CollectionType",
        "version": 0,
        "visibleName": name
    }
    if write_to_disc:
        if outdir is None:
            outdir = '.' + os.sep
        else:
            outdir = outdir + os.sep

        with open(outdir + '{}.metadata'.format(dir_uuid), 'w') as fid:
            json.dump(
                metadata,
                fid,
                indent=4,
                sort_keys=1,
            )
            fid.write('\n')

        with open(outdir + '{}.content'.format(dir_uuid), 'w') as fid:
            json.dump(content, fid)

    return dir_uuid, content, metadata
