from data import runtests
from queue import PriorityQueue
import sys
sys.setrecursionlimit(100000)

def create_graph_adjency_list(vertex_num, edges):
    graph = [[] for _ in range(vertex_num)]
    for v1,v2, wage in edges:
        graph[v1-1].append([v2-1,wage])
        graph[v2-1].append([v1-1,wage])
    return graph

def Find_biconnected_components(N, graph):
    def DFS_visit(u):
        nonlocal Time
        nonlocal count
        children = 0
        disc[u] = Time
        low[u] = Time
        Time += 1

        for v, _ in graph[u]:
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))
                DFS_visit(v)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    count += 1
                    w = -1
                    while w != (u, v):
                        w = st.pop()
                        components[w[0]].add(count)
                        components[w[1]].add(count)
            elif v != parent[u] and low[u] > disc[v]:
                low[u] = min(low[u], disc[v])
                st.append((u, v))


    disc = [-1 for _ in range(N)]
    low = [-1 for _ in range(N)]
    parent = [-1 for _ in range(N)]
    st = []
    count = 0
    Time = 0
    components = [set() for _ in range(N)]
    for i in range(N):
        if disc[i] == -1:
            DFS_visit(i)
        if st:
            count = count + 1
            while st:
                w1, w2 = st.pop()
                components[w1].add(count)
                components[w2].add(count)
    return components

def modified_Dijkstra(start, graph, n, components):

    def under_arch(u, old):
        new = components[u]
        if len(new)==0 or len(old)==0:
            return 0, new
        intersection = new.intersection(old)
        if len(intersection) > 0:
            return 0, new
        else:
            return 1, new

    queue = PriorityQueue()
    visited = [False for _ in range(n)]
    transit_squares = [0 for _ in range(n)]
    distance = [float("inf") for _ in range(n)]
    last = set()
    queue.put((0, 0, start, last))
    distance[start] = 0
    while not queue.empty():
        t, d, v, last = queue.get()
        for u, wage in graph[v]:
            arch, comp = under_arch(u, last)
            if (not visited[u]) and transit_squares[u] >= t - arch and distance[u] > wage + d:
                transit_squares[u] = t - arch
                distance[u] = wage + d
                queue.put((transit_squares[u], distance[u], u, components[v]))
        visited[v] = True
    return transit_squares, distance

def my_solve(N, streets):
    print(f"Place: {N}, ulice: {len(streets)}")
    graph = create_graph_adjency_list(N,streets)
    components = Find_biconnected_components(N, graph)

    transit_squares = set()
    for i in range(N):
        if len(components[i]) > 1:
            transit_squares.add(i)

    ending_points = set()
    for ts in transit_squares:
        for start, _ in graph[ts]:
            ending_points.add(start)

    result = (0,0)
    for start in ending_points:
        arches, distances = modified_Dijkstra(start, graph, N, components)
        for end in ending_points:
            result = min(result, (arches[end], distances[end]))
    return -result[0], result[1]

runtests(my_solve)
