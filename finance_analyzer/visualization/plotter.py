import matplotlib.pyplot as plt

def plot_indicator(df, indicator_series, title):
    fig, ax = plt.subplots()
    ax.plot(df["Year"], indicator_series, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel(title)
    return fig