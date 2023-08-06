# Mixes the elements of multiple lists in a balanced manner based on their proportional lengths.

## pip install mixbalanced 

#### Tested against Windows 10 / Python 3.10 / Anaconda 



```python

    

    This function takes multiple lists as input and returns a new list that contains the elements of the input lists.
    The elements are combined in a balanced manner based on their proportional lengths. Longer lists contribute more
    elements to the resulting list.

    Parameters:
        *args: Variable-length argument list, containing multiple lists/tuples.

    Returns:
        list: A new list containing the elements from the input lists/tuples mixed in a balanced manner.

    Example:
        from mixbalanced import mix_balanced
        l1 = ["Antonio"] * 10
        l2 = ["Paulo"] * 5
        l3 = ["Anna"] * 15
        l4 = ["Maria"] * 3
        mix = mix_balanced(l1, l2, l3, l4)
        print(mix)
        Output: ['Anna', 'Antonio', 'Anna', 'Antonio', 'Paulo', 'Anna', 'Anna', 'Antonio', 'Anna', 'Maria',
                 'Anna', 'Antonio', 'Paulo', 'Anna', 'Antonio', 'Anna', 'Antonio', 'Paulo', 'Anna', 'Anna',
                 'Maria', 'Antonio', 'Anna', 'Antonio', 'Paulo', 'Anna', 'Anna', 'Antonio', 'Anna', 'Antonio',
                 'Paulo', 'Anna', 'Maria']
```