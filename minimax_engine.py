def minimax(position, depth, maximizing_player):
    if depth == 0 or is_terminal(position):
        return evaluate(position)

    if maximizing_player:
        max_eval = float('-inf')
        for child in get_children(position):
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for child in get_children(position):
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Example utility functions

def is_terminal(position):
    # Implement termination check
    pass

def evaluate(position):
    # Implement evaluation
    pass

def get_children(position):
    # Implement child generation
    pass

