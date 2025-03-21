import streamlit as st
import numpy as np
import time
import altair as alt
import pandas as pd

# Set page title and configure layout
st.set_page_config(page_title="Sorting Algorithm Visualizer", layout="wide")
st.title("Sorting Algorithm Visualizer")

# Sorting algorithms implementation
def bubble_sort(arr, visualize):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                visualize(arr, [j, j + 1])
                time.sleep(0.1)
    return arr

def selection_sort(arr, visualize):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        visualize(arr, [i, min_idx])
        time.sleep(0.1)
    return arr

def insertion_sort(arr, visualize):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            visualize(arr, [j + 1, i])
            time.sleep(0.1)
        arr[j + 1] = key
        visualize(arr, [j + 1])
        time.sleep(0.1)
    return arr

def merge_sort_helper(arr, start, end, visualize):
    if end - start > 1:
        mid = (start + end) // 2
        merge_sort_helper(arr, start, mid, visualize)
        merge_sort_helper(arr, mid, end, visualize)
        merge(arr, start, mid, end, visualize)

def merge(arr, start, mid, end, visualize):
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        visualize(arr, [k])
        time.sleep(0.1)
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        visualize(arr, [k])
        time.sleep(0.1)
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        visualize(arr, [k])
        time.sleep(0.1)
        j += 1
        k += 1

def merge_sort(arr, visualize):
    merge_sort_helper(arr, 0, len(arr), visualize)
    return arr

def heapify(arr, n, i, visualize):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[largest] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        visualize(arr, [i, largest])
        time.sleep(0.1)
        heapify(arr, n, largest, visualize)

def heap_sort(arr, visualize):
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, visualize)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        visualize(arr, [0, i])
        time.sleep(0.1)
        heapify(arr, i, 0, visualize)
    
    return arr

def quick_sort_partition(arr, low, high, visualize):
    i = low - 1
    pivot = arr[high]
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            visualize(arr, [i, j, high])
            time.sleep(0.1)
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    visualize(arr, [i + 1, high])
    time.sleep(0.1)
    return i + 1

def quick_sort_helper(arr, low, high, visualize):
    if low < high:
        pi = quick_sort_partition(arr, low, high, visualize)
        quick_sort_helper(arr, low, pi - 1, visualize)
        quick_sort_helper(arr, pi + 1, high, visualize)

def quick_sort(arr, visualize):
    quick_sort_helper(arr, 0, len(arr) - 1, visualize)
    return arr

def counting_sort(arr, visualize):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    output = [0] * len(arr)
    
    for num in arr:
        count[num] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1
        visualize(output)
        time.sleep(0.1)
    
    arr[:] = output
    return arr


def radix_sort(arr, visualize):
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        counting_sort_radix(arr, exp, visualize)
        exp *= 10
    return arr


