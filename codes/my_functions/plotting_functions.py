import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

def set_fig_style(figsize_mm = (50, 35), font_scale = 1.0, style = 'ticks',context = 'notebook'):
    """Optimizes figure settings for publication.
    makes nice and standardized figures 
    
    Parameters:
    -----------
    figsize_mm: float
                figure size in millimeter (width, hight)
    font_scale: float
                scaled font size for all texts. If None then it uses parameters below.
    style     : str
                style of figure (white, dark, whitegrid, darkgrid, ticks)
    context   : str
                context of figure (paper, notebook, talk, poster)
    Raises:
    -------
    TypeError
        If fig_size or font_scale not number.
        if style or context not string
    
    Example:
    --------
    >>> set_fig_style(figsize_mm = (50, 35), font_scale = 1.0, style = 'ticks',context = 'notebook')
    """
    if not isinstance(figsize_mm, tuple):
        raise TypeError("figsize_mm must be a tuple i.e. (50,100) where 50 is width and 100 is height")
    
    if not isinstance(font_scale, (int, float)):
        raise TypeError("Fontscale must be a float or int")
        
    figsize_inches = (figsize_mm[0] / 25.4, figsize_mm[1] / 25.4)
    sns.set_style(style)  
    sns.set_context(context, font_scale=font_scale)
    mpl.rcParams["figure.figsize"] = figsize_inches  
    mpl.rcParams["savefig.dpi"] = 300  
    mpl.rcParams["font.family"] = "Arial" 
    mpl.rcParams["legend.frameon"] = False
    mpl.rcParams["legend.labelcolor"] = 'linecolor'
    mpl.rcParams["legend.handlelength"] = 0.5 
    mpl.rcParams["legend.handleheight"] = 0.5 
    mpl.rcParams["legend.loc"] = 'upper right'
    
    if font_scale == 0:
        mpl.rcParams["axes.labelsize"] = 16
        mpl.rcParams["axes.titlesize"] = 16
        mpl.rcParams["xtick.labelsize"] = 16
        mpl.rcParams["ytick.labelsize"] = 16
        mpl.rcParams["legend.fontsize"] = 16
        mpl.rcParams["axes.linewidth"] = 1.5  
        mpl.rcParams["legend.fontsize"] = 12
        
