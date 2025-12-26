import os
import math

#Function to calculate distance between two 3D points
def calc_distance(vec1, vec2):
    #Euclidean distance in 3D
    dx = vec1[0] - vec2[0]
    dy = vec1[1] - vec2[1]
    dz = vec1[2] - vec2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


_1 = (35.681,  24.505,  23.290)    # Atom 31
_3 = (40.048,  34.853,  29.934)    # Atom 94
_38 = (32.381,  26.054, 122.155)   # Atom 944 (will move)
_39 = (35.537,  41.434, 125.112)   # Atom 947 (will move)
_74 = (23.890,  35.632,  31.678)   # Atom 1809
_76 = (32.135,  40.540,  24.699)   # Atom 1872

#Chain 1 and Chain 2 pairs
chain1_pairs = [
    (1872, 944),
    (1809, 944),
    (31, 944),
    (94, 944)
]

chain2_pairs = [
    (1872, 947),
    (1809, 947),
    (31, 947),
    (94, 947)
]

#Simulation parameters
num_files = 401      # total folders (0.00 Å to 100.00 Å in 0.25 Å steps)
step_size = 0.25     # Å per folder step
save_every = 100000  # save every 100,000 steps

for i in range(1, num_files + 1):
    folder_name = f"S{i}"
    os.makedirs(folder_name, exist_ok=True)

    #Move _38 and _39 along z-axis by 0.25 * step
    move_z = step_size * (i - 1)
    _38_moved = (_38[0], _38[1], _38[2] + move_z)
    _39_moved = (_39[0], _39[1], _39[2] + move_z)


    distances = {}

    #Chain 1
    chain1_coords = [(_76, _38_moved), (_74, _38_moved), (_1, _38_moved), (_3, _38_moved)]
    for idx, (a, b) in enumerate(chain1_coords):
        distances[f"chain1_{idx+1}"] = calc_distance(a, b)

    #Chain 2
    chain2_coords = [(_76, _39_moved), (_74, _39_moved), (_1, _39_moved), (_3, _39_moved)]
    for idx, (a, b) in enumerate(chain2_coords):
        distances[f"chain2_{idx+1}"] = calc_distance(a, b)

    #Right handler
    distances["right_handler"] = calc_distance(_38_moved, _39_moved)

    #Generate RST file
    stretch_filename = f"stretch{i}.RST"
    filepath_rst = os.path.join(folder_name, stretch_filename)
    content_lines = [f"! stretch{i} (step={i}) dynamic distances"]

    def format_rst(iat, dist):
        center = round(dist, 2)
        r2 = center - 0.5
        r3 = center + 0.5
        r1 = r2 - 5.0
        r4 = r3 + 5.0
        return (
            f"&rst\n"
            f"  iat={iat},\n"
            f"  r1={r1:.2f}, r2={r2:.2f}, r3={r3:.2f}, r4={r4:.2f},\n"
            f"  rk2=10.0, rk3=10.0,\n"
            f"/"
        )

    #Add Chain 1 and Chain 2
    for idx, pair in enumerate(chain1_pairs):
        content_lines.append(format_rst(f"{pair[0]},{pair[1]}", distances[f"chain1_{idx+1}"]))

    for idx, pair in enumerate(chain2_pairs):
        content_lines.append(format_rst(f"{pair[0]},{pair[1]}", distances[f"chain2_{idx+1}"]))


    content_lines.append(format_rst("944,947", distances["right_handler"]))


    with open(filepath_rst, "w") as f:
        f.write("\n".join(content_lines))

#Generate md.in
    md_content = f"""&cntrl
  imin=0,
  irest=1,
  ntx=5,
  nstlim=500000,
  dt=0.002,
  ntc=2,
  ntf=2,
  ntb=2,
  ntp=1,
  cut=12.0,
  ntt=1,
  temp0=300.0,
  ntwx={save_every},
  ntpr={save_every},
  ntwr={save_every},
  nmropt=1,
  ntr=1,
  restraint_wt=500.0,
  restraintmask='@31,94,1809,1872',
/
&wt type='DUMPFREQ', istep1=1000 /
&wt type='END' /
DISANG={stretch_filename}
DUMPAVE=distances{i}.dat
"""
    with open(os.path.join(folder_name, "md.in"), "w") as f:
        f.write(md_content)

print("Created 401 folders (0.25 Å step) with Chain1, Chain2, and right handler restraints only, saving 50 trajectory frames per simulation.")