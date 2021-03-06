import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.finite_differences import ThreePoint
from src.utils import LABEL_SIZE, LEGEND_SIZE


def plot_3d():
    ax = plt.axes(projection='3d')
    ax.set_xlabel(r"$x$", size=LABEL_SIZE)
    ax.set_ylabel(r"$t$", size=LABEL_SIZE)
    ax.set_zlabel(r"$u(x,t)$", size=LABEL_SIZE, rotation=90)
    ax.view_init(elev=20., azim=25)
    ax.zaxis.set_rotate_label(False)
    return ax


# DATA.
T = .5
J = 500
N = lambda c, J: 2 * np.ceil(c * T * (J + 1)).astype(int)
space = np.linspace(0, 1, J + 2)
time = lambda c: np.linspace(0, T, N(c, J) + 1)

u0 = lambda x: np.where((0.3 < x) & (x < 0.6), 1, 0)


# FDM. Explicit Euler + 1. order upwind (FTBS).
fdm = ThreePoint((1, [-1, 1, 0]))
exact_sol_ = lambda c: fdm.solve(c, u0(space), space, time(c))


# EXACT SOLUTION.
X, T_ = np.meshgrid(space, time)


# PLOT. 3D.
c = 0.5
fdm.solve(c, u0(space), space, time(c))
X, T_ = np.meshgrid(space, time(c))
ax = plot_3d()
ax.plot_surface(X.T, T_.T, fdm.sol, alpha=.8, cmap="jet")
ax.plot_wireframe(
    space.reshape(-1, 1), np.zeros(space.size).reshape(-1, 1), u0(space).reshape(-1, 1), color="k", lw=2.5,
)
plt.tight_layout()
if not os.path.exists("project3/figs/"):
    os.makedirs("project3/figs/")
plt.savefig("project3/figs/adv_exact_1.pdf", bbox_inches='tight', format="pdf")
plt.show()

c = 2.0
fdm.solve(c, u0(space), space, time(c))
X, T_ = np.meshgrid(space, time(c))
ax = plot_3d()
ax.plot_surface(X.T, T_.T, fdm.sol, alpha=.8, cmap="jet")
ax.plot_wireframe(
    space.reshape(-1, 1), np.zeros(space.size).reshape(-1, 1), u0(space).reshape(-1, 1), color="k", lw=2.5,
)
plt.tight_layout()
if not os.path.exists("project3/figs/"):
    os.makedirs("project3/figs/")
plt.savefig("project3/figs/adv_exact_2.pdf", bbox_inches='tight', format="pdf")
plt.show()


# PLOT. 1D.
time_points = [.0, .05, .25, 0.5]
idx = [np.argmin(np.abs(time(c) - t)) for t in time_points]

color=plt.cm.jet(np.linspace(0, 1, len(time_points)))[::-1]
for i, (ix, t) in enumerate(zip(idx, time_points)):
    plt.plot(space, fdm.sol[:, ix], c=color[i], label=rf"$t={t:.2f}$")

plt.xlabel(r"$x$", size=LABEL_SIZE)
plt.ylabel(r"$u(x, t)$", size=LABEL_SIZE)
plt.legend(fontsize=LEGEND_SIZE)
plt.tight_layout()
if not os.path.exists("project3/figs/"):
    os.makedirs("project3/figs/")
plt.savefig("project3/figs/adv_diff_times.pdf", bbox_inches='tight', format="pdf")
plt.show()
