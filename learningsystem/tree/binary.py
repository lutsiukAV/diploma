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

