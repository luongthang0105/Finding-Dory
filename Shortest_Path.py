from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import tkinter as tk
import tkinter.messagebox as tkmsg
import math as m
import copy #this supports deepcopy, which is essential to "visualize" function!
import time
root = tk.Tk()

root.title("Shortest Path")
#frame & canvas
window = tk.Canvas(root)

bottom = tk.Frame(root)

plotWindow = tk.Frame(root)


bottom.pack(side = tk.BOTTOM, fill = tk.BOTH, expand=True) # fill = BOTH makes the Toolbar grows as the window gets bigger
window.pack(side = tk.BOTTOM)

map1_x_outer, map1_y_outer = [], []
adj_list, n = [], 0

ok, connecting = 0, 0
x1, x2, y1, y2 = 0,0,0,0
new_n = n
#------------------------GUI----------------------------
def create_map():
    figure = Figure(figsize=(5, 5))
    global a, canvas
    a = figure.add_subplot(111)
    a.grid()
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = tk.BOTH, expand=True)
    cid = figure.canvas.mpl_connect('button_press_event', mouse_event)

def dylit():
    global canvas, a
    canvas.get_tk_widget().forget()
    create_map()

def plot_graph():
    global a, n, canvas

    for i in range(0, n-1):
        x = [map1_x_outer[i], map1_x_outer[i+1]]
        y = [map1_y_outer[i], map1_y_outer[i+1]]
        a.plot(x, y , '-k', linewidth = 2)
    canvas.draw()

adj_list_temp = []

def visualize(isOn):
    global a, canvas, adj_list, ok, isFind, adj_list_temp, new_n
    
    if isOn == True:
        if(ok == 0):
            adj_list_temp = copy.deepcopy(adj_list)
            new_n = n
        for i in range(0, new_n-1):
            for j in range(i+1, new_n):
                '''
                if(i == 5 and j == 8):
                        print((map1_x_outer[i], map1_y_outer[i]))
                        print((map1_x_outer[j], map1_y_outer[j]))
                        print(adj_list_temp[i][j][0])
                '''
                if(adj_list_temp[i][j][0] == 2):
                    x = [map1_x_outer[i], map1_x_outer[j]]
                    y = [map1_y_outer[i], map1_y_outer[j]]
                    if(j < n):
                        a.plot(x, y , '-y', linewidth = 0.5)
                    else:
                        if j - n == 0:
                            a.plot(x, y, '-g', linewidth = 1)
                        else:
                            a.plot(x, y, '-r', linewidth = 1)
        canvas.draw()
    else:
        dylit()
        plot_graph()
        plot_points()
        if(ok >= 2): dijkstra()

def plot_points():
    
    if ok <= 2:
        if ok == 1:
            a.plot(x1, y1, marker="o", markersize=5, color = 'green')

        if ok == 2:
            a.plot(x1, y1, marker="o", markersize=5, color="green")
            a.plot(x2, y2, marker="o", markersize=5, color="red")

    else:
        if(ok % 2 == 1):
            a.plot(x1, y1, marker="o", markersize=5, color="green")
            a.plot(x2, y2, marker="o", markersize=5, color="red")
        else:
            a.plot(x1, y1, marker="o", markersize=5, color="green")
            a.plot(x2, y2, marker="o", markersize=5, color="red")
    canvas.draw()

#------------------------CALCULATE----------------------------

counter = 0
def intersect(Px, Py, Zx, Zy, i, j, point):
    Ax, Ay, Bx, By = map1_x_outer[i], map1_y_outer[i], map1_x_outer[j], map1_y_outer[j]
    #          A
    #  P ------|--------Z
    #          B
    PBx, PBy = Bx - Px, By - Py
    PZx, PZy = Zx - Px, Zy - Py
    PAx, PAy = Ax - Px, Ay - Py 

    AZx, AZy = Zx - Ax, Zy - Ay
    BZx, BZy = Zx - Bx, Zy - By

    area_PBZ = (PBx * PZy - PZx * PBy)
    area_PAZ = (PAx * PZy - PZx * PAy)

    area_PAB = (PBx * PAy - PBy * PAx)
    area_ABZ = (AZx * BZy - BZx * AZy)
    
    if (abs(abs(area_ABZ) + abs(area_PAB) - (abs(area_PBZ) + abs(area_PAZ))) < 1e-6) :
        if(area_PBZ * area_PAZ > 0):
            return 0
        if(area_PBZ * area_PAZ == 0):
            if(area_PBZ == area_PAZ == 0): #trường hợp 2 đường
                if(point == False): #nếu là đường thẳng thì tính, do trường hợp BC xen giữa AD thì AD ko tính: A  B-----C  D
                #                                                                |           |
                #                                                                -------------
                    return 1
                # nếu là điểm
                return 0
            else:
                diff_points = {(Ax,Ay), (Bx,By), (Px, Py), (Zx,Zy)}
                #trường hợp 2 đường có 1 điểm chung => ko cắt
                if(len(diff_points) != 4): #tất cả 4 điểm đều khác nhau
                    return 0
                return 1
        return 1
    return 0
