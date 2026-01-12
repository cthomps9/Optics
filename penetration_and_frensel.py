# -*- coding: utf-8 -*-
"""

This script reads experimentally measured pixel distances from an Excel file, converts them into physical distances, and computes the corresponding
angles of incidence for a TIRF microscopy geometry. Using these angles, it calculates the evanescent field penetration depth as a function of 
incidence angle and plots penetration depth versus angle. The code then computes Fresnel reflectance and resulting excitation intensity versus 
angle, generating and saving plots that quantify how both penetration depth and excitation intensity vary with incidence angle.

Created on Tue Oct  8 15:10:33 2024

@author: thompson.3962
"""
import numpy as np
import pandas as pd

#folder location
folocal = 'D:/20240310_Using the lens again with different angles_NA 1.49/Attempt 2/2/'
#folocal = 'D:/20240310_Using the lens again with different angles_NA 1.49/Attempt 2/1/'
# Load the Excel file
df = pd.read_excel('D:/20240310_Using the lens again with different angles_NA 1.49/Attempt 2/2/Values.xlsx', sheet_name='Values')
#df = pd.read_excel('D:/20240310_Using the lens again with different angles_NA 1.49/Attempt 2/1/Values.xlsx', sheet_name='Values')


# Extract a specific column (e.g., 'ColumnName')
column_data_distance = df['Distance_(pixels)']
x_data = column_data_distance * 66
s_x = pd.Series(x_data)
# Convert the Series to a NumPy array
x_data = s_x.to_numpy()

true_range = len(x_data)

opp_list = []
for i in range(0, true_range):
    opp = ((x_data[i] * (1/6)))
    opp_list.append(opp)


alpha_list = []


flipped_data = np.flip(x_data, axis=0)

# Fill the list with numbers from 1 to 10
for i in range(0, true_range):
    alpha = np.arctan((opp_list[i]/flipped_data[i]))
    alpha_list.append(alpha)

alpha_list = np.array(alpha_list)


def penetration_depth(alpha, wavelength, n1, n2):
    """
    Calculate the penetration depth for TIRF microscopy.
    
    Parameters:
    alpha (float or np.array): Angle of incidence in radians.
    wavelength (float): Wavelength of the excitation light.
    n1 (float): Refractive index of the medium through which the light is traveling.
    n2 (float): Refractive index of the sample.
    
    Returns:
    float or np.array: Penetration depth.
    """
    return wavelength / (4 * np.pi * np.sqrt(n1**2 * np.sin(alpha)**2 - n2**2))

# Example usage
wavelength = 488e-9  # Wavelength in meters (e.g., 488 nm)
n1 = 1.51  # Refractive index of the medium (e.g., glass)
n2 = 1.33   # Refractive index of the sample (e.g., water)

# Calculate penetration_depth = []
penetration_depth_dp = []

# Fill the list with numbers from 1 to 10
for i in range(0, true_range):
    d_p = penetration_depth(alpha_list[i], wavelength, n1, n2)
    penetration_depth_dp.append(d_p)

# Print the list
print(penetration_depth_dp)
penetration_depth_dp = np.array(penetration_depth_dp)


# Print or plot the results
import matplotlib.pyplot as plt
new_alpha_list = np.degrees(alpha_list)
plt.plot(new_alpha_list, penetration_depth_dp * 1e9)  # Convert depth to nanometers for plotting
plt.xlabel('Angle of Incidence (degrees)')
plt.ylabel('Penetration Depth (nm)')
plt.title('Penetration Depth vs. Angle of Incidence')
plt.grid(True)
plt.savefig(folocal + 'Penetration Depth.png')  # You can change the file name and format as needed

plt.show()




def fresnel_reflectance(alpha, n1, n2):
    """
    Calculate the Fresnel reflectance for p-polarized light.
    
    Parameters:
    alpha (float or np.array): Angle of incidence in radians.
    n1 (float): Refractive index of the medium through which the light is traveling.
    n2 (float): Refractive index of the sample.
    
    Returns:
    float or np.array: Reflectance.
    """
    sin_alpha_t = n1 / n2 * np.sin(alpha)
    cos_alpha_t = np.sqrt(1 - sin_alpha_t**2)
    rs = (n1 * np.cos(alpha) - n2 * cos_alpha_t) / (n1 * np.cos(alpha) + n2 * cos_alpha_t)
    rp = (n2 * np.cos(alpha) - n1 * cos_alpha_t) / (n2 * np.cos(alpha) + n1 * cos_alpha_t)
    R = 0.5 * (rs**2 + rp**2)
    return R

def excitation_intensity(alpha, I_incident, n1, n2):
    """
    Calculate the excitation intensity for TIRF microscopy.
    
    Parameters:
    alpha (float or np.array): Angle of incidence in radians.
    I_incident (float): Incident light intensity.
    n1 (float): Refractive index of the medium through which the light is traveling.
    n2 (float): Refractive index of the sample.
    
    Returns:
    float or np.array: Excitation intensity.
    """
    R = fresnel_reflectance(alpha, n1, n2)
    return I_incident * (1 - R)

# Example usage
I_incident = 1.0  # Incident light intensity (arbitrary units)
n1 = 1.5  # Refractive index of the medium (e.g., glass)
n2 = 1.33   # Refractive index of the sample (e.g., water)

# Calculate excitation intensity
I0_alpha = excitation_intensity(alpha_list, I_incident, n1, n2)

# Plot the results
import matplotlib.pyplot as plt

plt.plot(new_alpha_list, I0_alpha)
plt.xlabel('Angle of Incidence (degrees)')
plt.ylabel('Excitation Intensity (arbitrary units)')
plt.title('Excitation Intensity vs. Angle of Incidence')
plt.grid(True)
plt.savefig(folocal + 'Excitation Intensity.png')  # You can change the file name and format as needed

plt.show()