class BTreeNode:
    def __init__(self, t):
        self.keys = []
        self.children = []
        self.param = t

    def insert(self, key):
        if len(self.children) > 0:
            index = -1
            result = None
            for i in range(len(self.keys)):
                if key < self.keys[i]:
                    result, m, l, r = self.children[i].insert(key)
                    index = i
                    break
            else:
                result, m, l, r = self.children[-1].insert(key)
                index = len(self.children) - 1
            if result:
                if len(self.keys) == 2 * self.param - 1:
                    middle = self.keys[self.param - 1]
                    left = BTreeNode(self.param)
                    left.keys = self.keys[:self.param - 1]
                    left.children = self.children[:len(self.children) // 2]
                    right = BTreeNode(self.param)
                    right.keys = self.keys[self.param:]
                    right.children = self.children[len(self.children) // 2:]
                    return True, middle, left, right
                else:
                    self.keys.append(m)
                    self.keys.sort()
                    newchildren = []
                    for child in self.children:
                        if key < min(child.keys) or key > max(child.keys):
                            newchildren.append(child)
                    self.children = newchildren
                    self.children.append(l)
                    self.children.append(r)
                    self.children.sort(key=lambda item: item.keys[0])
                    return False, None, None, None
            else:
                return False, None, None, None
        else:
            if len(self.keys) == 2 * self.param - 1:
                middle = self.keys[self.param - 1]
                left = BTreeNode(self.param)
                left.keys = self.keys[:self.param - 1]
                right = BTreeNode(self.param)
                right.keys = self.keys[self.param:]
                if key < middle:
                    left.keys.append(key)
                    left.keys.sort()
                else:
                    right.keys.append(key)
                    right.keys.sort()
                return True, middle, left, right
            else:
                self.keys.append(key)
                self.keys.sort()
                return False, None, None, None

    def to_object(self):
        return {'keys': self.keys, 'children': [elem.to_object() for elem in self.children]}

    def to_config(self):
        return {
            'text': {
                'name': ' '.join(map(str, self.keys))
            },
            'children': [child.to_config() for child in self.children]
        }


class BTree:
    def __init__(self, t):
        self.root = None
        self.param = t

    def insert(self, key):
        if self.root is None:
            self.root = BTreeNode(self.param)
            self.root.insert(key)
        else:
            res, m, l, r = self.root.insert(key)
            if res:
                if len(self.root.keys) == 2 * self.param - 1:
                    newroot = BTreeNode(self.param)
                    newroot.keys = [m]
                    newroot.children = [l] + [r]
                    self.root = newroot
                else:
                    self.root.keys.append(m)
                    self.root.keys.sort()
                    newchildren = []
                    for child in self.root.children:
                        if not key in range(min(child, max(child) + 1)):
                            newchildren.append(child)
                    self.root.children = newchildren
                    self.root.children.append(l)
                    self.root.children.append(r)
                    self.root.children.sort(key=lambda item: item.keys[0])

    def to_object(self):
        return self.root.to_object()

    def to_config(self):
        return self.root.to_config()