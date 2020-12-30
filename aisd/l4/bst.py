import node


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, s):
        if self.root is None:
            self.root = node.BSTNode(s)
        else:
            self.root.insert(s)

    def delete(self, s):
        if self.root is None:
            pass
        else:
            if self.root.value == s:  # deleting root
                if self.root.left is None and self.root.right is None:
                    self.root = None
                elif self.root.left is None and self.root.right is not None:  # only right child
                    self.root = self.root.right
                elif self.root.left is not None and self.root.right is None:  # only left child
                    self.root = self.root.left
                else:  # root has 2 children
                    min_right = self.root.right.min()
                    self.root.value = min_right.value
                    min_right.delete()
            else:
                n = self.find_node(s)
                if not n:
                    return
                if n.left and n.right:
                    min_right = n.right.min()
                    n.value = min_right.value
                    min_right.delete()
                else:
                    n.delete()

    def find(self, s):
        if self.root is not None:
            if self.root.find(s):
                print('1')
            else:
                print('0')
        else:
            print('0')

    def find_node(self, s) -> node.BSTNode:
        if self.root is not None:
            return self.root.find(s)
        else:
            return None

    def max(self):
        if self.root is not None:
            print(self.root.max().value)
        else:
            print('\n')

    def min(self):
        if self.root is not None:
            print(self.root.min().value)
        else:
            print('\n')

    def successor(self, k):
        if self.root is not None:
            n = self.root.find(k)

            if n.right is not None:
                print(n.right.min().value)
            else:
                if n.isLeftChild():
                    print(n.parent.value)
        else:
            print('\n')

    def inorder(self):
        if self.root is not None:
            print(*self.root.inorder([]))
        else:
            print('\n')

    def load(self, path):
        try:
            f = open(path, 'r')
        except IOError:
            print('File error')
        else:
            with f:
                for line in f:
                    for word in line.split():
                        word = word.strip("!@#$%^&*()_+=-/;:'[]|<>?,.")
                        self.insert(word)
            f.close()
