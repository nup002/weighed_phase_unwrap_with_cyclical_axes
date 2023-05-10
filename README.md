# Robust two-dimensional weighted and unweighted phase unwrapping that uses fast transforms and iterative methods

This branch is a work in progress to expand on Tobias A. de Jong's [original implementation](https://github.com/TAdeJong/weighed_phase_unwrap) 
for the purpose of adding support for optional cyclical axes, i.e. data which is wrapped around one or more axes.

Run `demo_unwrapper.py` to display a window showing the performance of the algorithm. 

It currently implements a function 'phase_unwrap_cyclical_axes' that assumes that all axes are cyclical. It is a 
work in progress due to unsolved problems when using weights.
