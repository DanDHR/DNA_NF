import os
import re
import csv
import math

base_dir = "."

ENERGY_PATTERNS_SAME_LINE = {
    "EPtot": r'EPtot\s*=\s*([-+]?\d*\.\d+|\d+)',
    "Etot":  r'Etot\s*=\s*([-+]?\d*\.\d+|\d+)',
    "EKtot": r'EKtot\s*=\s*([-+]?\d*\.\d+|\d+)',
}

ENERGY_PATTERNS_NEXT_LINE = {
    "Bond":  r'Bond\s*=\s*([-+]?\d*\.\d+|\d+)',
    "Angle": r'Angle\s*=\s*([-+]?\d*\.\d+|\d+)',
}

def read_all_energies_filtered(base_dir="."):

    all_keys = list(ENERGY_PATTERNS_SAME_LINE.keys()) + list(ENERGY_PATTERNS_NEXT_LINE.keys())
    all_energies = {k: [] for k in all_keys}

    seq_folders = sorted(
        [d for d in os.listdir(base_dir)
         if d.startswith("S") and os.path.isdir(os.path.join(base_dir, d))],
        key=lambda x: int(x[1:])
    )

    for seq in seq_folders:
        seq_number = int(seq[1:])
        seq_path = os.path.join(base_dir, seq)

        mdout_filename = f"md{seq_number}.out"
        mdout_path = os.path.join(seq_path, mdout_filename)

        if not os.path.exists(mdout_path):
            print(f"No {mdout_filename} in {seq}")
            continue

        print(f"Reading: {mdout_path}")


        file_energies = {k: [] for k in all_keys}
    
        with open(mdout_path, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            m_ep = re.search(ENERGY_PATTERNS_SAME_LINE["EPtot"], line, re.IGNORECASE)
            if not m_ep:
                continue

            ep_val = float(m_ep.group(1))


            if abs(ep_val) <= 1000:
                continue

            #Store EPtot
            file_energies["EPtot"].append(ep_val)

            #Etot, EKtot on the same line (case-insensitive)
            for key, pattern in ENERGY_PATTERNS_SAME_LINE.items():
                if key == "EPtot":
                    continue
                m = re.search(pattern, line, re.IGNORECASE)
                if m:
                    file_energies[key].append(float(m.group(1)))

            #Bond, Angle on the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                for key, pattern in ENERGY_PATTERNS_NEXT_LINE.items():
                    m = re.search(pattern, next_line, re.IGNORECASE)
                    if m:
                        file_energies[key].append(float(m.group(1)))

        for key, values in file_energies.items():
            filtered = [
                v for j, v in enumerate(values)
                if (j % 51) != 50
            ]
            all_energies[key].extend(filtered)

    return all_energies


energies = read_all_energies_filtered(base_dir)

for key, arr in energies.items():
    print(key, len(arr))




output_file = "energies.csv"

max_len = max(len(v) for v in energies.values())


fieldnames = list(energies.keys())


with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(fieldnames)


    for i in range(max_len):
        row = []
        
        for key in fieldnames:
            vals = energies[key]
            
            if i < len(vals):
                row.append(vals[i])
            else:
                row.append("")  
        writer.writerow(row)

print(f"Saved energies to {output_file}")