def counting_sort_radix(arr, exp, visualize):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for num in reversed(arr):
        index = (num // exp) % 10
        output[count[index] - 1] = num
        count[index] -= 1
        visualize(output)
        time.sleep(0.1)
    
    for i in range(n):
        arr[i] = output[i]


def bucket_sort(arr, visualize):
    num_buckets = len(arr) // 5
    max_val = max(arr)
    buckets = [[] for _ in range(num_buckets)]
    
    for num in arr:
        index = min(num_buckets - 1, num * num_buckets // (max_val + 1))
        buckets[index].append(num)
    
    for bucket in buckets:
        bucket.sort()
        visualize(arr)
        time.sleep(0.1)
    
    arr[:] = [num for bucket in buckets for num in bucket]
    return arr


def shell_sort(arr, visualize):
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                visualize(arr, [j])
                time.sleep(0.1)
            arr[j] = temp
        gap //= 2
    return arr


def tim_sort(arr, visualize):
    arr.sort()
    visualize(arr)
    time.sleep(0.1)
    return arr

# Sidebar controls
st.sidebar.header("Controls")
array_size = st.sidebar.slider("Array Size", 5, 50, 20)
algorithm = st.sidebar.selectbox(
    "Select Sorting Algorithm",
    [
        "Bubble Sort", "Selection Sort", "Quick Sort", "Insertion Sort", "Merge Sort", "Heap Sort",
        "Counting Sort", "Radix Sort", "Bucket Sort", "Shell Sort", "Tim Sort"
    ]
)

# Generate random array
if 'array' not in st.session_state or st.sidebar.button("Generate New Array"):
    st.session_state.array = list(np.random.randint(1, 100, array_size))

# Create a placeholder for the chart
chart_placeholder = st.empty()

# Visualization function
def visualize_array(arr, highlighted_indices=[]):
    df = pd.DataFrame({
        'index': range(len(arr)),
        'value': arr
    })
    
    color_condition = alt.condition(
        alt.FieldOneOfPredicate(field='index', oneOf=highlighted_indices),
        alt.value('red'),
        alt.value('blue')
    )
    
    chart = alt.Chart(df).mark_bar().encode(
        x='index:O',
        y='value:Q',
        color=color_condition
    ).properties(
        width=800,
        height=400
    )
    
    chart_placeholder.altair_chart(chart)

# Display initial array
visualize_array(st.session_state.array)

# Start sorting button
if st.button("Start Sorting"):
    # Create a copy of the array for sorting
    arr = st.session_state.array.copy()
    
    # Select and execute the chosen sorting algorithm
    if algorithm == "Bubble Sort":
        bubble_sort(arr, visualize_array)
    elif algorithm == "Selection Sort":
        selection_sort(arr, visualize_array)
    elif algorithm == "Quick Sort":
        quick_sort(arr, visualize_array)
    elif algorithm == "Insertion Sort":
        insertion_sort(arr, visualize_array)
    elif algorithm == "Merge Sort":
        merge_sort(arr, visualize_array)
    elif algorithm == "Heap Sort":  
        heap_sort(arr, visualize_array)
    elif algorithm == "Counting Sort":
        counting_sort(arr, visualize_array)
    elif algorithm == "Radix Sort":
        radix_sort(arr, visualize_array)
    elif algorithm == "Bucket Sort":
        bucket_sort(arr, visualize_array)
    elif algorithm == "Shell Sort":
        shell_sort(arr, visualize_array)
    else:
        tim_sort(arr, visualize_array)
    
    # Show final sorted array
    visualize_array(arr)
    st.session_state.array = arr
    st.success("Sorting Complete!")

# Add explanation section
st.markdown("---")
st.header("How it works")
st.markdown("""
This visualization shows different sorting algorithms in action:
- **Bubble Sort**: Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.
- **Selection Sort**: Divides the array into a sorted and unsorted region, repeatedly finds the minimum element in the unsorted region and adds it to the sorted region.
- **Quick Sort**: Uses a divide-and-conquer strategy, selecting a 'pivot' element and partitioning the array around it.
- **Insertion Sort**: Builds the final sorted array one item at a time, by repeatedly inserting a new element into the sorted portion of the array.
- **Merge Sort**: Divides the array into smaller subarrays, sorts them, and then merges them back together to form the final sorted array.
- **Heap Sort**: Creates a heap data structure from the array and repeatedly extracts the maximum element to build the sorted array.
- **Counting Sort**: Uses an auxiliary array to count occurrences of elements and reconstructs the sorted array.
- **Radix Sort**: Sorts numbers by processing individual digits, from least to most significant.
- **Bucket Sort**: Distributes elements into multiple buckets, sorts each bucket, and then merges them.
- **Shell Sort**: A variation of insertion sort that moves elements over larger gaps to improve efficiency.
- **Tim Sort**: A hybrid sorting algorithm combining merge sort and insertion sort for optimal performance.

Red bars indicate the elements being compared or swapped at each step.
""")