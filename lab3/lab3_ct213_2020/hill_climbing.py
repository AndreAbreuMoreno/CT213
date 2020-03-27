from math import inf


def hill_climbing(cost_function, neighbors, theta0, epsilon, max_iterations):
    """
    Executes the Hill Climbing (HC) algorithm to minimize (optimize) a cost function.

    :param cost_function: function to be minimized.
    :type cost_function: function.
    :param neighbors: function which returns the neighbors of a given point.
    :type neighbors: list of numpy.array.
    :param theta0: initial guess.
    :type theta0: numpy.array.
    :param epsilon: used to stop the optimization if the current cost is less than epsilon.
    :type epsilon: float.
    :param max_iterations: maximum number of iterations.
    :type max_iterations: int.
    :return theta: local minimum.
    :rtype theta: numpy.array.
    :return history: history of points visited by the algorithm.
    :rtype history: list of numpy.array.
    """
    theta = theta0
    history = [theta0]
    # Todo: Implement Hill Climbing

    count = 0

    while (count < max_iterations) and (cost_function(theta)> epsilon):
        best = None
        for neighbor in neighbors(theta):
            if best is None:
                best = neighbor
            cost_best = cost_function(best)

            if cost_function(neighbor) < cost_best:
                best = neighbor
                cost_best = cost_function(best)

        if cost_best > cost_function(theta):
            return theta, history

        theta = best
        history.append(theta)
        count += 1

    return theta, history
