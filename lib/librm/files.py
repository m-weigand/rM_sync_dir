import os
import subprocess
import datetime
import json
import uuid
import shutil

import librm.tree as rmt
import librm.directory as rmd


def _gen_metadata(filename, parent=''):
    base = os.path.basename(filename)

    metadata = {
        "deleted": False,
        "lastModified": datetime.datetime.now().strftime('%s') + '000',
        "metadatamodified": False,
        "modified": False,
        "parent": parent,
        "pinned": False,
        "synced": False,
        "type": "DocumentType",
        "version": 1,
        "visibleName": base
    }
    return json.dumps(metadata, indent=5, sort_keys=True)


def _gen_contentdata():
    content = {
        "extraMetadata": {
        },
        "fileType": "pdf",
        "fontName": "",
        "lastOpenedPage": 0,
        "lineHeight": -1,
        "margins": 100,
        "pageCount": 1,
        "textScale": 1,
        "transform": {
            "m11": 1,
            "m12": 1,
            "m13": 1,
            "m21": 1,
            "m22": 1,
            "m23": 1,
            "m31": 1,
            "m32": 1,
            "m33": 1
        }
    }

    return json.dumps(content, indent=5, sort_keys=True)


class fileAdder(object):
    """Prepare objects for the remarkable """

    def __init__(self, syncdir):
        self.tree = rmt.gen_tree(syncdir)

    def to_rm(self, filename, subdir, outdir):
        """
        filename: input file (pdf/epub)
        subdir: subdirectory on rM
        outdir: output directory on PC
        """
        if not os.path.isdir(outdir):
            os.makedirs(outdir, exist_ok=True)

        node = self.tree

        if subdir != '':
            # find parent
            subitems = subdir.split('/')

            # loop over the individual levels
            for item in subitems:
                # print('looking in node', node.name, node.data['visibleName'])
                # loop over children
                found = False
                for child in node.children:
                    # ignore all non-directories
                    if not child.data['type'] == 'CollectionType':
                        continue

                    if child.data['visibleName'] == item:
                        # print('found level', item)
                        node = child
                        found = True
                        break
                if not found:
                    # create new one
                    print('creating directory {}'.format(item))
                    dir_uuid, content, metadata = rmd.create_dir(
                        item, parent=node.name,
                        write_to_disc=True, outdir=outdir
                    )
                    node_new = rmt.node(name=dir_uuid, data=metadata)
                    node.children.append(node_new)
                    node = node_new

            # this should contain the parent
            # print('SEARCH')
            # print(node.name, node.data['visibleName'])
            parent = node.name
        else:
            parent = ''

        # check if this file is already present in this parent
        for child in node.children:
            if(child.data['type'] == 'DocumentType' and
               child.data['visibleName'] == os.path.basename(filename)):
                # this file is already present
                print('file already in tree, skipping')
                return

        file_uuid = str(uuid.uuid4())

        metadata = _gen_metadata(filename, parent=parent)
        contentdata = _gen_contentdata()

        for ending in ('cache', 'highlights', 'thumbnails'):
            os.makedirs(outdir + os.sep + file_uuid + '.' + ending)

        with open(outdir + os.sep + file_uuid + '.metadata', 'w') as fid:
            fid.write(metadata)

        with open(outdir + os.sep + file_uuid + '.content', 'w') as fid:
            fid.write(contentdata)

        cmd = ''.join((
            'convert -density 300 ',
            '"' + filename + '"',
            '\'[0]\'',
            ' -colorspace Gray -separate -average ',
            '-shave 5%x5% -resize 280x374 ',
            outdir + os.sep + file_uuid + '.thumbnails' + os.sep + '0.jpg'
        ))
        print('calling convert to generate thumbnail')
        subprocess.call(cmd, shell=True)
        print('thumbnail finished')

        shutil.copy(filename, outdir + os.sep + file_uuid + '.pdf')
