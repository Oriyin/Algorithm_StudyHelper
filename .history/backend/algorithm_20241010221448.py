# This is code perfectly work entire program.

# backend/algorithm.py

# Insertion Sort Algorithm (used for immediate sorting by due date when adding a new task)
def insertion_sort(arr, key):
    for i in range(1, len(arr)):
        current_element = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] > current_element[key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current_element
    return arr

# Merge Sort Algorithm (used for sorting by due date)
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i =  r = 0
    while l < len(left) and r < len(right):
        if left[l][key] <= right[r][key]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    return result + left[l:] + right[r:]

# Counting Sort Algorithm (used for sorting by priority)
def counting_sort(arr, key):
    max_priority = 3
    count = [0] * (max_priority + 1)
    output = [None] * len(arr)

    for item in arr:
        count[item[key]] += 1

    # Modify count to get the descending order position
    for i in range(max_priority - 1, -1, -1):
        count[i] += count[i + 1]

    for item in reversed(arr):
        output[count[item[key]] - 1] = item
        count[item[key]] -= 1

    return output

# Heap Sort Algorithm (used for sorting by both due date and priority)
def heap_sort(arr, key1, key2):
    n = len(arr)
    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key1, key2)
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Swap the root (max element) with the last element
        heapify(arr, i, 0, key1, key2)

    # Reverse the array to get the sorted order (from top to bottom)
    return arr[::-1]  # Reversing the sorted list to ensure correct display order

def heapify(arr, n, i, key1, key2):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child index
    right = 2 * i + 2  # Right child index

    # Compare left child with root
    if left < n and (arr[left][key1] < arr[largest][key1] or (arr[left][key1] == arr[largest][key1] and arr[left][key2] > arr[largest][key2])):
        largest = left

    # Compare right child with largest so far
    if right < n and (arr[right][key1] < arr[largest][key1] or (arr[right][key1] == arr[largest][key1] and arr[right][key2] > arr[largest][key2])):
        largest = right

    # Swap and continue heapifying if root is not largest
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        heapify(arr, n, largest, key1, key2)

# Naive String Search Algorithm (used for searching notes)
def naive_string_search(text, pattern):
    m = len(pattern)
    n = len(text)
    result = []

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            result.append(i)

    return result
