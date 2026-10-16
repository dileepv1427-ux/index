from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------- EASY

# 1. Maximum depth / height (number of nodes on the longest root-to-leaf path)
def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# 2. Identical trees
def is_same_tree(p, q):
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    return (p.val == q.val
            and is_same_tree(p.left, q.left)
            and is_same_tree(p.right, q.right))


# 3. Invert / mirror a binary tree
def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# 4. Symmetric tree
def is_symmetric(root):
    def mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return root is None or mirror(root.left, root.right)


# 5. Balanced binary tree (height difference <= 1 at every node)
def is_balanced(root):
    def height(node):                    # returns -1 as soon as a node is unbalanced
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) != -1


# 6. Convert sorted array to height-balanced BST
def sorted_array_to_bst(nums):
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(nums[mid], build(lo, mid - 1), build(mid + 1, hi))

    return build(0, len(nums) - 1)


# 7. Kth smallest / kth largest element in a BST (k starts at 1)
def kth_smallest(root, k):
    stack = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return None


def kth_largest(root, k):
    stack = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.right
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.left
    return None


# ---------------------------------------------------------------- MEDIUM

# 8. Diameter of a binary tree (number of edges on the longest path)
def diameter_of_binary_tree(root):
    best = 0

    def depth(node):
        nonlocal best
        if node is None:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    depth(root)
    return best


# 9. Validate binary search tree (strict bounds)
def is_valid_bst(root):
    def check(node, low, high):
        if node is None:
            return True
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, None, None)


# 10. Lowest common ancestor of two values (both assumed to be in the tree)
def lowest_common_ancestor(root, p, q):
    if root is None or root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root
    return left if left is not None else right


# 11. Zigzag level order traversal
def zigzag_level_order(root):
    result = []
    if root is None:
        return result
    queue = deque([root])
    left_to_right = True
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        if not left_to_right:
            level.reverse()
        result.append(level)
        left_to_right = not left_to_right
    return result


# 12. Construct tree from preorder and inorder traversals (unique values)
def build_tree(preorder, inorder):
    position = {value: i for i, value in enumerate(inorder)}
    pre_index = 0

    def build(lo, hi):
        nonlocal pre_index
        if lo > hi:
            return None
        value = preorder[pre_index]
        pre_index += 1
        mid = position[value]
        node = TreeNode(value)
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)


# 13. Boundary traversal (anticlockwise: left edge, leaves, right edge reversed)
def boundary_traversal(root):
    if root is None:
        return []

    def is_leaf(node):
        return node.left is None and node.right is None

    if is_leaf(root):
        return [root.val]

    result = [root.val]

    node = root.left                     # left edge, top to bottom, no leaves
    while node is not None:
        if not is_leaf(node):
            result.append(node.val)
        node = node.left if node.left is not None else node.right

    stack = [root]                       # all leaves, left to right
    while stack:
        node = stack.pop()
        if is_leaf(node):
            result.append(node.val)
        else:
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

    right_edge = []                      # right edge, no leaves, added bottom to top
    node = root.right
    while node is not None:
        if not is_leaf(node):
            right_edge.append(node.val)
        node = node.right if node.right is not None else node.left
    result.extend(reversed(right_edge))
    return result


# 14. Vertical order traversal (column -> list of (row, value))
def vertical_order_traversal(root):
    if root is None:
        return []
    columns = {}
    queue = deque([(root, 0, 0)])
    while queue:
        node, col, row = queue.popleft()
        columns.setdefault(col, []).append((row, node.val))
        if node.left is not None:
            queue.append((node.left, col - 1, row + 1))
        if node.right is not None:
            queue.append((node.right, col + 1, row + 1))
    return [[value for _, value in sorted(columns[col])] for col in sorted(columns)]


# 15. Check if a tree is a subtree of another
def is_subtree(root, sub):
    if sub is None:
        return True
    if root is None:
        return False
    return (is_same_tree(root, sub)
            or is_subtree(root.left, sub)
            or is_subtree(root.right, sub))


# ---------------------------------------------------------------- HARD

# 16. Binary tree maximum path sum
def max_path_sum(root):
    if root is None:
        return 0
    best = float("-inf")

    def gain(node):                      # best downward path starting at node
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return best


# 17. Binary tree to doubly linked list in place (left = prev, right = next)
def tree_to_dll(root):
    head = prev = None
    stack = []
    node = root
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
    return head


# 18. Serialize and deserialize a binary tree (level order, "null" for gaps)
def serialize(root):
    if root is None:
        return ""
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append("null")
        else:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    return ",".join(out)


def deserialize(data):
    if not data:
        return None
    tokens = data.split(",")
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    i = 1
    while queue and i < len(tokens):
        node = queue.popleft()
        if tokens[i] != "null":
            node.left = TreeNode(int(tokens[i]))
            queue.append(node.left)
        i += 1
        if i < len(tokens) and tokens[i] != "null":
            node.right = TreeNode(int(tokens[i]))
            queue.append(node.right)
        i += 1
    return root


# 19. Merge two BSTs into one balanced BST
def inorder_list(root):
    result = []
    stack = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        result.append(node.val)
        node = node.right
    return result


def merge_two_bsts(root1, root2):
    a = inorder_list(root1)
    b = inorder_list(root2)
    merged = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return sorted_array_to_bst(merged)


# 20. Burn a binary tree: minimum time to burn every node starting at target value
def burn_tree(root, target):
    if root is None:
        return 0
    parent = {root: None}
    start = None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.val == target:
            start = node
        for child in (node.left, node.right):
            if child is not None:
                parent[child] = node
                queue.append(child)
    if start is None:
        return -1

    burned = {start}
    queue = deque([start])
    time = 0
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt is not None and nxt not in burned:
                    burned.add(nxt)
                    queue.append(nxt)
        if queue:
            time += 1
    return time
