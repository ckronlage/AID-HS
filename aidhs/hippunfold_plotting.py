''' These functions were create by Jordan DeKraker for the visualisation of hippocampal surfaces from HippUnfold
    They are part of the hippunfold_toolbox https://github.com/jordandekraker/hippunfold_toolbox '''


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale.  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().'''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    return ax



def cdata_vertex_to_face(c,faces):
    '''Interpolates vertex data to the nearest face
    Input
      c: vertex data
      faces: face data'''
    if len(c.shape)>1:
        cf = np.zeros([len(faces),c.shape[1]])
        for f in range(len(faces)):
            cf[f,:] = np.mean(c[faces[f],:],axis=0)
    else:
        cf = np.zeros(len(faces))
        for f in range(len(faces)):
            cf[f] = np.mean(c[faces[f]])
    return cf



def window_cdata(cdata,cutoff=0.05):
    '''Returns upper and lower X percent interval values
    Input
      cdata: list of values
      cutoff: upper and lower percentile'''
    if not cutoff:
        return False
    l = np.sort(cdata.flatten())
    return l[[int(cutoff*len(l)), int((1-cutoff)*len(l))]]



def surfplot_cdata(ax,cdat,f,v,cwindow=False,cmap=False):
    '''create surface in existing axis
    Input
      ax: axis (of type subplot_kw={'projection': "3d"})
      cdata: color of surface
      f: faces
      v: vertices
      cwindow: whether to narrow the window of cdata [True,False, or Tuple for custom window]
      cmap: whether to use a custom colormap [Nx3 where N is the number of unique cdat values]'''
    cdata = cdata_vertex_to_face(cdat,f)
    # make window if needed
    if type(cwindow) == type(True):
        if not cwindow:
            norm = plt.Normalize(np.min(cdata), np.max(cdata)) 
        elif cwindow: # use default
            norm = plt.Normalize(window_cdata(cdata)[0],window_cdata(cdata)[1]) 
    else: # hard set window
        norm = plt.Normalize(cwindow[0],cwindow[1]) 
    # set colours if needed
    if type(cmap) == type(False):
        colors = plt.cm.viridis(norm(cdata))
    else:
        colors = np.zeros([len(cdat),cmap.shape[1]])
        u,i = np.unique(cdat,return_index=True)
        for ii in range(len(u)):
            colors[cdat==u[ii],:] = cmap[ii,:]
        colors = cdata_vertex_to_face(colors,f)
    
    pc = art3d.Poly3DCollection(v[f], facecolors=colors)
    ax.add_collection(pc)

    ax.set_xlim([np.min(v[:,0]),np.max(v[:,0])])
    ax.set_ylim([np.min(v[:,1]),np.max(v[:,1])])
    ax.set_zlim([np.min(v[:,2]),np.max(v[:,2])])
    ax.view_init(elev=90, azim=-90)
    ax = set_axes_equal(ax)
    ax.set_axis_off()
    return ax
