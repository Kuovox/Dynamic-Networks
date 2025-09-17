graph [
  node [
    id 0
    label "0"
    bfs_distance_from_0 0
    bfs_path_from_0 "_networkx_list_start"
    bfs_path_from_0 "0"
  ]
  node [
    id 1
    label "1"
    bfs_distance_from_0 1
    bfs_path_from_0 "0"
    bfs_path_from_0 "1"
  ]
  node [
    id 2
    label "2"
    bfs_distance_from_0 2
    bfs_path_from_0 "0"
    bfs_path_from_0 "1"
    bfs_path_from_0 "2"
  ]
  node [
    id 3
    label "3"
    bfs_distance_from_0 3
    bfs_path_from_0 "0"
    bfs_path_from_0 "1"
    bfs_path_from_0 "2"
    bfs_path_from_0 "3"
  ]
  node [
    id 4
    label "4"
    bfs_distance_from_0 2
    bfs_path_from_0 "0"
    bfs_path_from_0 "1"
    bfs_path_from_0 "4"
  ]
  node [
    id 5
    label "5"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 1
    target 4
  ]
  edge [
    source 2
    target 3
  ]
  edge [
    source 3
    target 4
  ]
]
