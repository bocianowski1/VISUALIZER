def bubble_sort_mod(arr, i, j):
    n = len(arr)-1
    if i == n:
        return (arr, i, j)
    if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = swap(arr[j], arr[j+1])
    j += 1
    if j == n-i: 
        j = 0
        i += 1
    return (arr, i, j)

def swap(a, b):
    temp = a
    a = b
    b = temp
    return a, b


    