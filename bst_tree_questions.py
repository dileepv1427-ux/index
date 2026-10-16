"""
bst_tree_questions.py
---------------------
The 20 classic binary-tree problems, adapted to OUR project's BST.

Each method uses only `self.root`, so in the exam you PASTE THE METHOD INSIDE
`class BSTIndex` in bst_index.py (and add `from collections import deque` at
the top if the method uses deque).  Here they sit in a subclass only so they can
be tested without touching your real file.

How the guide's tree code maps to our nodes
    TreeNode.val      ->  node.word      (the key, a string)
    TreeNode.left     ->  node.left
    TreeNode.right    ->  node.right
    (extra)               node.queue     (the word's LineQueue)
    root              ->  self.root
    new TreeNode(x)   ->  _BSTNode(x, 1) (the 1 is a placeholder line number)
    counting nodes    ->  self._count    (update it whenever nodes are added/removed)
"""

from collections import deque

from index_common import LineQueue
from bst_index import BSTIndex, _BSTNode


def _same_nodes(a, b, compare_lines=False):
    """Same shape and same words (and same line numbers if compare_lines)."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if a.word != b.word:
        return False
    if compare_lines and list(a.queue) != list(b.queue):
        return False
    return (_same_nodes(a.left, b.left, compare_lines)
            and _same_nodes(a.right, b.right, compare_lines))


class BSTTreeQuestions(BSTIndex):

    # 1. Maximum depth / height (number of nodes on the longest path)
    def max_depth(self):
        def depth(node):
            if node is None:
                return 0
            return 1 + max(depth(node.left), depth(node.right))
        return depth(self.root)

    # 2. Identical trees (compares this index's tree with another index's tree)
    def is_identical(self, other, compare_lines=False):
        return _same_nodes(self.root, other.root, compare_lines)

    # 3. Invert / mirror in place.  WARNING: the tree is no longer a valid BST,
    #    so search() and insert() stop working until you invert it back.
    #    (Useful trick: in-order of a mirrored tree gives DESCENDING order.)
    def invert(self):
        def flip(node):
            if node is None:
                return None
            node.left, node.right = flip(node.right), flip(node.left)
            return node
        self.root = flip(self.root)

    # 4. Symmetric tree.  Words are all different, so only the SHAPE can be
    #    symmetric (comparing words left vs right would never match).
    def is_symmetric_shape(self):
        def mirror(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return mirror(a.left, b.right) and mirror(a.right, b.left)
        return self.root is None or mirror(self.root.left, self.root.right)

    # 5. Balanced tree (height difference <= 1 at every node)
    def is_balanced(self):
        def height(node):                # -1 means "already unbalanced"
            if node is None:
                return 0
            left = height(node.left)
            if left == -1:
                return -1
            right = height(node.right)
            if right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        return height(self.root) != -1

    # 6a. Sorted array of words -> balanced BST (fresh nodes, placeholder lines)
    def build_from_sorted_words(self, words):
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            node = _BSTNode(words[mid], 1)
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node
        self.root = build(0, len(words) - 1)
        self._count = len(words)

    # 6b. Rebuild THIS index as a balanced tree, keeping every word's line numbers
    def rebuild_balanced(self):
        items = list(self.items_sorted())

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            word, queue = items[mid]
            node = _BSTNode(word, 0)
            node.queue = queue
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node
        self.root = build(0, len(items) - 1)

    # 7. Kth smallest / kth largest word (k starts at 1)
    def kth_smallest(self, k):
        stack = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.word
            node = node.right
        return None

    def kth_largest(self, k):
        stack = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.right
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.word
            node = node.left
        return None

    # 8. Diameter (number of edges on the longest path between any two nodes)
    def diameter(self):
        best = 0

        def depth(node):
            nonlocal best
            if node is None:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            best = max(best, left + right)
            return 1 + max(left, right)
        depth(self.root)
        return best

    # 9. Validate BST (strict bounds, words compared in ASCII order)
    def is_valid_bst(self):
        def check(node, low, high):
            if node is None:
                return True
            if low is not None and node.word <= low:
                return False
            if high is not None and node.word >= high:
                return False
            return check(node.left, low, node.word) and check(node.right, node.word, high)
        return check(self.root, None, None)

    # 10. Lowest common ancestor of two words (uses the BST ordering: no recursion)
    def lowest_common_ancestor(self, w1, w2):
        if self.search(w1) is None or self.search(w2) is None:
            return None                  # both words must be in the index
        low, high = min(w1, w2), max(w1, w2)
        node = self.root
        while node is not None:
            if high < node.word:         # both are in the left subtree
                node = node.left
            elif low > node.word:        # both are in the right subtree
                node = node.right
            else:                        # the paths split here
                return node.word
        return None

    # 11. Zigzag level order
    def zigzag_level_order(self):
        result = []
        if self.root is None:
            return result
        queue = deque([self.root])
        left_to_right = True
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.word)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            if not left_to_right:
                level.reverse()
            result.append(level)
            left_to_right = not left_to_right
        return result

    # 12. Rebuild the tree from preorder and inorder word lists (unique words)
    def build_from_preorder_inorder(self, preorder, inorder):
        position = {word: i for i, word in enumerate(inorder)}
        pre_index = 0

        def build(lo, hi):
            nonlocal pre_index
            if lo > hi:
                return None
            word = preorder[pre_index]
            pre_index += 1
            mid = position[word]
            node = _BSTNode(word, 1)
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node
        self.root = build(0, len(inorder) - 1)
        self._count = len(inorder)

    # 13. Boundary traversal (left edge, leaves, right edge reversed)
    def boundary_traversal(self):
        root = self.root
        if root is None:
            return []

        def is_leaf(node):
            return node.left is None and node.right is None

        if is_leaf(root):
            return [root.word]
        result = [root.word]

        node = root.left
        while node is not None:
            if not is_leaf(node):
                result.append(node.word)
            node = node.left if node.left is not None else node.right

        stack = [root]
        while stack:
            node = stack.pop()
            if is_leaf(node):
                result.append(node.word)
            else:
                if node.right is not None:
                    stack.append(node.right)
                if node.left is not None:
                    stack.append(node.left)

        right_edge = []
        node = root.right
        while node is not None:
            if not is_leaf(node):
                right_edge.append(node.word)
            node = node.right if node.right is not None else node.left
        result.extend(reversed(right_edge))
        return result

    # 14. Vertical order traversal
    def vertical_order(self):
        if self.root is None:
            return []
        columns = {}
        queue = deque([(self.root, 0, 0)])
        while queue:
            node, col, row = queue.popleft()
            columns.setdefault(col, []).append((row, node.word))
            if node.left is not None:
                queue.append((node.left, col - 1, row + 1))
            if node.right is not None:
                queue.append((node.right, col + 1, row + 1))
        return [[w for _, w in sorted(columns[c])] for c in sorted(columns)]

    # 15. Is `other` (another index's tree) a subtree of this tree?
    def contains_subtree(self, other, compare_lines=False):
        if other.root is None:
            return True
        stack = [self.root] if self.root is not None else []
        while stack:
            node = stack.pop()
            if _same_nodes(node, other.root, compare_lines):
                return True
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        return False

    # 16. Maximum path sum.  Words are not numbers, so the question must say what
    #     each node is worth.  Default weight: number of lines the word is on.
    def max_path_sum(self, weight=lambda node: len(node.queue)):
        if self.root is None:
            return 0
        best = float("-inf")

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            best = max(best, weight(node) + left + right)
            return weight(node) + max(left, right)
        gain(self.root)
        return best

    # 17. Tree -> doubly linked list in place (left = previous, right = next).
    #     The nodes are re-linked, so the index is EMPTY (root = None) afterwards.
    def to_doubly_linked_list(self):
        head = prev = None
        stack = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev is None:
                head = node
            else:
                prev.right = node
                node.left = prev
            prev = node
            node = node.right
        self.root = None
        self._count = 0
        return head

    # 18. Serialize / deserialize, including each word's line numbers.
    #     Words can never contain a comma or a colon (they are separators), so
    #     "," between nodes, ":" between word and lines, and an EMPTY token for a
    #     missing child cannot be confused with real words.
    #     Format of one node:  word:1|3|7
    def serialize(self):
        if self.root is None:
            return ""
        out = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("")
            else:
                out.append(node.word + ":" + "|".join(map(str, node.queue)))
                queue.append(node.left)
                queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data):
        def make(token):
            word, _, lines = token.partition(":")
            node = _BSTNode(word, 0)
            node.queue = LineQueue()
            if lines:
                for number in lines.split("|"):
                    node.queue.enqueue(int(number))
            return node

        if not data:
            self.root = None
            self._count = 0
            return
        tokens = data.split(",")
        root = make(tokens[0])
        count = 1
        queue = deque([root])
        i = 1
        while queue and i < len(tokens):
            node = queue.popleft()
            if i < len(tokens) and tokens[i] != "":
                node.left = make(tokens[i])
                queue.append(node.left)
                count += 1
            i += 1
            if i < len(tokens) and tokens[i] != "":
                node.right = make(tokens[i])
                queue.append(node.right)
                count += 1
            i += 1
        self.root = root
        self._count = count

    # 19. Merge two indexes into a NEW balanced BST.  A word that is in both gets
    #     the union of its line numbers.
    def merge_with(self, other):
        a = list(self.items_sorted())
        b = list(other.items_sorted())
        merged = []                                  # (word, sorted line list)
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i][0] < b[j][0]:
                merged.append((a[i][0], list(a[i][1])))
                i += 1
            elif a[i][0] > b[j][0]:
                merged.append((b[j][0], list(b[j][1])))
                j += 1
            else:
                lines = sorted(set(list(a[i][1]) + list(b[j][1])))
                merged.append((a[i][0], lines))
                i += 1
                j += 1
        for word, queue in a[i:] + b[j:]:
            merged.append((word, list(queue)))

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            word, lines = merged[mid]
            node = _BSTNode(word, 0)
            node.queue = LineQueue()
            for number in lines:
                node.queue.enqueue(number)
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        result = type(self)()
        result.root = build(0, len(merged) - 1)
        result._count = len(merged)
        return result

    # 20. Burn the tree: minutes until every node has burned, starting at the
    #     node holding `target_word` (fire spreads to children AND parent).
    def burn_time(self, target_word):
        if self.root is None:
            return -1
        parent = {self.root: None}
        start = None
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.word == target_word:
                start = node
            for child in (node.left, node.right):
                if child is not None:
                    parent[child] = node
                    queue.append(child)
        if start is None:
            return -1
        burned = {start}
        queue = deque([start])
        minutes = 0
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                for nxt in (node.left, node.right, parent[node]):
                    if nxt is not None and nxt not in burned:
                        burned.add(nxt)
                        queue.append(nxt)
            if queue:
                minutes += 1
        return minutes
