import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np

class Charts():
    
    def __init__(self, data):
        self.data = data
        self.color = sb.color_palette()[0]
   #plot_pie
 
        
    def plot_hist(self, col):
         
        bin_min = self.data[col].min()
        bin_max = self.data[col].max()
            
        bin_step = round((bin_max-bin_min)/10, 2)    
            
        bin_max_new = bin_min + 10*bin_step
        
        plt.figure(figsize=[14.70, 8.27])
        
        bin_edges = np.arange(bin_min, bin_max+bin_step, bin_step)
        plt.hist(data=self.data, x=col, bins=bin_edges)

        plt.xlabel("{}".format(col))
        plt.ylabel('Count')
        plt.title("Distribution of {}".format(col))
        plt.xticks(np.arange(bin_min, bin_max_new, bin_step))
        plt.show()
        

    def plot_scatter(self, xcol, ycol, hue = None):
        plt.figure(figsize=[14.70, 8.27])
        sb.scatterplot(data=self.data, x=xcol, y=ycol, hue=hue)
        plt.title('{} by {}'.format(ycol, xcol))
        plt.show()
        
    def plot_bar(self, xcol, ycol, func):
        plt.figure(figsize=[14.70, 8.27])

        counts = self.data.groupby(xcol)[ycol].agg(func).reset_index()
        sb.barplot(x=xcol, y=ycol, data=counts, color=self.color)
        plt.xlabel(xcol)
        plt.ylabel('{} of {}'.format(func, ycol))
        plt.title('{} of {} per {}'.format(func, ycol, xcol))
        plt.show()

    def plot_count(self, xcol, hue = None):
        plt.figure(figsize=[14.70, 8.27])

        sb.countplot(data=self.data, x=xcol, hue=hue, color=self.color)
        plt.xlabel(xcol)
        plt.ylabel('Count')
        plt.title('Count of {}'.format(xcol))
        plt.show()
        
        
    def plot_line(self, xcol, ycol, hue = None):
        plt.figure(figsize=[14.70, 8.27])
        sb.pointplot(data=self.data, x=xcol, y=ycol, hue = hue)
        plt.xlabel(xcol)
        plt.ylabel(ycol)
        plt.title("{} per {}".format(ycol, xcol))
        plt.show()        

    def plot_box(self, xcol, ycol):
        plt.figure(figsize=[14.70, 8.27])
        sb.boxplot(data=self.data, x=xcol, y=ycol, color=self.color)
        plt.xlabel(xcol)
        plt.ylabel(ycol)
        plt.title("{} per {}".format(ycol, xcol))
        plt.show() 
        
        
    def plot_violin(self, xcol, ycol):
        plt.figure(figsize=[14.70, 8.27])
        sb.violinplot(data=self.data, x=xcol, y=ycol, color=self.color)
        plt.xlabel(xcol)
        plt.ylabel(ycol)
        plt.title("{} per {}".format(ycol, xcol))
        plt.show() 
        
        
    def plot_bar_with_line(self, xcol, bar_col, line_col, bar_func, line_func):
        fig, ax1 = plt.subplots(figsize=[14.70, 8.27])
        
        counts = df.groupby(xcol).agg({bar_col: bar_func, line_col: line_func}).reset_index()
        
        base_color = sb.color_palette()[0]
        
        color = 'tab:red'
        
        a = sb.barplot(data=counts[[xcol, bar_col]],
               x=xcol,
               y=bar_col,
               color=self.color,
               ax=ax1)
        
        a.set_xticklabels(a.get_xticks(), size=12)
        
        ax1.set_ylabel('{} of {}'.format(bar_func, bar_col), fontsize=15)
        ax2 = ax1.twinx()
        
        b = sb.pointplot(data=counts,
                 x=xcol,
                 y=line_col,
                 color=color, ax=ax2)
        ax2.set_ylabel('{} {} per {}'.format(line_func, line_col, xcol), fontsize=15)
        ax1.set_xlabel(xcol, fontsize=15)
        ax1.set_ylabel('{} per {}'.format(bar_func, xcol), fontsize=15)
        ax1.tick_params(labelrotation=45)
        ax1.set_title("{} distribution".format(xcol),
              fontsize=15)

        fig.tight_layout()
        plt.show()