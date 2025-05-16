# This '.py' file serves the purpose of extracting mosfet device parameters in a LTSpice compatible format.

# TO-DO: understand why it cannot be imported - has to do with the fact tha the python module starts with "1_"
import mosfet_device_characterisation as mosfet_char 

# Function to extract the Labmda modulation parameter (pclm @ BSIM3) from Id@Vd
# This function is a placeholder and needs to be implemented based on the specific lambda calculation method calculation method.
# 1) Have Id@Vds for multiple Vdg; 2) (optional) Extract the Overdrive voltage (Vov=Vgs - Vth) from the Id@Vds curve for each Vdg;
# 3) (TBD) Compute the derivative at each Vov point (tangent line) or from a point far from the Vov in the saturation regime (TBD
# 4) Find the intersect of the derivative on the negative x-axis for each tangent line;
# 5) The x-axis intercept will be equal to Vintercept = abs(1/lambda); 6) The lambda value is then equal to 1/abs(Vintercept);

def lambda_modulation(file_path):
    lambda_value = None

    return lambda_value