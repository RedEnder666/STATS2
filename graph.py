import matplotlib.pyplot as plt


def graphic(lst, view=3):
    lst = [i for i in lst if i is not None]
    coords = [[], []]
    for i in sorted(list(set(lst))):
        coords[0].append(lst.count(i))
        coords[1].append(i)
    if view in [1, 3]:
        plt.plot(coords[1], coords[0])
    if view in [2, 3]:
        plt.scatter(coords[1], coords[0], c='black')
    plt.style.use('seaborn-whitegrid')

    plt.title('Полигон частот')
    plt.ylabel('m')
    plt.xlabel('X')

    plt.grid(True)

    plt.show()
