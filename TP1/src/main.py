from data_structures.SokobanState import SokobanState
from algorithm_picker import Algorithm
from heuristic_picker import Heuristic
from input import read_input
import time
import sys
import json

if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols, forbidden_points) = read_input(config["map"])

        SokobanState.map_limits = map_limits
        SokobanState.goal_points = goal_points
        SokobanState.max_rows = max_rows
        SokobanState.max_cols = max_cols
        if config["forbidden_points"] == "YES":
            SokobanState.forbidden_points = forbidden_points
        else:
            SokobanState.forbidden_points = set()
        state = SokobanState(None, 0, boxes_position, player_coord)

        solver = Algorithm.from_string(config["algorithm"])
        heuristic = Heuristic.from_string(config["heuristic"])
        solution = solver.solve(state, heuristic)

        if solution.is_valid():
            for curr in solution.build_solution():
                print(curr)
            print(solution.end_state.steps)
        else:
            print("There is no solution for the map")

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Visited Count: {solution.visited_count}")
        if solution.is_valid():
            print(f"End State Steps: {solution.end_state.steps}")
            print(f"Time of Execution: {execution_time:.2f} seconds")


