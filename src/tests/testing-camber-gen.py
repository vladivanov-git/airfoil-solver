import sys
sys.path.insert(0, r"C:\Users\vladi\airfoil-solver\src")

from airfoil_geometry.airfoil import Airfoil
import matplotlib.pyplot as mpl

my_airfoil = Airfoil("2412")
xu, yu, xl, yl = my_airfoil.generate_coords(100)

mpl.plot(xu, yu)
mpl.plot(xl, yl)
mpl.grid()
mpl.axis("equal")
mpl.show()
