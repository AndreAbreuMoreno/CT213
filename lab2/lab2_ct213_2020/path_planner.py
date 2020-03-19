from grid import Node, NodeGrid
from math import inf
import heapq


class PathPlanner(object):
    """
    Represents a path planner, which may use Dijkstra, Greedy Search or A* to plan a path.
    """
    def __init__(self, cost_map):
        """
        Creates a new path planner for a given cost map.

        :param cost_map: cost used in this path planner.
        :type cost_map: CostMap.
        """
        self.cost_map = cost_map
        self.node_grid = NodeGrid(cost_map)

    @staticmethod
    def construct_path(goal_node):
        """
        Extracts the path after a planning was executed.

        :param goal_node: node of the grid where the goal was found.
        :type goal_node: Node.
        :return: the path as a sequence of (x, y) positions: [(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)].
        :rtype: list of tuples.
        """
        node = goal_node
        # Since we are going from the goal node to the start node following the parents, we
        # are transversing the path in reverse
        reversed_path = []
        while node is not None:
            reversed_path.append(node.get_position())
            node = node.parent
        return reversed_path[::-1]  # This syntax creates the reverse list

    def dijkstra(self, start_position, goal_position):
        """
        Plans a path using the Dijkstra algorithm.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
		# Todo: implement the Dijkstra algorithm
        pq = []

        start = self.node_grid.get_node(start_position[0], start_position[1])
        goal = self.node_grid.get_node(goal_position[0], goal_position[1])

        start.f = 0
        heapq.heappush(pq,(start.f, start))

        while pq:
            f, node = heapq.heappop(pq)
            node.closed = True
            node_i, node_j = node.get_position()

            if node == goal:
                path_dijkstra = self.construct_path(goal)
                cost_dijkstra = goal.f
                self.node_grid.reset()
                return path_dijkstra, cost_dijkstra

            for successor in self.node_grid.get_successors(node_i, node_j):
                successor_node = self.node_grid.get_node(successor[0], successor[1])

                if not successor_node.closed:
                    if successor_node.f > node.f + self.cost_map.get_edge_cost(node.get_position(), successor_node.get_position()):
                        successor_node.f = node.f + self.cost_map.get_edge_cost(node.get_position(), successor_node.get_position())

                        successor_node.parent = node
                        heapq.heappush(pq, (successor_node.f,successor_node))


    def greedy(self, start_position, goal_position):
        """
        Plans a path using greedy search.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
		# Todo: implement the Greedy Search algorithm
        pq = []

        start = self.node_grid.get_node(start_position[0], start_position[1])
        goal = self.node_grid.get_node(goal_position[0], goal_position[1])

        start.g = start.distance_to(goal_position[0], goal_position[1])
        start.f = 0
        heapq.heappush(pq, (start.g, start))

        while pq:
            g, node = heapq.heappop(pq)
            node.closed = True
            node_i, node_j = node.get_position()

            for successor in self.node_grid.get_successors(node_i, node_j):
                successor_node = self.node_grid.get_node(successor[0], successor[1])

                if not successor_node.closed:
                    successor_node.closed = True
                    successor_node.parent = node
                    successor_node.f = node.f + self.cost_map.get_edge_cost(node.get_position(),successor_node.get_position())

                    if successor_node == goal:
                        path_greedy = self.construct_path(goal)
                        cost_greedy = goal.f
                        self.node_grid.reset()
                        return path_greedy, cost_greedy

                    successor_node.g = successor_node.distance_to(goal_position[0], goal_position[1])
                    heapq.heappush(pq,(successor_node.g, successor_node))



    def a_star(self, start_position, goal_position):
        """
        Plans a path using A*.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
		# Todo: implement the A* algorithm

        pq = []
        start = self.node_grid.get_node(start_position[0], start_position[1])
        goal = self.node_grid.get_node(goal_position[0], goal_position[1])

        start.g = 0
        start.f = start.distance_to(goal_position[0], goal_position[1])
        heapq.heappush(pq, (start.f, start))

        while pq:
            f, node = heapq.heappop(pq)
            node.closed = True
            node_i, node_j = node.get_position()

            if node == goal:
                path_a_star = self.construct_path(goal)
                cost_a_star = goal.f
                self.node_grid.reset()
                return path_a_star, cost_a_star

            for successor in self.node_grid.get_successors(node_i, node_j):
                successor_node = self.node_grid.get_node(successor[0], successor[1])
                if successor_node.f > node.g + self.cost_map.get_edge_cost(node.get_position(), successor_node.get_position())  + successor_node.distance_to(goal_position[0], goal_position[1]):
                    successor_node.g = node.g + self.cost_map.get_edge_cost(node.get_position(), successor_node.get_position())
                    successor_node.f = successor_node.g + successor_node.distance_to(goal_position[0], goal_position[1])
                    successor_node.parent = node
                    heapq.heappush(pq, (successor_node.f, successor_node))

