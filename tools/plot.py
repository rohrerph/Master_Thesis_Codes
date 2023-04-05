import matplotlib.pyplot as plt
def plot_layout(title, xlabel, ylabel, ax):

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(which='major', axis='y', linestyle='-', linewidth=0.5)
    ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5)
    ax.set_title(title)
    ax.legend()