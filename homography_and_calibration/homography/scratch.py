W=54.5
L=55.2
positions=list()
for row in range(0,5):
	positions.append(list())
	for column in range(0,5):
		positions[row].append((W*column,L*row))

for row in positions:
	print(row)