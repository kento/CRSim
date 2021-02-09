import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def main():
    fname = './graph.csv'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    if not os.path.exists(fname):
        print('can NOT find %s!' % fname)
        exit(-1)

    fh = open( fname,  'r' )

    X = []
    Y = []
    Z = []
    xflag = True
    idx = 0
    title_str = ''
    for linedata in fh:
        linedata = linedata.strip()
        if len(linedata) > 1:
            split_data = linedata.split(',')
            if len(split_data) > 1:
                if split_data[0].find('max_ef') >= 0:
                    title_str = linedata.replace('max_ef', 'Maximum Efficiency')
                    title_str = title_str.replace('int', 'interval')
                    title_str = title_str.replace('L2_freq', 'L2ckpt_freq')
                elif xflag:
                    for i in range(len(split_data)):
                        if i == 0: continue
                        X.append(int(split_data[i]))
                    xflag = False
                else:
                    if len(split_data) > len(X):
                        for i in range(len(split_data)):
                            if i == 0:
                                Y.append(int(split_data[i]))
                                Z.append([])
                            else:
                                Z[idx].append(float(split_data[i]))
                        idx += 1
    fh.close()

    # create glaph
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X, Y = np.meshgrid(np.array(X), np.array(Y))
    Z = np.array(Z)
    #surf = ax.plot_surface(X, Y, Z, cmap='bwr', linewidth=0)
    #surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0)
    surf = ax.plot_surface(X, Y, Z, cmap='jet', linewidth=0, vmin=0, vmax=1)
    fig.colorbar(surf)
    ax.set_zlim3d(0, 1)
    ax.set_title(title_str)
    ax.set_xlabel('interval')
    ax.set_ylabel('L2ckpt_freq')
    ax.set_zlabel('Efficiency')

    plt.show()


if __name__  == "__main__":
    main()