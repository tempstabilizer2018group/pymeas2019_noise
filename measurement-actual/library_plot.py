"""
There are three modes:

do_show=False,do_animate=False: No GUI. Just write the plot into a file.
do_show=True,do_animate=False: GUI. Show the data, no animation.
do_show=True,do_animate=True: GUI. Show the data, animation.

"""

import pathlib
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.animation

import library_topic


class PlotConext:
    def __init__(self, plotData, fig, ax):
        # The currently active presentation
        self.presentation = None
        # The data to be displayed
        self.plotData = plotData
        self.fig = fig
        self.ax = ax

    def initialize_plot_lines(self):
        for topic in self.plotData.listTopics:
            x, y = self.presentation.get_xy(topic)
            assert len(x) == len(y)
            (plot_line,) = self.ax.plot(x, y, linestyle="none", linewidth=0.1, marker=".", markersize=3, color=topic.color, label=topic.topic)
            scale = "log" if self.presentation.logarithmic_scales else "linear"
            self.ax.set_xscale(scale)
            self.ax.set_yscale(scale)
            topic.set_plot_line(plot_line)

        leg = self.ax.legend(fancybox=True, framealpha=0.5)
        leg.get_frame().set_linewidth(0.0)

    def update_presentation(self, presentation=None, update=True):
        if presentation is not None:
            self.presentation = presentation
            if self.plotData is not None:
                # The presentation changed, update the graph
                self.plotData.remove_lines(fig=self.fig, ax=self.ax)
                self.initialize_plot_lines()

        if update:
            assert self.plotData is not None
            plt.xlabel(self.presentation.x_label)
            plt.ylabel(f"{self.presentation.tag}: {self.presentation.y_label}")
            for topic in self.plotData.listTopics:
                topic.recalculate_data(presentation=self.presentation)
            for ax in self.fig.get_axes():
                ax.relim()
                ax.autoscale()
                plt.grid(True, which="major", axis="both", linestyle="-", color="gray", linewidth=0.5)
                plt.grid(True, which="minor", axis="both", linestyle="-", color="silver", linewidth=0.1)
                if self.presentation.logarithmic_scales:
                    ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, numticks=20))
                    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, numticks=20))
                # Uncomment to modify figure
                # self.fig.set_size_inches(13.0, 7.0)
                # ax.set_xlim(1e-1, 1e4)
                # ax.set_ylim(1e-9, 1e-5)
            self.fig.canvas.draw()

    def animate(self):
        if self.plotData.directories_changed():
            self.plotData.remove_lines_and_reload_data(self.fig, self.ax)
            self.initialize_plot_lines()
            # initialize_grid()
            return

        for topic in self.plotData.listTopics:
            topic.reload_if_changed(self.presentation)



def do_plots(**args):
    """
    Print all presentation (LSD, LS, PS, etc.)
    """
    for tag in library_topic.PRESENTATIONS.tags:
        do_plot(presentation_tag=tag, **args)


def do_plot(plotData, title=None, do_show=False, do_animate=False, write_files=("png", "svg"), write_files_directory=None, presentation_tag="LSD"):  # pylint: disable=too-many-arguments
    GLOBALS.update_presentation(library_topic.PRESENTATIONS.get(presentation_tag), update=False)

    if do_show or do_animate:
        import library_tk

        library_tk.initialize(plt)

    fig, ax = plt.subplots(figsize=(8, 4))
    GLOBALS.set(plotData, fig, ax)

    if title:
        plt.title(title)

    if do_show or do_animate:
        import library_tk

        library_tk.add_buttons(fig)

    GLOBALS.initialize_plot_lines()
    GLOBALS.update_presentation()

    if write_files_directory is None:
        # The current directory
        write_files_directory = pathlib.Path(__file__).parent

    for ext in write_files:
        filename = write_files_directory.joinpath(f"result_{GLOBALS.presentation.tag}.{ext}")
        print(filename)
        fig.savefig(filename, dpi=300)

    if do_show or do_animate:
        if do_animate:
            import library_tk

            def animate(i):
                if plotData.directories_changed():
                    plotData.remove_lines_and_reload_data(fig, ax)
                    GLOBALS.initialize_plot_lines()
                    # initialize_grid()
                    return

                for topic in plotData.listTopics:
                    topic.reload_if_changed(GLOBALS.presentation)

            _animation = library_tk.start_animation(fig=fig, func_animate=animate)
            # '_animation': This avoids the garbage collector to be called !?
        plt.show()

    fig.clf()
    plt.close(fig)
    plt.clf()
    plt.close()


