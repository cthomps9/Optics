# -*- coding: utf-8 -*-
"""
Created on Thu May  1 16:17:47 2025

This code simulates a multi-lens optical system using the raytracing library, tracing rays from an object through two lenses and a tube lens to 
analyze their propagation. It defines the lens focal lengths, constructs the imaging path, and traces rays at specific input heights to calculate 
their output angles after the tube lens.

@author: thompson.3962
"""
from raytracing import *
import numpy as np

# Define focal lengths
f_obj = 175   # Lens 3
f_eye = 250    # Lens 4
f_tube = 30   # Tube lens

# Create the imaging path
path = ImagingPath()
path.label = "Leaving the SLM to the Telescope + Tube Lens"
path.objectHeight = 2  # For ray drawing purposes
path.rayNumber = 1     # Number of rays to display

# Append elements
path.append(Space(d=0))  # Light from object at infinity Index 0
path.append(Lens(f=f_obj, label="Lens 3"))  #index 1
path.append(Space(d=f_obj + f_eye)) #index 2
path.append(Lens(f=f_eye, label="Lens 4"))  #index3
path.append(Space(d=650))   #index 4
path.append(Lens(f=f_tube, label="Tube Lens")) #index 5
path.append(Space(d=30)) #index 6

# --- Ray angle diagnostics ---
# Create specific rays for angle extraction
rays_input = [Ray(y=y, theta=0.6714) for y in [-50, -2.5, 0, 2.5, 50]]

# Trace and print angles after the tube lens
print("Angles (in degrees) of rays after the tube lens:")
tube_lens_index = len(path.elements) - 2  # tube lens position

for ray in rays_input:
    traced = path.trace(ray)
    ray_after = traced[len(path.elements) - 1]  # After tube lens
    angle_deg = np.degrees(ray_after.theta)
    print(f"Input y={ray.y:.1f} mm → Output angle: {angle_deg:.4f}°")

# --- Show system diagram ---
path.display()
