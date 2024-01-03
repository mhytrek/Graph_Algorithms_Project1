from data import runtests


def create_graph_adjency_list(vertex_num, edges):
    graph = [[] for _ in range(vertex_num)]
    for v1,v2, wage in edges:
        graph[v1-1].append((v2-1,wage))
        graph[v2-1].append((v1-1,wage))
    return graph

def find_articulation_points(vertex_num, graph):

    def DFS_low(vertex, parent, graph, visited, dv, points):
        visited[vertex] = dv
        low = dv
        dv = dv + 1
        test = False
        for neighour, _ in graph[vertex]:
            if neighour == parent:
                continue
            if visited[neighour] != 0 and visited[neighour] < low:
                low = visited[neighour]
                continue
            if visited[neighour] == 0:
                temp = DFS_low(neighour, vertex, graph, visited, dv, points)
                if temp < low:
                    low = temp
                if temp >= visited[vertex]:
                    test = True
        if test:
            points.append(vertex)
        return low


    visited = [0 for _ in range(vertex_num)]
    points = []
    for vertex in range(vertex_num):
        if visited[vertex] > 0:
            continue
        dv = 2
        nc = 0
        visited[vertex] = 1
        for neighbour, _ in graph[vertex]:
            if visited[neighbour] > 0:
                continue
            nc = nc + 1
            DFS_low(neighbour, vertex, graph, visited, dv,points)
        if nc > 1:
            points.append(vertex)
    return points


def find_biconnected_components(vertex_num, graph, articulation_points):

    def DFS(vertex, id):
        visited[vertex] = True
        components[vertex] = id
        for neighbour in graph[vertex]:
            if not visited[neighbour]:
                DFS(neighbour, id)
        return


    components = {}
    index = 0
    visited = [True if i in articulation_points else False for i in range(vertex_num)]
    for vertex in range(vertex_num):
        if not visited[vertex]:
            DFS(vertex, index)
            index += 1
    return components


def modified_Dijkstra():


def my_solve(N, streets):
    print(f"Place: {N}, ulice: {len(streets)}")
    graph = create_graph_adjency_list(N,streets)
    transit_squares = find_articulation_points(N, graph)
    check_if_under_arch = find_biconnected_components(N, graph, transit_squares)

    return 0, 0

runtests(my_solve)
