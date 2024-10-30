from typing import List, Any


def batch_splitter(data: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split a list of data into batches of a specified size.
    """
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
