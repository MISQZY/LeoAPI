from GUI.initialise_gui import App
import multiprocessing as mp

if __name__ == "__main__":
    mp.freeze_support()
    app = App()
    app.mainloop()