def check_pip(x, y):
    cnt_vertical = 0
    eps = 1e-3
    for i in range(0, n-1):
        if(intersect(x,y+eps , 1000, y+eps, i, i+1, point = True) == 1):
            cnt_vertical += 1

    if(cnt_vertical % 2 == 1): return True
    else: return False


def dist(x1, y1, x2, y2):
    return m.sqrt((x1-x2)**2 + (y1-y2)**2)
#connect gồm: nối các điểm với nhau, trừ các cạnh có rồi


def printSolution(path, dist):
    global new_n
    end = new_n - 1
    start = new_n - 2
    while path[end] != -1: 
        x = [map1_x_outer[end], map1_x_outer[path[end]]]
        y = [map1_y_outer[end], map1_y_outer[path[end]]]

        a.plot(x, y , '-b', linewidth = 2.2)
        end = path[end]        
    
    canvas.draw()

def minDistance(dist, sptSet):
    global new_n
    min = 1e7
    for v in range(new_n):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
    return min_index


def dijkstra():
    global isFind, new_n, adj_list_temp, value
    if(isFind == False):
        dylit()
        plot_graph()
        plot_points()
        if isOn == True: visualize(isOn)
        return

    time_stamp_start = time.perf_counter()

    dist = [1e7] * new_n
    dist[new_n-2] = 0
    sptSet = [False] * new_n
    path = [-1] * new_n

    for _ in range(new_n):
        u = minDistance(dist, sptSet)

        sptSet[u] = True
        for v in range(new_n):
            if (adj_list_temp[u][v][0] != 0 and dist[v] > dist[u] + adj_list_temp[u][v][1] and sptSet[v] == False):
                dist[v] = dist[u] + adj_list_temp[u][v][1]
                path[v] = u

    printSolution(path,dist)

    time_stamp_end = time.perf_counter()

    dist_val = round(dist[new_n-1], 4)
    time_val = round(time_stamp_end-time_stamp_start, 4)
    value.set(dist_val)
    timer.set(time_val)

def event_point_connect():
    global a, n, canvas, adj_list, x1,y1,x2,y2, ok, isFind, adj_list_temp, new_n, isOn

    adj_list_temp = copy.deepcopy(adj_list)
    new_n = n
    
    x1_list, x2_list = [], []

    if(ok == 1): 
        new_n = n+1
        map1_x_outer[n], map1_y_outer[n] = x1, y1
    else: 
        new_n = n+2
        map1_x_outer[n], map1_y_outer[n] = x1, y1
        map1_x_outer[n+1], map1_y_outer[n+1] = x2, y2

    for i in range(0, new_n):
        cnt_x1, cnt_x2 = 0, 0
        for j in range(0, n-1):
            cnt_x1 += intersect(x1, y1, map1_x_outer[i], map1_y_outer[i], j, j+1, point = False)
            if(ok >= 2):
                cnt_x2 += intersect(x2, y2, map1_x_outer[i], map1_y_outer[i], j, j+1, point = False)
        
        connected_x1, connected_x2 = 0, 0
        if cnt_x1 == 0: connected_x1 = 2
        x1_list.append((connected_x1, dist(map1_x_outer[i],map1_y_outer[i], x1, y1)))
        
        if ok >= 2:
            if cnt_x2 == 0: connected_x2 = 2
            x2_list.append((connected_x2, dist(map1_x_outer[i],map1_y_outer[i], x2, y2)))

    
    adj_list_temp.append(x1_list)       
    
    if ok >= 2: 
        adj_list_temp.append(x2_list)       

    z = 0
    for i in range(0, n):
        for j in range(n, new_n):   
            adj_list_temp[i].append(adj_list_temp[j][i])

#------------------------GUI-2----------------------------
points = []
def mouse_event(event):
    global ok,x1,x2,y1,y2, isOn, isFind
    if(check_pip(event.xdata, event.ydata) == False):
        mssg = tkmsg.showerror("Error", "The point must be inside the maze!")
        return
        
    ok += 1
    if ok % 2 == 1: 
        x1 = event.xdata
        y1 = event.ydata
    else:
        x2 = event.xdata
        y2 = event.ydata

    if ok >= 2:
        event_point_connect()

    dylit()
    plot_graph()
    plot_points()
    visualize(isOn)
    if ok >= 2: dijkstra()

