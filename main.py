import numpy as np
import matplotlib.pyplot as plt


interval = 0.5, 5
func = lambda x: max(0.1, abs(abs(1/x-1)-0.5))

def get_all_integrals(f, dr, a,b):
    ints = dict()
    for i in range(FID):
        for j in range(i, FID):
            if i != j:
                lx = a + i * dr
                rx = a + j * dr
                if lx  > a + eps and rx  < b - eps:
                    ints[i,j] = abs(f((lx + rx) / 2)) * dr

    return ints

a,b = interval
r_max = b-a

FID = 1000
eps = 1 / (FID ** 1.5)


dr = r_max / FID
print("dr", dr)
print("eps", eps)
ints = get_all_integrals(func, dr, a, b)



def hl_maximal(f, x, interval):
    lw = dict()
    k = int((x-a) // dr)
    for i in range(FID):
        for j in range(FID):
            l = k - i
            r = k + j
            if (l,r) in ints:
                lw[(l,r)] = ints[(l,r)]
    
    best_int = max(lw, key=lambda x: lw[x])
    return best_int

fig, ax = plt.subplots()
x_values = np.linspace(*interval, FID)
y_values = np.array([func(x) for x in x_values])

ax.plot(x_values, y_values, label='$f(x)$', linestyle=":", c="pink")
ax.plot(x_values, abs(y_values), label='$|f(x)|$', linestyle="-", c="pink")
ax.grid(True)
ax.legend()

prev_line = None
prev_point = None
def on_click(event):
    global prev_line, prev_point
    if event.inaxes == ax:
        try:
            prev_line.pop(0).remove()
            prev_point.remove()
        except:
            pass
        click_x, click_y = event.xdata, event.ydata
        x0 = click_x
        l, r = hl_maximal(func, x0, interval)
        lx, rx = a + l * dr, a + r * dr
        print(f"Best interval at {x0}: {(lx,rx)}")
        xhf_values = np.linspace(lx, rx, FID)
        yhf_values = np.array([func(x) for x in xhf_values])
        prev_line = ax.plot(xhf_values, abs(yhf_values), label=f'Best interval', linestyle='-', c="k", linewidth=2)
        prev_point = ax.scatter(x0, abs(func(x0)))
        ax.legend()
        fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', on_click)

ro = None
def hover(event):
    global ro
    if event.inaxes == ax:
        try:
            ro.set_visible(False)
        except:
            pass
        x, _ = event.xdata, event.ydata
        if a<x<b:
            ro = plt.scatter(x, abs(func(x)), c="r")
        fig.canvas.draw_idle()

hid = fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
