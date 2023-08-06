from . import _np
from . import _plt
from .dsp import sig2frames

def shift_factory(fig, shift=0.05):
    """shift <shift>% of current x axis with wheel, up-right down-left"""
    def shift_fun(event):
        # get axes where scroll event happened
        ax = event.inaxes
        if ax is None: # if outside axe 
            return
        x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
        for line in ax.get_lines():
            x = line.get_xdata()
            if event.button == 'up':
                # deal with shift right  
                x += shift*x_range
            elif event.button == 'down':
                # deal with shift left
                x -= shift*x_range
            # set new x data
            line.set_xdata(x)
        _plt.draw() # force re-draw
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',shift_fun)
    return shift_fun

def zoom_factory(fig, base_scale = 1.1):
    """zoom <base_scale> of current axes with wheel, up-zoom in down-zoom out"""
    def zoom_fun(event):
        """zoom when scrolling"""
        ax = event.inaxes
        scale_factor = _np.power(base_scale, -event.step)
        xdata = event.xdata
        ydata = event.ydata
        x_left = xdata - ax.get_xlim()[0]
        x_right = ax.get_xlim()[1] - xdata
        y_top = ydata - ax.get_ylim()[0]
        y_bottom = ax.get_ylim()[1] - ydata

        ax.set_xlim([xdata - x_left * scale_factor,
                        xdata + x_right * scale_factor])
        ax.set_ylim([ydata - y_top * scale_factor,
                        ydata + y_bottom * scale_factor])
        ax.figure.canvas.draw()

    fig.canvas.mpl_connect('scroll_event', zoom_fun)
    return zoom_fun

def hist2d_3d(x, y, bins_2d=(10,10), title="", xlabel="", ylabel=""):
    # https://stackoverflow.com/questions/8437788/how-to-correctly-generate-a-3d-histogram-using-numpy-or-matplotlib-built-in-func/
    x = _np.array(x)   #turn x,y data into numpy arrays
    y = _np.array(y)

    fig = _plt.figure()          #create a canvas, tell matplotlib it's 3d
    ax = fig.add_subplot(111, projection='3d')

    #make histogram stuff - set bins - I choose 20x20 because I have a lot of data
    hist, xedges, yedges = _np.histogram2d(x, y, bins=bins_2d)
    xpos, ypos = _np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])

    xpos = xpos.flatten()/2.
    ypos = ypos.flatten()/2.
    zpos = _np.zeros_like (xpos)

    dx = xedges [1] - xedges [0]
    dy = yedges [1] - yedges [0]
    dz = hist.flatten()

    cmap = _plt.cm.get_cmap('jet') # Get desired colormap - you can change this!
    max_height = _np.max(dz)   # get range of colorbars so we can normalize
    min_height = _np.min(dz)
    # scale each z to [0,1], and get their rgb values
    rgba = [cmap((k-min_height)/max_height) for k in dz] 

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
    _plt.title(title)
    _plt.xlabel(xlabel)
    _plt.ylabel(ylabel)
    _plt.show()

    return fig