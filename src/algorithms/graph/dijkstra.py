import heapq
import numpy as np

graph = [
    [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
    [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
    [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
    [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
    [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
    [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
    [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
    [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
    [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
    [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
]

def dijkstra(graph, source):
    visited = np.array([[False for col in row] for row in graph])
    dist = np.array([[np.inf for col in row] for row in graph])
    prev = np.array([[None for col in row] for row in graph])
    directions = np.array([(0, 1), (1, 0), (-1, 0), (0, -1)])

    dist[source[0]][source[1]] = 0
    n, m = len(graph), len(graph[0])
    
    min_heap = []
    heapq.heappush(min_heap, (dist[source[0]][source[1]], source[0], source[1]))

    while len(min_heap) != 0:
        curr = heapq.heappop(min_heap)
        dist_from_src, row, col = curr
        if visited[row][col]: continue

        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if (-1 < new_row < n) and (-1 < new_col < m) and not visited[new_row][new_col]:
                dist_to_new = dist_from_src + graph[new_row][new_col]

                if dist_to_new < dist[new_row][new_col]:
                    dist[new_row][new_col] = dist_to_new
                    prev[new_row][new_col] = (row, col)
                    heapq.heappush(min_heap, (dist_to_new, new_row, new_col))

        visited[row][col] = True
        if graph[row][col] == 3: break

    return dist, prev, visited

def find_shortest_path(prev, to_find):
    shortest_path = []
    curr = to_find
    while curr is not None:
        shortest_path.append(curr)
        curr = prev[curr[0]][curr[1]]
    shortest_path.reverse()
    return shortest_path



def merge_sort(arr, low, high):
    if low > high:
        return
    
    mid = (low + high) / 2
    merge_sort(arr, low, mid)
    merge_sort(arr, mid + 1, high)
    merge(arr, low, mid, high)

def merge():
    pass



