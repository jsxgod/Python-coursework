import node

BLACK = 'black'
RED = 'red'
NIL = 'nil'

class RBT:
    # every node has null nodes as children initially, create one such object for easy management
    NIL_LEAF = node.RBTNode(value=None, color=NIL, parent=None)

    def __init__(self):
        self.size = 0
        self.root = None

    def insert(self, s):
        if self.root is None:
            self.root = node.RBTNode(s, BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.size += 1
        else:
            inserted_node = self.root.insert(s)
            if inserted_node is None:
                return
            inserted_node.left = self.NIL_LEAF
            inserted_node.right = self.NIL_LEAF
            self.size += 1

            self.fix_insert(inserted_node)

    def fix_insert(self, current_node):
        while current_node.parent and current_node.parent.color == RED:
            if current_node.parent.isLeftChild():
                uncle = current_node.parent.parent.right

                if uncle.color == RED:
                    current_node.parent.color = BLACK
                    uncle.color = BLACK
                    current_node.parent.parent.color = RED
                    current_node = current_node.parent.parent
                else:
                    if current_node.isRightChild():
                        current_node = current_node.parent
                        self.left_rotation(current_node)

                    current_node.parent.color = BLACK
                    current_node.parent.parent.color = RED
                    self.right_rotation(current_node.parent.parent)
            else:
                uncle = current_node.parent.parent.left

                if uncle.color == RED:
                    current_node.parent.color = BLACK
                    uncle.color = BLACK
                    current_node.parent.parent.color = RED
                    current_node = current_node.parent.parent
                else:
                    if current_node.isLeftChild():
                        current_node = current_node.parent
                        self.right_rotation(current_node)

                    current_node.parent.color = BLACK
                    current_node.parent.parent.color = RED
                    self.left_rotation(current_node.parent.parent)

        self.root.parent = None
        self.root.color = BLACK

    def left_rotation(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left.color != NIL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:  # x is root
            self.root = right_child
        elif node.isLeftChild():  # x is left child
            node.parent.left = right_child
        else:  # x is right child
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def right_rotation(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right.color != NIL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:  # x is root
            self.root = left_child
        elif node.isRightChild():  # x is right child
            node.parent.right = left_child
        else:  # x is left child
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def delete(self, s):
        node = self.find_node(s)
        n = None
        m = None
        if node is None:
            return
        if node.left.color == NIL or node.right.color == NIL:
            n = node
        else:
            n = self.successor_node(s)

        if n.left.color != NIL:
            m = n.left
        else:
            m = n.right

        m.parent = n.parent

        if n.parent is None:
            self.root = m
        elif n.isLeftChild():
            n.parent.left = m
        else:
            n.parent.right = m

        if n is not node:
            node.value = n.value

        if n.color == BLACK:
            self.fix_delete(m)

        self.NIL_LEAF.color = NIL
        self.size -= 1

    def fix_delete(self, node):
        sibling = None
        while node.parent and node.color == BLACK:
            if node.isLeftChild():
                sibling = node.parent.right

                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.left_rotation(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.right.color == BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self.right_rotation(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.right.color = BLACK
                    self.left_rotation(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left

                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.right_rotation(node.parent)
                    sibling = node.parent.left

                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self.left_rotation(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.left.color = BLACK
                    self.right_rotation(node.parent)
                    node = self.root
        node.color = BLACK

    def find(self, s):
        if self.root is not None:
            if self.root.find(s):
                print('1')
            else:
                print('0')
        else:
            print('0')

    def find_node(self, s) -> node.RBTNode or None:
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
            n = self.find_node(k)

            if n.right.color != NIL:
                print(n.right.min().value)
            else:
                if n.isLeftChild():
                    print(n.parent.value)
        else:
            print('\n')

    def successor_node(self, k):
        if self.root is not None:
            n = self.find_node(k)

            if n.right.color != NIL:
                return n.right.min()
            else:
                if n.isLeftChild():
                    return n.parent
        else:
            return None

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
