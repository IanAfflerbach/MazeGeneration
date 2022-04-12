conda create -n [env_name] python==3.7

conda activate [env_name]

ND:
generator.py --- used to create a maze
output types: .txt (saves maze data for solution), .png, & .mp4

solver.py --- used to solve a given maze
output types: .png, & .mp4


2D:
generator algorithms: prims, kruskals, recursive_backtrack, ellers, hunt_and_kill
solver algorithms   : recursive_dfs, bfs, deadend_filling

3D & 4D:
generator algorithms: prims, kruskals, recursive_backtrack
solver algorithms   : recursive_dfs, bfs