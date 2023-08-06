# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 20:49:45 2023

@author: richie bao
migrated from: Isotonic Regression https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_isotonic_regression.html#sphx-glr-auto-examples-miscellaneous-plot-isotonic-regression-py
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LinearRegression
from sklearn.utils import check_random_state

def demo_isotonic_regression(n=100,figsize=(12, 6),markersize=12):
    x = np.arange(n)
    rs = check_random_state(0)
    y = rs.randint(-50, 50, size=(n,)) + 50.0 * np.log1p(np.arange(n))    
    
    ir = IsotonicRegression(out_of_bounds="clip")
    y_ = ir.fit_transform(x, y)
    
    lr = LinearRegression()
    lr.fit(x[:, np.newaxis], y)  # x needs to be 2d for LinearRegression    

    segments = [[[i, y[i]], [i, y_[i]]] for i in range(n)]
    lc = LineCollection(segments, zorder=0)
    lc.set_array(np.ones(len(y)))
    lc.set_linewidths(np.full(n, 0.5))
    
    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=figsize)
    
    ax0.plot(x, y, "C0.", markersize=markersize)
    ax0.plot(x, y_, "C1.-", markersize=markersize)
    ax0.plot(x, lr.predict(x[:, np.newaxis]), "C2-")
    ax0.add_collection(lc)
    ax0.legend(("Training data", "Isotonic fit", "Linear fit"), loc="lower right")
    ax0.set_title("Isotonic regression fit on noisy data (n=%d)" % n)
    
    x_test = np.linspace(-10, 110, 1000)
    ax1.plot(x_test, ir.predict(x_test), "C1-")
    ax1.plot(ir.X_thresholds_, ir.y_thresholds_, "C1.", markersize=markersize)
    ax1.set_title("Prediction function (%d thresholds)" % len(ir.X_thresholds_))
    
    plt.show()
    
    return x,y,ir