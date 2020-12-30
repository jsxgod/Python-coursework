class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def insert(self, value):
        if value == self.value:
            return
        if value < self.value:
            if self.left is None:
                self.left = BSTNode(value)
                self.left.parent = self
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BSTNode(value)
                self.right.parent = self
            else:
                self.right.insert(value)

    def find(self, value):
        if self.value == value:
            return self
        elif value < self.value and self.left is not None:
            return self.left.find(value)
        elif value > self.value and self.right is not None:
            return self.right.find(value)
        else:
            return None

    def max(self):
        if self.right is not None:
            return self.right.max()
        else:
            return self

    def min(self):
        if self.left is not None:
            return self.left.min()
        else:
            return self

    def inorder(self, result):
        if self.left:
            self.left.inorder(result)
        result.append(self.value)
        if self.right:
            self.right.inorder(result)
        return result

    def delete(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.left = None
            else:
                self.parent.right = None
        elif self.left is None and self.right:
            if self.isLeftChild():
                self.parent.left = self.right
            else:
                self.parent.right = self.right
        elif self.left and self.right is None:
            if self.isLeftChild():
                self.parent.left = self.left
            else:
                self.parent.right = self.left

    def isLeftChild(self):
        if self.value < self.parent.value:
            return True
        else:
            return False

    def isRightChild(self):
        if self.value > self.parent.value:
            return True
        else:
            return False

    def isLeaf(self):
        return self.left is None and self.right is None


class RBTNode:
    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.color = color
        self.parent = parent

    def isParent(self):
        return self.left is not None or self.right is not None

    def children_count(self):
        if self.color == 'nil':
            return 0
        return int(self.left.color != 'nil') + int(self.right.color != 'nil')

    def insert(self, value):
        if value == self.value:
            return None
        if value < self.value:
            if self.left.color == 'nil':
                self.left = RBTNode(value, color='red', parent=self)
                return self.left
            else:
                return self.left.insert(value)
        else:
            if self.right.color == 'nil':
                self.right = RBTNode(value, color='red', parent=self)
                return self.right
            else:
                return self.right.insert(value)

    def find(self, value):
        if self.value == value:
            return self
        elif value < self.value and self.left.color != 'nil':
            return self.left.find(value)
        elif value > self.value and self.right.color != 'nil':
            return self.right.find(value)
        else:
            return None

    def max(self):
        if self.right.color != 'nil':
            return self.right.max()
        else:
            return self

    def min(self):
        if self.left.color != 'nil':
            return self.left.min()
        else:
            return self

    def inorder(self, result):
        if self.left.color != 'nil':
            self.left.inorder(result)
        result.append(self.value)
        if self.right.color != 'nil':
            self.right.inorder(result)
        return result

    def isLeftChild(self):
        if self.value < self.parent.value:
            return True
        else:
            return False

    def isRightChild(self):
        if self.value > self.parent.value:
            return True
        else:
            return False