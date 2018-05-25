from simulacion import Simulacion
import gui

sim = Simulacion(10000, "pezoa", "humanos", 0.01, "2:2:2", "rodolfo", "muertos vivientes", 0.01, "2:2:2")
gui.set_size(1024, 680)
gui.run(sim.tick)
