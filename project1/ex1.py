"""
FYS-STK4155 @UiO, PROJECT I. 
Exercise 1: Ordinary least squares
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

from utils import plot_3d
from utils import franke_function
from utils import sample_franke_function
from utils import plot_franke_function
from utils import design_matrix
from utils import OLS

np.random.seed(2021)

SHOW_PLOTS = True
NOISE = .1
TEST_SIZE = .2
DEGREE = 5


# DATA. Uniform. Noise. Train-Test split.
N = 200
X, Y = sample_franke_function(N, noise=NOISE)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=TEST_SIZE)


# PLOT. Train & test data.
if SHOW_PLOTS:
    ax = plot_3d()
    plot_franke_function(ax)
    ax.scatter3D(*X_train.T, Y_train, label="Train data")
    ax.scatter3D(*X_test.T, Y_test, label="Test data")
    ax.set_title("Sampling Franke's function.")
    plt.legend()
    plt.tight_layout()
    plt.show()


# OLS. Design matrix.
X_train_ = design_matrix(X_train, degree=DEGREE)
X_test_ = design_matrix(X_test, degree=DEGREE)

model = OLS().fit(X_train_, Y_train, confidence=.95)


# PLOT. Prediction. 2D & 3D.
if SHOW_PLOTS:
    n = 50
    x = np.linspace(0, 1, n)
    x, y = np.meshgrid(x, x)
    mgrid = np.column_stack((x.reshape(-1), y.reshape(-1)))
    X_ = design_matrix(mgrid, degree=DEGREE)
    # 2D.
    fig, axs = plt.subplots(nrows=1, ncols=2)
    axs[0].imshow(franke_function(x, y))
    axs[1].imshow((model.predict(X_)).reshape(n, n))
    axs[0].set_title("Franke's function.")
    axs[1].set_title("Prediction.")
    plt.tight_layout()
    plt.show()
    # 3D.
    ax = plot_3d()
    plot_franke_function(ax)
    ax.scatter3D(*X_test.T, model.predict(X_test_), c="red")
    ax.plot_wireframe(
        x, y, (model.predict(X_)).reshape(n, n),
        color="r",
        label="Prediction",
        alpha=.3,
    )
    ax.set_title("Predicting Franke's function.")
    plt.legend()
    plt.tight_layout()
    plt.show()


# SCORES. MSE & R2.
model.score(X_test_, Y_test)
print("--- SCORES ---")
print(f"MSE (Train): {model.mse_train:.4f}")
print(f"MSE (Test): {model.mse_test:.4f}")
print(f"R2 (Train): {model.r2_train:.4f}")
print(f"R2 (Test): {model.r2_test:.4f}")


# PLOT. Confidence intervals.
if SHOW_PLOTS:
    devs = .5 * (model.CI[:, 1] - model.CI[:, 0])
    plt.errorbar(range(len(model.beta)), model.beta, yerr=devs, fmt='o')
    plt.title(r"OLS estimation $\beta$.")
    plt.xticks(np.arange(len(model.beta)))
    plt.ylabel(r"$\beta_j \pm \hat{\sigma} \sqrt{(X^{\top}X)^{-1}_{jj}}$", size=14)
    plt.xlabel(r"$j$", size=14)
    plt.tight_layout()
    plt.show()