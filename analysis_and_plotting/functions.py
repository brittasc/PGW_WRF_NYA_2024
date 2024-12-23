import seaborn as sns

def plotstyle_serif():
    sns.set_context('paper', font_scale=1.3)
    sns.set(font = 'Serif', font_scale = 1.3, )
    sns.set_style('ticks', 
                      {'font.family':'serif',
                       'grid.linestyle': '--',
                       'axes.grid': True,
                      }, 
                       )
    sns.set_palette("colorblind")
# plotstyle_serif()


def plotstyle_sansserif():
    sns.set_context('paper', font_scale=1.8)
    sns.set(font = 'Sans-serif', font_scale = 1.8, )
    sns.set_style('ticks', 
                      {'font.family':'sans-serif', 
                       'grid.linestyle': '--',
                       'axes.grid': True,
                      }, 
                       )
    sns.set_palette("colorblind")
# plotstyle_sansserif()
