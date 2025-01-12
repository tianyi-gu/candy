def get_state_key(piles):
    """
    Convert a list of piles into a hashable tuple, sorted to handle equivalent states.
    
    Args:
        piles (list): List of integers representing candy piles
        
    Returns:
        tuple: A sorted tuple representation of the piles
    """
    return tuple(sorted(piles))