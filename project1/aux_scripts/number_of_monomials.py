import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils import LEGEND_SIZE, LABEL_SIZE

MAX_DEGREE = 20
degrees = np.arange(MAX_DEGREE)

plt.plot(degrees, degrees + 1, "-o", label="Homogen")
plt.plot(degrees, (degrees + 1) * (degrees + 2) / 2,   "-o", label="Inhomogen")
plt.xlabel(r"Polynomial degree $d$", size=LABEL_SIZE)
plt.ylabel("Number of monomials", size=LABEL_SIZE)
plt.legend(fontsize=LEGEND_SIZE)
plt.tight_layout()
if not os.path.exists("project1/figs/"):
    os.makedirs("project1/figs/")
plt.savefig("project1/figs/number_of_monomials.pdf", bbox_inches='tight', format="pdf")
plt.show()
