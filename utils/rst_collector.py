import os
import shutil

def collect_rst7_files(base_dir=".", out_dir="rst7"):
    os.makedirs(out_dir, exist_ok=True)

    seq_folders = sorted(
        [d for d in os.listdir(base_dir)
         if d.startswith("S") and os.path.isdir(os.path.join(base_dir, d))],
        key=lambda x: int(x[1:]) if x[1:].isdigit() else 10**9
    )

    copied = 0
    for seq in seq_folders:
        seq_path = os.path.join(base_dir, seq)

        rst7_files = [f for f in os.listdir(seq_path) if f.lower().endswith(".rst7")]
        if not rst7_files:

            continue

        for rst7_name in sorted(rst7_files):
            src = os.path.join(seq_path, rst7_name)

            base, ext = os.path.splitext(rst7_name)
            dst_name = f"{seq}_{base}{ext}"
            dst = os.path.join(out_dir, dst_name)

            shutil.copy2(src, dst)

            copied += 1

    print(f"\nDone. Copied {copied} rst7 file(s) into '{out_dir}/'.")


collect_rst7_files(base_dir=".", out_dir="rst7")
