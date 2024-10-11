# This is code perfectly work entire program.
import random
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
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

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

#### Flashcard
def uniqueness_testing(flashcards, new_flashcard):
    terms_set = {flashcard['term'] for flashcard in flashcards}  # Use set for uniqueness
    if new_flashcard['term'] not in terms_set:  # Check if the new term is already present
        flashcards.append(new_flashcard)  # Add the flashcard if unique
        return True  # Indicate success
    return False  # Indicate failure due to duplicate term

def random_flashcards(flashcards):
    randomized_flashcards = []  # เก็บ flashcards ที่สุ่มแล้ว
    available_indices = list(range(len(flashcards)))  # ลำดับที่ยังไม่ถูกเลือก

    for _ in range(len(flashcards)):
        random_index = random.randrange(len(available_indices))  # สุ่มลำดับ
        randomized_flashcards.append(flashcards[available_indices[random_index]])  # เพิ่ม flashcard ที่สุ่มมา
        available_indices.pop(random_index)  # เอาลำดับที่สุ่มแล้วออก

    return randomized_flashcards

# Divide and Conquer for grouping flashcards by incorrect answers frequency
def divide_and_conquer_flashcards(flashcards, low_threshold):
    # Base case: if only one flashcard, return as it is already "divided"
    if len(flashcards) <= 1:
        return flashcards
    
    # Step 1: Divide the flashcards into two halves
    mid = len(flashcards) // 2
    left_half = divide_and_conquer_flashcards(flashcards[:mid], low_threshold)  # Recursively divide left half
    right_half = divide_and_conquer_flashcards(flashcards[mid:], low_threshold)  # Recursively divide right half
    
    # Step 2: Conquer by combining flashcards into "low priority" and "high priority" based on frequency
    low_priority = []
    high_priority = []
    
    # Process each half after recursive division
    for flashcard in left_half + right_half:
        if flashcard['incorrect_count'] > low_threshold:
            high_priority.append(flashcard)  # Add to high priority group
        else:
            low_priority.append(flashcard)  # Add to low priority group
    
    # Step 3: Combine the results
    return high_priority + low_priority  # Combine high priority first, then low priority

# Counting Sort Algorithm (used for sorting by difficulty)
def counting_sortflash(arr, key):
    difficulty_order = {'Easy': 1, 'Medium': 2, 'Hard': 3}

    # Create count array based on the maximum difficulty level
    max_difficulty = 3
    count = [0] * (max_difficulty + 1)
    output = [None] * len(arr)

    # Count the occurrences of each difficulty level
    for item in arr:
        difficulty_level = difficulty_order[item[key]]
        count[difficulty_level] += 1

    # Modify count to get the correct positions
    for i in range(1, max_difficulty + 1):
        count[i] += count[i - 1]

    # Build the output array based on the difficulty levels
    for item in reversed(arr):
        difficulty_level = difficulty_order[item[key]]
        output[count[difficulty_level] - 1] = item
        count[difficulty_level] -= 1

    print("Flashcards sorted by difficulty:", output)  # Debugging print statement

    return output
