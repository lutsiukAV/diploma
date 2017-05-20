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
