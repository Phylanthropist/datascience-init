memory = ['3', '4', '5', '6', '7', '8', '9', '1', '0', '4']
address = []
x = 0
while x < len(memory):
    for val in memory:
        address.append(val)
        x = +1

print(address)
