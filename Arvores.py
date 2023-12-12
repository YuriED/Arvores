import time
import ast
import random

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x





    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, root, key):
        if root is None:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1:
            if key < root.left.key:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if key > root.right.key:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root
    
    def in_order_traversal(self, root):
        result = []
        if root:
            result += self.in_order_traversal(root.left)
            result.append(root.key)
            result += self.in_order_traversal(root.right)
        return result

class RBNode:
    def __init__(self, key, color='R'):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = RBNode(key)
        self._insert(new_node)

    def _insert(self, z):
        y = None
        x = self.root

        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent is not None and z.parent.color == 'R':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y is not None and y.color == 'R':
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)

                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y is not None and y.color == 'R':
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)

                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self._left_rotate(z.parent.parent)

        self.root.color = 'B'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right is not None:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x


    def in_order_traversal(self, root):
        result = []
        self._in_order_traversal(root, result)
        return result

    def _in_order_traversal(self, root, result):
        if root:
            self._in_order_traversal(root.left, result)
            result.append(root.key)
            self._in_order_traversal(root.right, result)




# Function to read data from the file
def read_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return ast.literal_eval(file.read())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"Error reading the file '{filename}': {e}")
        return []

# File name containing the data
filename = "dados100_mil.txt"

# Read data from the file
data = read_data_from_file(filename)

if not data:
    print("Unable to get data from the file. Please check if the file is in the correct path and contains valid numbers.")
else:
    # Create AVL and Red-Black trees
    avl_tree = AVLTree()
    rb_tree = RedBlackTree()

    # Insert data into AVL and Red-Black trees and measure the time
    avl_start_time = time.time()
    for number in data:
        avl_tree.root = avl_tree.insert(avl_tree.root, number)
    avl_end_time = time.time()
    avl_time = avl_end_time - avl_start_time

    rb_start_time = time.time()
    for number in data:
        rb_tree.insert(number)
    rb_end_time = time.time()
    rb_time = rb_end_time - rb_start_time

    # Print results for AVL tree
    print(f"Time to insert data into AVL tree: {avl_time} seconds")
    print("Ordered data from AVL tree:")
    avl_ordered_data = avl_tree.in_order_traversal(avl_tree.root)
    for value in avl_ordered_data:
        print(value)

    # Print results for Red-Black tree
    print(f"Time to insert data into Red-Black tree: {rb_time} seconds")
    print("Ordered data from Red-Black tree:")
    rb_ordered_data = rb_tree.in_order_traversal(rb_tree.root)
    for value in rb_ordered_data:
        print(value)
def fill_trees_with_file_data(avl_tree, rb_tree, data):
    avl_start_time = time.time()
    for number in data:
        avl_tree.root = avl_tree.insert(avl_tree.root, number)
    avl_end_time = time.time()
    avl_time = avl_end_time - avl_start_time

    rb_start_time = time.time()
    for number in data:
        rb_tree.insert(number)
    rb_end_time = time.time()
    rb_time = rb_end_time - rb_start_time

    return avl_time, rb_time

# Função para realizar operações aleatórias nas árvores
def random_operations(avl_tree, rb_tree, num_operations=50000):
    for _ in range(num_operations):
        random_number = random.randint(-9999, 9999)

        if random_number % 3 == 0:
            avl_tree.root = avl_tree.insert(avl_tree.root, random_number)
            rb_tree.insert(random_number)
        elif random_number % 5 == 0:
            rb_tree.delete(random_number)
        else:
            avl_count = avl_tree.count_occurrences(avl_tree.root, random_number)
            rb_count = rb_tree.count_occurrences(rb_tree.root, random_number)
            print(f"Number {random_number} occurs {avl_count} times in AVL tree and {rb_count} times in Red-Black tree.")

# ... (Rest of the code)

if not data:
    print("Unable to get data from the file. Please check if the file is in the correct path and contains valid numbers.")
else:
    # Create AVL and Red-Black trees
    avl_tree = AVLTree()
    rb_tree = RedBlackTree()

    # Fill trees with data from the file and measure the time
    avl_fill_time, rb_fill_time = fill_trees_with_file_data(avl_tree, rb_tree, data)
    print(f"Time to fill AVL tree: {avl_fill_time} seconds")
    print(f"Time to fill Red-Black tree: {rb_fill_time} seconds")

    # Perform random operations on trees
    random_operations(avl_tree, rb_tree)