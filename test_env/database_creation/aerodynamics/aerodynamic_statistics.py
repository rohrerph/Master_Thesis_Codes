import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from test_env.tools import plot

def calculate(savefig, folder_path):

    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.loc[data['Aspect Ratio']<=15] # Filter out 767-400 where a wrong value is set in the database
    data = data.dropna(subset=['Wingspan,float,metre', 'MTOW,integer,kilogram'])
    data.loc[data['Name'] == 'B787-800 Dreamliner', 'Height,float,metre'] = 16.92
    data.loc[data['Name'] == 'B787-900 Dreamliner', 'Height,float,metre'] = 17.02
    data.loc[data['Name'] == '787-10 Dreamliner', 'Height,float,metre'] = 17.02

    groups = [
        {'Group': 'Group I', 'Min Span': 0, 'Max Span': 15, 'Min Height': 0, 'Max Height': 6.1},
        {'Group': 'Group II', 'Min Span': 15, 'Max Span': 24, 'Min Height': 6.1, 'Max Height': 9.1},
        {'Group': 'Group III', 'Min Span': 24, 'Max Span': 36, 'Min Height': 9.1, 'Max Height': 13.7},
        {'Group': 'Group IV', 'Min Span': 36, 'Max Span': 52, 'Min Height': 13.7, 'Max Height': 18.3},
        {'Group': 'Group V', 'Min Span': 52, 'Max Span': 65, 'Min Height': 18.3, 'Max Height': 20.1},
        {'Group': 'Group VI', 'Min Span': 65, 'Max Span': 80, 'Min Height': 20.1, 'Max Height': 24.4}
    ]
    df = pd.DataFrame(groups)

    # Plot FAA Group Regulations for Airport Wingspan and Height
    fig, ax = plt.subplots(dpi=300)
    column_data1 = pd.to_numeric(data['YOI'], errors='coerce')
    norm = mcolors.Normalize(vmin=1959, vmax=2020)
    norm_column_data1 = norm(column_data1)
    # create a colormap and map normalized values to colors
    cmap = plt.colormaps.get_cmap('Reds')
    colors = cmap(norm_column_data1)

    colormap = plt.cm.get_cmap('Blues', len(df))

    for _, group in df[::-1].iterrows():
        x2, y2 = group['Max Span'], group['Max Height']

        square = patches.Rectangle((0, 0), x2, y2, linewidth=1, edgecolor=colormap(_), facecolor=colormap(_), label=group['Group'], alpha=0.7)
        ax.add_patch(square)
        ax.legend(loc='lower right')

    # Plotting Wingspan vs. MTOW
    ax.scatter(data['Wingspan,float,metre'], data['Height,float,metre'], color=colors, s=20)
    for i, row in data.iterrows():
        plt.annotate(row['Name'], (row['Wingspan,float,metre'], row['Height,float,metre']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Aircraft Release Year')

    plt.xlabel('Wingspan (m)')
    plt.ylabel('Height (m)')
    plt.title('FAA Aircraft Categorisation')
    plt.ylim(0,24.4)
    plt.xlim(0,80)
    plt.tight_layout()
    if savefig:
        plt.savefig(folder_path+ '/faa_wingspan_regulations.png')


    # Plot Aspect Ratio vs the Year of Release

    fig, ax = plt.subplots(dpi=300)


    # Plotting Wingspan vs. MTOW
    ax.scatter(data['YOI'], data['Aspect Ratio'], color='red', s=20)
    for i, row in data.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['Aspect Ratio']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

    xlabel = 'Year of Introduction'
    ylabel = 'Aspect Ratio'
    plot.plot_layout(None, xlabel, ylabel, ax)
    plt.tight_layout()
    if savefig:
        plt.savefig(folder_path+ '/aspectratio_vs_releaseyear.png')


