from tkinter import CENTER, Canvas, Tk

from boid import BoidManager

WIDTH, HEIGHT = 800, 600


def main():
    root = Tk()
    root.title("Boids")
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack(anchor=CENTER, expand=True)

    boid_manager = BoidManager(canvas)
    boid_manager.update_boids()

    root.mainloop()


if __name__ == "__main__":
    print("Running Boid Simulation")
    main()
    print("Exiting Program")
