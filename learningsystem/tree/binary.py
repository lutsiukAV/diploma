from enum import Enum

class Color(Enum):
    RED = 0
    BLACK = 1

class BinaryNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def toObject(self):
        left = {} 
        if not self.left is None:
            left = self.left.toObject()
        right = {}
        if not self.right is None:
            right = self.right.toObject()
        return {'key': self.key, 'left': left, 'right': right}

    def toTreantConfig(self):
        children = []
        if not self.left is None:
            children.append(self.left.toTreantConfig())
        if not self.right is None:
            children.append(self.right.toTreantConfig())
        return {'text': {'name': self.key}, 'children': children}

class BinaryHandler:
    @classmethod
    def insert(cls, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BinaryNode(key)
                return node
            else:
                node.left = cls.insert(node.left, key)
                return node
        elif key > node.key:
            if node.right is None:
                node.right = BinaryNode(key)
                return node
            else:
                node.right = cls.insert(node.right, key)
                return node
        else:
            return node

class BinaryTree:
    def __init__(self):
        self.root = None

    def toObject(self):
        return self.root.toObject()

    def toTreantConfig(self):
        return self.root.toTreantConfig()

    def insert(self, key):
        if self.root is None:
            self.root = BinaryNode(key)
        else:
            self.root = BinaryHandler.insert(self.root, key)

class AvlNode(BinaryNode):
    def __init__(self, key, left=None, right=None):
        super(AvlNode, self).__init__(key, left, right)

    def height(self):
        if self.left is None and self.right is None:
            return 1
        else:
            left = 0
            if not self.left is None:
                left = self.left.height()
            right = 0
            if not self.right is None:
                right = self.right.height()
            return 1 + max(left, right)

class AvlHandler:
    @classmethod
    def insert(cls, node, key):
        if key < node.key:
            if node.left is None:
                node.left = AvlNode(key)
                l = 0
                if not node.left is None:
                    l = node.left.height()
                r = 0
                if not node.right is None:
                    r = node.right.height()
                if abs(l - r) >= 2:
                    node = cls.balance(node)
                return node
            else:
                node.left = cls.insert(node.left, key)
                l = 0
                if not node.left is None:
                    l = node.left.height()
                r = 0
                if not node.right is None:
                    r = node.right.height()
                if abs(l - r) >= 2:
                    node = cls.balance(node)
                return node
        elif key > node.key:
            if node.right is None:
                node.right = AvlNode(key)
                l = 0
                if not node.left is None:
                    l = node.left.height()
                r = 0
                if not node.right is None:
                    r = node.right.height()
                if abs(l - r) >= 2:
                    node = cls.balance(node)
                return node
            else:
                node.right = cls.insert(node.right, key)
                l = 0
                if not node.left is None:
                    l = node.left.height()
                r = 0
                if not node.right is None:
                    r = node.right.height()
                if abs(l - r) >= 2:
                    node = cls.balance(node)
                return node
        else:
            return node

    @classmethod
    def balance(cls, node):
        newnode = node
        l = 0
        if not node.left is None:
            l = node.left.height()
        r = 0
        if not node.right is None:
            r = node.right.height()
        if r - l >= 2:
            rl = 0
            if not node.right.left is None:
                rl = node.right.left.height()
            rr = 0
            if not node.right.right is None:
                rr = node.right.right.height()
            if rl <= rr:
                newnode = AvlNode(node.right.key, AvlNode(node.key, node.left, node.right.left), node.right.right)
            elif rl > rr:
                newnode = AvlNode(node.right.left.key, AvlNode(node.key, node.left, node.right.left.left), AvlNode(node.right.key, node.right.left.right, node.right.right))
        elif l - r >= 2:
            ll = 0
            if not node.left.left is None:
                ll = node.left.left.height()
            lr = 0
            if not node.left.right is None:
                lr = node.left.right.height()
            if lr <= ll:
                newnode = AvlNode(node.left.key, node.left.left, AvlNode(node.key, node.left.right, node.right))
            elif lr > ll:
                newnode = AvlNode(node.left.right.key, AvlNode(node.left.key, node.left.left, node.left.right.left), AvlNode(node.key, node.left.right.right, node.right))
        return newnode

class AvlTree:
    def __init__(self):
        self.root = None

    def toObject(self):
        return self.root.toObject()

    def toTreantConfig(self):
        return self.root.toTreantConfig()

    def insert(self, key):
        if self.root is None:
            self.root = AvlNode(key)
        else:
            self.root = AvlHandler.insert(self.root, key)


class RBNode(BinaryNode):
    def __init__(self, key, left=None, right=None, color = Color.RED):
        super(RBNode, self).__init__(key, left, right)
        self.color = color

    def toObject(self):
        left = {} 
        if not self.left is None:
            left = self.left.toObject()
        right = {}
        if not self.right is None:
            right = self.right.toObject()
        return {'key': self.key, 'left': left, 'right': right, 'color': self.color}

    def toTreantConfig(self):
        children = []
        if not self.left is None:
            children.append(self.left.toTreantConfig())
        if not self.right is None:
            children.append(self.right.toTreantConfig())
        color_class = 'red-node'
        if self.color == Color.BLACK:
            color_class = 'black-node'
        return {'text': {'name': self.key}, 'HTMLclass': color_class, 'children': children}


class RBHandler:
    @classmethod
    def insert(cls, root, key):
        if key < root.key:
            if root.left is None:
                root.left = RBNode(key)
                if root.color == Color.BLACK:
                    return root, False, False, False
                else:
                    return root, True, False, False
            else:
                root.left, to_paint, to_check, is_right = cls.insert(root.left, key)
                if to_paint and not root.right is None and root.right.color == Color.RED:
                    root.left.color = Color.BLACK
                    root.right.color = Color.BLACK
                    root.color = Color.RED
                    return root, False, True, False
                elif to_paint and ((not root.right is None and root.right.color == Color.BLACK) or (root.right is None)):
                    root.left.color = Color.BLACK
                    if is_right:
                        root.left = RBNode(root.left.right.key, RBNode(root.left.key, root.left.left, root.left.right.left, color=root.left.color), root.left.right.right, color=root.left.right.color)
                    root = RBNode(root.left.key, root.left.left, RBNode(root.key, root.left.right, root.right, color=root.color), color=root.left.color)
                    return root, False, False, False
                elif to_check and root.color == Color.BLACK:
                    return root, False, False, False
                elif to_check and root.color == Color.RED:
                    return root, True, False, False
                else:
                    return root, False, False, False
        elif key > root.key:
            if root.right is None:
                root.right = RBNode(key)
                if root.color == Color.BLACK:
                    return root, False, False, True
                else:
                    return root, True, False, True
            else:
                root.right, to_paint, to_check, is_right = cls.insert(root.right, key)
                if to_paint and not root.left is None and root.left.color == Color.RED:
                    root.left.color = Color.BLACK
                    root.right.color = Color.BLACK
                    root.color = Color.RED
                    return root, False, True, True
                elif to_paint and ((not root.left is None and root.left.color == Color.BLACK) or (root.left is None)):
                    root.right.color = Color.BLACK
                    if not is_right:
                        root.right = RBNode(root.right.left.key, root.right.left.left, RBNode(root.right.key, root.right.left.right, root.right.right, color=root.right.color), color=root.right.left.color)
                    root = RBNode(root.right.key, RBNode(root.key, root.left, root.right.left, color=root.color), root.right.right, color = root.right.color)
                    return root, False, False, True
                elif to_check and root.color == Color.BLACK:
                    return root, False, False, True
                elif to_check and root.color == Color.RED:
                    return root, True, False, True
                else:
                    return root, False, False, False
        else:
            return root, False, False, False


class RBTree:
    def __init__(self):
        self.root = None

    def toObject(self):
        return self.root.toObject()

    def toTreantConfig(self):
        return self.root.toTreantConfig()

    def insert(self, key):
        if self.root is None:
            self.root = RBNode(key, color=Color.BLACK)
        else:
            self.root, to_paint, to_check, is_right = RBHandler.insert(self.root, key)
            self.root.color = Color.BLACK


