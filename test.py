global a
a = [1 , 2]
b = a

print(a)
print(b)

def print_list(List: list):
    List[0] = List[0] + 1
    print(f'{List[0]}')


print_list(a)

print(a)
print(b)