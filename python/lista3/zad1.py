

def transpose(m, n):
    return [" ".join([m[i].split()[j] for i in range(len(m))]) for j in range(n)]


matrix = ["1.1 2.2 3.3", "4.4 5.5 6.6", "7.7 8.8 9.9"]
n = len(matrix[0].split())

print(matrix)
print(transpose(matrix, n))
