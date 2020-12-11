import numpy as np
import matplotlib.pyplot as plt
# import decorators as deco
import sys, getopt
import os


# @deco.dir_active(__file__)
def main(log_path: str, plot_names=None, scale_names=None):
    """
    Displays columns from a csv file as a plot. Specific columns can be selected from header names
    :param log_path: path to csv file
    :param plot_names: list containing header names of columns to plot. Default all
    :param scale_names: list containing scale factors for each column.
    :return: None
    """
    with open(log_path, 'r') as log_file:
        names = log_file.readline().strip().split(',')
    plot_names = names if plot_names is None else plot_names
    scale_names = [1 for _ in plot_names] if scale_names is None else scale_names

    data = np.genfromtxt(log_path, delimiter=',', names=names, skip_header=1)  # Read CSV file

    time = data['time']  # Extract time column
    names.remove('time')

    plt.figure()  # Create figure

    # Plot selected variables
    plotted_names = []
    for name in names:
        if name in plot_names:  # Ignore typo in plot_names
            plotted_names.append(name)
            index = plot_names.index(name)  # Find index of current name in plot_names list
            scale = scale_names[index]      # Extract scale corresponding to name
            y = [d * scale for d in data[name]]  # Scale values in column
            plt.plot(time, y)  # Add data vs time to plot
    plt.grid()
    plt.legend(plotted_names)
    plt.xlabel('Time [s]')
    plt.ylabel('Value')
    plt.show()


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    def parse():
        """
        Function for parsing commandline arguments and options
        :return: filename, kwargs
        """
        kwarguments = {}

        def help_func(*help_args):
            print(f"python log-viewer.py <opts> <args>\n"
                  f"    opts:\n"
                  f"        -n: String with variable names to plot i.e 'var1, var2, var3'\n"
                  f"        -s: String with scales for plotted variables i.e '1, 10, 2'\n"
                  f"        -h: Help\n"
                  f"    args:\n"
                  f"        filename (is assumed to be located in 'logs/'relative to script)")
            exit(0)

        def n(names):
            kwarguments['plot_names'] = [text.strip() for text in names.strip().split(',')]

        def s(scales):
            kwarguments['scale_names'] = [float(text.strip()) for text in scales.strip().split(',')]

        try:
            opt_dict = {'-h': help_func, '-n': n, '-s': s}
            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, 'hn:s:', ['plotnames=', 'scalenames='])
            for opt, arg in opts:
                opt_dict[opt](arg)
            filename = args[0]
            return filename, kwarguments
        except IndexError as e:
            print(f'{e}: Has the filename been supplied?')
            help_func()
        except getopt.GetoptError as e:
            print(f'{e}')
            help_func()

    file, kwargs = parse()
    main(f'logs/{file}', **kwargs)
