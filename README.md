# Boid Simulation in Python3

A demonstration of emergent behavior in the form of flocking "bird-like objects" or *boids*.

![boids](https://github.com/user-attachments/assets/eb2ce641-41a7-444e-abef-149cc787b556)

See the *[Getting Started](https://github.com/alecthedev/tk-boids/edit/main/README.md#getting-started)* section below if you would like to try the simulation out for yourself.

## What's happening here?

There are essentially three rules that determine a boids behavior towards another boid:

1. Alignment
	* Adjust your heading according to the average heading of your neighbors.
2. Cohesion
	* Move toward the center of mass of your neighbors.
3. Separation
	* To avoid crowding, move away from any boid you get too close to.

A boid is only able to track boids within a certain distance. They do not know of boids far away. 

Additionally, they will avoid predators. An evade response is evoked when a predator comes within range of a boid, this is a stronger effect than the other behaviors. The predators themselves do not flock.

![pred_chase](https://github.com/user-attachments/assets/16cadbb8-cd48-4e67-9255-13a44d4c0bbb)


By combining all these factors, boids will demonstrate flocking behavior of all sizes and shapes. They can even avoid predators when they do not see one, as they respond to their neighbor's movements.

If you would like to learn more I encourage you to read the [Wikipedia entry](https://wikipedia.org/wiki/Boids). (Be careful - it's a rabbit hole!)
## Demos

Left-click to add new boids

![flocking_behavior](https://github.com/user-attachments/assets/bca176ea-8759-43e3-aa1f-efd5a36dd75f)

Right-click to add predators

![add_predator](https://github.com/user-attachments/assets/b3cc1f7a-a67e-48eb-b546-b536db344a2f)

## Getting Started

### Prerequisites:


* Knowledge of basic [CLI](https://en.wikipedia.org/wiki/Command-line_interface) usage
* [Python3](https://www.python.org/downloads/) (download page on python.org)
* Tkinter: 
	* When installing Python check "tcl/tk and IDLE" under optional features

#### 1. Clone this repository
```shell
git clone https://github.com/alecthedev/tk-boids.git
cd tk-boids
```

#### 2. Execute 'run.sh' to Start Program
```shell
./run.sh
``` 

#### 3. Tweaking Settings

* Currently there is no UI for tweaking the strength of the adjusments boids make. Any playing around must be done in your editor.

* In the boid.py file there is a dictionary in the Boid class called `self.adjustments` feel free to tweak these values to your liking. 
 
![screenshot.png](https://github.com/user-attachments/assets/c6ceda5a-b540-458d-acb9-d09005e8db03)

 
 ("randomness" makes slight adjustments for more organic boid movement)

---

Thanks for checking out my project, I hope you at least enjoyed the gifs if nothing else :)
