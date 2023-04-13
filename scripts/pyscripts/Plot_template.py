
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#Typeset LaTeX, e.g. plt.title(r'$\Gamma = 3$')
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"]}) 


def plotter(ax,x_data,y_data,size="30%"): 
    #region format axes
    divider = make_axes_locatable(ax)
    ax2 = divider.append_axes("bottom", size=size, pad=0.3)
    ax.figure.add_axes(ax2)
    #endregion

    #region Main plot
    # use ax.plot(...), ax.scatter(...), etc.
    #example:
    ax.scatter(x_data,y_data, marker='.')
    ax.plot(x_data,y_data,'r',linestyle = '--')
    #endregion

    #region Residuals
    # use ax2.plot(...), etc.
    # example: 
    ax2.errorbar(x_data,x_data,20,fmt= 'D',markerfacecolor = 'blue',markersize=4,markeredgecolor='red',ecolor="grey",capsize=4,label=",")
    #endregion


    #region formatting
    ax.set_title(r"Continuous Observation with Unknown Transit")
    ax.set_ylabel(r'Power (dB\*)')
    ax2.set_xlabel(r't (s)',loc = 'center')
    ax2.set_ylabel(r'Residuals')

    ax.grid(linestyle = '--', linewidth = 0.5)
    ax2.grid(linestyle = '--', linewidth = 0.5)
    ax2.set_xlim([min(x_data),max(x_data)])
    ax.legend()
    #endregion

# x = np.linspace(1,100,20) #example data
# y = np.random.rand(20,1) #example data
# plotter(axes,x,y)

# plt.tight_layout()
# #plt.savefig('example.png', dpi=500) #very high resolution, no svg required
# plt.show()
