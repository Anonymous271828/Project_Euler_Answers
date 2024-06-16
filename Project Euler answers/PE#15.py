def paths(grid, path, x, y, all_paths):
    grid_h = len(grid)-1
    grid_l = len(grid[0])-1
    path.append(grid[y][x])
    if grid[y][x] == 400:
        #print(path)
        all_paths.append(path)
        return 0
    #path.append(grid[y][x])
    #print(path, x , y)
    if x + 1 <= grid_l:
        paths(grid, path, x + 1, y, all_paths)
        path.pop(len(path) - 1)
    if y + 1 <= grid_h:
        paths(grid, path, x, y + 1, all_paths)
        path.pop(len(path) - 1)
    #print(path)
path = []
all_paths = []
x = 0
y = 0
achieve = 20
p = 0
a = []
g = [x for x in range(1, achieve**2 + 1)]
for num in g:
    if num % achieve == 0:
        a.append(g[p:num])
        p = num
#print(a)
paths(a, path, x, y, all_paths)
print(len(all_paths))