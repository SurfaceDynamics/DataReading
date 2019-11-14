import mainGUI
import plotGenerator
import threading

gui = mainGUI.MainGUI()
plotter = plotGenerator.PlotGenerator(gui)
def GUI():
    gui.Initiation()
    gui.Render()
def PLOTTER():
    plotter.Plot()


def main():
    thread_1 = threading.Thread(target=GUI)
    thread_2 = threading.Thread(target=PLOTTER)

    thread_1.start()
    thread_2.start()

if __name__ == "__main__":
    main()

