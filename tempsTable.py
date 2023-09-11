import matplotlib.pyplot as plt
import pandas as pd
import time
import matplotlib.animation as animation

def update_table(file):
    data = pd.read_csv(file)


    def animate():
        fig, ax= plt.subplots(figsize=(7,1))

        ax.axis('off')
        table = ax.table(cellText=[data.iloc[0].values], colLabels=data.columns,bbox=[0, 0, 1, 1], loc='center',
                          cellLoc='center',fontsize=6)
        fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.95)
        table.auto_set_font_size(False)
        def update(frame):
            row = data.iloc[frame].tolist()
            table.auto_set_font_size(False)
            for i in range(len(row)):
                table._cells[(1, i)]._text.set_text(str(row[i]))
                table._cells[(0, i)]._text.set_fontsize(6)
                table._cells[(1, i)]._text.set_fontsize(10)              
            return table,

        ani = animation.FuncAnimation(fig, update, frames=len(data), interval=3000, repeat=False)
        return ani, fig

    my_anim, fig = animate()
    
    return my_anim, fig
    