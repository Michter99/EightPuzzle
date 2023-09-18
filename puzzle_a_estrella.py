import copy
from typing import List, Tuple

MATRIX_SIZE = 3


class Node:
    def __init__(self):
        self.parent = None
        self.mat = []
        self.x_empty = 0
        self.y_empty = 0
        self.cost = 0
        self.num_movements = 0
        self.heuristic_cost_num_mov = 0


class PuzzleAEstrella:
    def __init__(self):
        self.node_found = None

    def new_node(
        self,
        matrix: List[List[int]],
        x_empty_parent: int,
        y_empty_parent: int,
        x_empty_new: int,
        y_empty_new: int,
        parent: Node,
        cost: int,
        num_movements: int,
    ) -> Node:
        new_node = Node()
        new_node.parent = parent
        new_node.x_empty = x_empty_new
        new_node.y_empty = y_empty_new
        new_node.cost = cost
        new_node.num_movements = num_movements
        new_node.heuristic_cost_num_mov = cost + num_movements
        new_node.mat = copy.deepcopy(matrix)
        (
            new_node.mat[x_empty_parent][y_empty_parent],
            new_node.mat[x_empty_new][y_empty_new],
        ) = (
            new_node.mat[x_empty_new][y_empty_new],
            new_node.mat[x_empty_parent][y_empty_parent],
        )
        return new_node

    def calculate_current_state_cost(
        self, initial_state: List[List[int]], final_state: List[List[int]]
    ) -> int:
        cost = sum(
            initial_state[i][j] != final_state[i][j]
            for i in range(MATRIX_SIZE)
            for j in range(MATRIX_SIZE)
        )
        return cost

    def is_position_valid(self, x: int, y: int) -> bool:
        return 0 <= x < MATRIX_SIZE and 0 <= y < MATRIX_SIZE

    def find_initial_empty_cell_coordinates(
        self, initial_state: List[List[int]]
    ) -> Tuple[int, int]:
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if initial_state[i][j] == 0:
                    return i, j
        return -1, -1

    def is_in_ancestors(self, parent_node: Node, child_state: List[List[int]]) -> bool:
        while parent_node:
            if self.calculate_current_state_cost(parent_node.mat, child_state) == 0:
                return True
            parent_node = parent_node.parent
        return False

    def get_node_with_lowest_heuristic(self, agenda: List[Node]) -> Node:
        min_node = min(agenda, key=lambda x: x.heuristic_cost_num_mov)
        agenda.remove(min_node)
        return min_node

    def exists_node_with_lower_cost(self, agenda: List[Node]) -> bool:
        for i, node in enumerate(agenda):
            if node.heuristic_cost_num_mov < self.node_found.heuristic_cost_num_mov:
                return True
            else:
                del agenda[i]
        return False

    def generate_movement_route(
        self, found_node_route: Node, flag: int = 0
    ) -> List[List[List[int]]]:
        if flag == 0:
            found_node_route = self.node_found
        if not found_node_route:
            return []
        path = self.generate_movement_route(found_node_route.parent, 1)
        path.append(found_node_route.mat)
        return path

    def solve_8_puzzle(
        self, initial_state: List[List[int]], final_state: List[List[int]]
    ) -> Tuple[bool, List[List[List[int]]]]:
        # bottom, left, up, right
        row = [1, 0, -1, 0]
        column = [0, -1, 0, 1]

        agenda = []
        x_initial, y_initial = self.find_initial_empty_cell_coordinates(initial_state)
        self.node_found = self.new_node(
            initial_state,
            x_initial,
            y_initial,
            x_initial,
            y_initial,
            None,
            self.calculate_current_state_cost(initial_state, final_state),
            0,
        )
        agenda.append(self.node_found)

        while agenda:
            self.node_found = self.get_node_with_lowest_heuristic(agenda)
            if self.calculate_current_state_cost(self.node_found.mat, final_state) != 0:
                for i in range(4):
                    if self.is_position_valid(
                        self.node_found.x_empty + row[i],
                        self.node_found.y_empty + column[i],
                    ):
                        temp_mat_child = copy.deepcopy(self.node_found.mat)
                        (
                            temp_mat_child[self.node_found.x_empty][
                                self.node_found.y_empty
                            ],
                            temp_mat_child[self.node_found.x_empty + row[i]][
                                self.node_found.y_empty + column[i]
                            ],
                        ) = (
                            temp_mat_child[self.node_found.x_empty + row[i]][
                                self.node_found.y_empty + column[i]
                            ],
                            temp_mat_child[self.node_found.x_empty][
                                self.node_found.y_empty
                            ],
                        )
                        if not self.is_in_ancestors(self.node_found, temp_mat_child):
                            child_node = self.new_node(
                                self.node_found.mat,
                                self.node_found.x_empty,
                                self.node_found.y_empty,
                                self.node_found.x_empty + row[i],
                                self.node_found.y_empty + column[i],
                                self.node_found,
                                self.calculate_current_state_cost(
                                    temp_mat_child, final_state
                                ),
                                self.node_found.num_movements + 1,
                            )
                            agenda.append(child_node)
            else:
                if not self.exists_node_with_lower_cost(agenda):
                    solution_steps = self.generate_movement_route(self.node_found)
                    return True, solution_steps
        return False, []
