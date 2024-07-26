from tkinter import Canvas, Tk, ttk

from boid import BoidManager

WIDTH, HEIGHT = 1200, 675


class BoidSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Boids Simulation - github.com/alecthedev")
        self.canvas = None
        self.boid_manager = None

        self.build_gui()

    def build_gui(self):
        content = ttk.Frame(self.root)

        self.canvas = Canvas(content, width=WIDTH, height=HEIGHT, bg="black")

        boid_label = ttk.Label(content, text="Left-Click to add Boid")
        pred_label = ttk.Label(content, text="Right-Click to add Predator")

        content.grid(column=0, row=0)
        self.canvas.grid(column=0, row=0, columnspan=4, sticky="nsew")

        boid_label.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
        pred_label.grid(column=2, row=1, columnspan=2, padx=5, pady=5)

    def start_app(self):
        if self.canvas is None:
            raise ValueError("BoidManager requires Canvas to run simulation")
        self.boid_manager = BoidManager(self.canvas)
        self.boid_manager.update_boids()


if __name__ == "__main__":
    print("Running Boid Simulation")

    root = Tk()
    boid_sim = BoidSimulation(root)
    boid_sim.start_app()
    root.mainloop()

    print("Exiting Program")
