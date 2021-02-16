
<p align="center">
  <img src="example_images/iqm_example.png">
</p>

# Disclaimer
This is a small personal project to get back in some OpenGL-Development without the hassle to compile anything in C++ or anything else. It's small side project which can load IQM-Files and display the animations by coding everything in Python directly. It probably doesnt have a use case as a real Engine since python is to slow for all the heavy math calculations (maybe if you use numpy instead of own classes). But anyway might be useful for someone who wants to understand the IQM-3D-File or for anything else. Beside that I will probably update the code from time to time, if i want to expand it. Note that it isn't commented at all since it's only for me hobby-wise but I though that it could be useful for someone and I want to use git to keep track of my progress :P



## Libraries
- numpy (I use it at for some testing, maybe it's still at some places in the code :P)
- ctypes
- Pyglet
- Python 3.91

## RUN
Just type in "python engine.py" and it should run. By default it will try to load "data/models/iqms/mrfixit/mrfixit.iqm" which is not provided in this repository, since I don't know if I'm allowed to. You can grab the Model from the [SDK](https://github.com/lsalzman/iqm) and place it at the named position.
