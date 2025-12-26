import os
import netCDF4 as nc
import numpy as np

base_dir = "." 

DNA_ATOMS = 1894 

all_coords_list = []
all_boxes_list  = []


seq_folders = sorted(
    [d for d in os.listdir(base_dir)
     if d.startswith("S") and os.path.isdir(os.path.join(base_dir, d))],
    key=lambda x: int(x[1:])
)

print(f"Found {len(seq_folders)} sequence folders.")

for seq in seq_folders:
    seq_path = os.path.join(base_dir, seq)

    # detect .nc file
    nc_files = [f for f in os.listdir(seq_path) if f.endswith(".nc")]
    if len(nc_files) == 0:
        print(f"⚠ No nc file found in {seq}")
        continue

    nc_file = os.path.join(seq_path, nc_files[0])
    print(f"Reading {nc_file}")

    traj = nc.Dataset(nc_file)

    coords = traj.variables["coordinates"][:] 
    try:
        box = traj.variables["cell_lengths"][:]  
    except:
        print(f"⚠ No box detected in {nc_file}, using zeros")
        box = np.zeros((coords.shape[0], 3))

    traj.close()

    if coords.shape[1] < DNA_ATOMS:
        raise ValueError(f"Trajectory {seq} has fewer than {DNA_ATOMS} atoms!")

    coords_dna = coords[:, :DNA_ATOMS, :]

    all_coords_list.append(coords_dna)
    all_boxes_list.append(box)

    print(f"Loaded {coords_dna.shape[0]} frames of DNA-only coordinates.")

all_coords = np.concatenate(all_coords_list, axis=0)
all_boxes  = np.concatenate(all_boxes_list, axis=0) 



print("coords:", all_coords.shape)
print("boxes: ", all_boxes.shape)

np.savez("all_traj_DNAonly.npz", coords=all_coords, boxes=all_boxes)
print("\nSaved DNA-only dataset to all_traj_DNAonly.npz")