def MAP1():
    global ok, isOn, n, map1_y_outer, map1_x_outer, adj_list, isFind
    
    map1_x_outer = [2, 4, 4,6,6,7,7,11,11,13,13,11,11,5, 5, 8, 8, 2, 2, 0, 0]
    map1_y_outer = [15,15,4,4,3,3,4,4, 3, 3, 14,14,13,13,15,15,16,16,15,0, 0]

    n = len(map1_x_outer) - 2
    #2 điểm cuối là 2 slot dành cho 2 điểm click vào
    adj_list.clear()

    ok = 0
    isOn = isFind = False

    pre_proc()

    plot_graph()
    plot_points()
    visualize(isOn)

def MAP2():
    global ok, isOn, n, map1_y_outer, map1_x_outer, adj_list, isFind
    
    map1_x_outer = [1,15,15,7,7,4,4,3,3,8,8,9,9,11,11,2,2,12,12,13,13,8,8,15,15,4,4, 0, 0,3,3,7,7,2,2,0,0,1,  1,0,0]
    map1_y_outer = [1,1, 2, 2,3,3,2,2,4,4,3,3,4,4, 5, 5,6,6, 3, 3, 7, 7,8,8, 9, 9,10,10,9,9,8,8,7,7,8,8,7,7,  1,0,0]

    n = len(map1_x_outer) - 2
    #2 điểm cuối là 2 slot dành cho 2 điểm click vào
    adj_list.clear()

    ok = 0
    isOn = isFind = False
    pre_proc()

    plot_graph()
    plot_points()
    visualize(isOn)


isOn = False
def connect():
    global isOn

    if(isOn == False):
        isOn = True
        visualize(isOn)
    else:
        isOn = False
        visualize(isOn)

isFind = False
def Find_path():
    global isFind

    if(isFind == False):
        if(ok < 2):
            mssg = tkmsg.showerror("Error", "We need 2 points in the maze to execute!")
            return
        isFind = True
        dijkstra()
    else:
        isFind = False
        dijkstra()

#butt
button_Map1 = tk.Button(plotWindow, text = "MAP 1", command = lambda:MAP1()).grid(row=0, column=0, padx=10)
button_Map2 = tk.Button(plotWindow, text = "MAP 2", command = lambda:MAP2()).grid(row=0, column=1, padx=10)
button_Visualize = tk.Button(plotWindow, text = "Visualize", command = lambda:connect()).grid(row=0, column=2, padx=10)
button_Find_Path = tk.Button(plotWindow, text = "Find", command = lambda:Find_path()).grid(row=0, column=3, padx=10)

value = tk.StringVar()
distance_outp = tk.Label(plotWindow, textvariable=value).grid(row=0, column=5)
distance_lab = tk.Label(plotWindow, text="Distance: ").grid(row=0, column=4)

timer = tk.StringVar()
timer_outp = tk.Label(plotWindow, textvariable=timer).grid(row=0, column=7)
timer_lab = tk.Label(plotWindow, text="Time: ").grid(row=0, column=6)

create_map()
plotWindow.pack(side = tk.TOP)


def pre_proc():
    global adj_list, map1_x_outer, map1_y_outer, n
    for i in range(0, n):
        temp = []
        for j in range(0, n):
            temp.append((0, 0))
        adj_list.append(temp)
    
    adj_list[0][n-1] = adj_list[n-1][0] = (1, dist(map1_x_outer[0], map1_y_outer[0],map1_x_outer[n-1], map1_y_outer[n-1]))
    for i in range(0, n-1):
        adj_list[i][i+1] = adj_list[i+1][i] = (1, dist(map1_x_outer[i], map1_y_outer[i], map1_x_outer[i+1], map1_y_outer[i+1]))
    
    for i in range(0, n-1):
        for j in range(i+1, n):
            if(adj_list[i][j][0] == 0):
                midx, midy = (map1_x_outer[i] + map1_x_outer[j]) / 2,  (map1_y_outer[j] + map1_y_outer[i]) / 2
                cnt_inter = 0
                
                
                for z in range(0, n-1):
                    temp = intersect(map1_x_outer[i], map1_y_outer[i], map1_x_outer[j], map1_y_outer[j], z, z+1, point = False)
                    cnt_inter += temp
                    if(i == 0 and j == 3 and temp == 1): print(z)
                    
                if(cnt_inter > 0): continue

                if(check_pip(midx, midy) == False): continue

                adj_list[i][j] = adj_list[j][i] = (2,dist(map1_x_outer[i], map1_y_outer[i], map1_x_outer[j], map1_y_outer[j]))

root.mainloop()
