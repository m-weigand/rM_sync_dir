import os
from glob import glob

import json


def gen_tree(directory):
    pwd = os.getcwd()
    os.chdir(directory)
    dirfiles = glob('*.metadata')
    # generate rM tree from a local directory copy
    # read in metadata of directories
    md = {}
    for filename in dirfiles:
        with open(filename, 'r') as fid:
            entry = json.load(fid)
            # if entry['type'] == 'CollectionType':
            md[filename[:-len('.metadata')]] = entry

    os.chdir(pwd)

    # root node
    root = node(None, '')
    root.children = find_children(root, md)
    print('TREE')
    print_tree(root)
    return root


# define a tree-like structure
class node():
    def __init__(self, data, name):
        self.name = name
        self.children = []
        if data is None:
            self.data = {}
            self.data['visibleName'] = 'root'
        else:
            self.data = data


# populate tree
def find_children(root, md, depth=''):
    # print(depth + 'find children of parent {}'.format(root.name))
    children = []
    for name, item in md.items():
        # print(depth + 'check', name, item['visibleName'], item['parent'])
        if item['parent'] == root.name:
            # print(depth + '  found child')
            obj = node(item, name)
            subchilds = find_children(obj, md, depth=depth + '  ')
            obj.children = subchilds
            children.append(obj)
    return children


def print_tree(tree, depth=''):
    print(depth + tree.name + ' ({})'.format(tree.data['visibleName']))
    for child in tree.children:
        print_tree(child, depth + '  ')

