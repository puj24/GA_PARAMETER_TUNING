import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation

# Function to convert RA, DEC, NCP to quaternion
def ra_dec_ncp_to_quaternion(ra, dec, ncp):
    try:
        ra_rad = np.deg2rad(ra)
        dec_rad = np.deg2rad(-dec)
        ncp_rad = np.deg2rad(ncp)

        r = Rotation.from_euler('ZYX', [ra_rad, dec_rad, ncp_rad])
        q = r.as_quat()
        return q
    except:
        return [np.nan, np.nan, np.nan, np.nan]  # Return empty quaternion if computation fails

# Load the Excel file
file_path = 'HILS_Quaternion.xlsx'  # Replace with your file path
sheet_name = 'JALNA'  # Replace with your sheet name if different

# Read specific ranges of columns L, M, N from the Excel file
df_ra = pd.read_excel(file_path, sheet_name=sheet_name, usecols='L', skiprows=4, nrows=53)
df_dec = pd.read_excel(file_path, sheet_name=sheet_name, usecols='M', skiprows=4, nrows=53)
df_ncp = pd.read_excel(file_path, sheet_name=sheet_name, usecols='N', skiprows=4, nrows=53)

# Rename the columns for easier manipulation
df_ra.columns = ['RA']
df_dec.columns = ['DEC']
df_ncp.columns = ['NCP']

# Create an empty DataFrame to store quaternion components with specific column names
df_quaternions = pd.DataFrame(columns=['q3_x', 'q3_y', 'q3_z', 'q4'])

# Apply the conversion function to compute quaternions and store them in DataFrame
for idx in range(len(df_ra)):
    quaternion = ra_dec_ncp_to_quaternion(df_ra.iloc[idx]['RA'], df_dec.iloc[idx]['DEC'], df_ncp.iloc[idx]['NCP'])
    df_quaternions = pd.concat([df_quaternions, pd.DataFrame([quaternion], columns=['q3_x', 'q3_y', 'q3_z', 'q4'])], ignore_index=True)

# Append the computed quaternion values (or empty rows if computation fails) to the existing sheet without overwriting
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    df_quaternions.to_excel(writer, index=False, sheet_name=sheet_name, startcol=14, startrow=5, header=False)
