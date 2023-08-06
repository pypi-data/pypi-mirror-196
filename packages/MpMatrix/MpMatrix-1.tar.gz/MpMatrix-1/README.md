# MpMatrix

MpMatrix is a programming library which supports matrices containing mpmath's mpf objects.

# MpMatrix Operations

The operations supported by MpMatrix are addition, subtraction, and multiplication.

# Addition

**Input:** MpMatrix([[5, 6]]) + MpMatrix([[2, 8]])
**Output:** MpMatrix([[7, 14]])

# Subtraction

**Input:** MpMatrix([[5, 6]]) - MpMatrix([[4, 3]])
**Output:** MpMatrix([[1, 3]])

# Multiplication

**Input:** MpMatrix([[1, 2], [3, 4]]) * MpMatrix([[4, 3], [2, 1]])
**Output:** MpMatrix([[8, 5], [20, 13]])

# Comparisons

**Input:** MpMatrix([[1, 2], [3, 4]]) == MpMatrix([[1, 2], [3, 4]])
**Output:** True

**Input:** MpMatrix([[1, 2], [3, 4]]) == MpMatrix([[1, 2], [3, 5]])
**Output:** False (not all corresponding entries are equal)

**Input:** MpMatrix([[1, 2], [3, 4]]) == MpMatrix([[4, 3], [2, 1]])
**Output:** False (same entries used but in different positions)

