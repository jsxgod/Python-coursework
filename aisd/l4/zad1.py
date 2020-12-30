import sys
import bst as bst
import rbt as rbt
import hmap as hmap


def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", node.value, ' ('+node.color+')', sep="", file=file)
    _prefix += "   " if _last else "|  "
    children = []
    if node.left:
        children.append(node.left)
    if node.right:
        children.append(node.right)
    child_count = len(children)

    for i, child in enumerate(children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


assert len(sys.argv) == 3

if sys.argv[1] != '--type':
    print('Usage: --type bst|rbt|hmap')
    exit('Invalid argument: ' + sys.argv[1])

allowed_operations = ['insert', 'load', 'delete', 'find', 'min', 'max', 'successor', 'inorder', 'print']
allowed_types = ['bst', 'rbt', 'hmap']

struct_type = sys.argv[2]
assert struct_type in allowed_types

num_ops = int(input())
operations = []
for _ in range(num_ops):
    operations.append(input())

data_structure = None
if struct_type == 'bst':
    data_structure = bst.BST()
elif struct_type == 'rbt':
    data_structure = rbt.RBT()
elif struct_type == 'hmap':
    data_structure = hmap.HMAP()

for op in operations:
    args = op.split(' ')
    if args[0] == 'insert':
        data_structure.insert(args[1])
    elif args[0] == 'delete':
        data_structure.delete(args[1])
    elif args[0] == 'find':
        data_structure.find(args[1])
    elif args[0] == 'min':
        data_structure.min()
    elif args[0] == 'max':
        data_structure.max()
    elif args[0] == 'successor':
        data_structure.successor(args[1])
    elif args[0] == 'inorder':
        data_structure.inorder()
    elif args[0] == 'load':
        data_structure.load(args[1])
    elif args[0] == 'print':
        pprint_tree(data_structure.root)


