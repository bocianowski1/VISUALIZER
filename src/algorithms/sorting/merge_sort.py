def merge_sort(arr, low, high):
    if low > high:
        return
    
    mid = (low + high) / 2
    merge_sort(arr, low, mid)
    merge_sort(arr, mid + 1, high)
    merge(arr, low, mid, high)

def merge():
    pass