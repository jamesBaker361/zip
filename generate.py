for step in [4,8,16]:
    for dir_n in [1,2]:
        for n_rows in [2,4,8]:
            for kernel_size in [3,5,7]:
                for cent in ["--use_centroids",""]:
                    name=f"{step}_{dir_n}_{n_rows}_{kernel_size}_{cent}".replace("--","_")
                    print(f"sbatch --out=slurm/horizon/trial_{name}.out --err=slurm/horizon/trial_{name}.err runpymain.sh horizon.py --step {step} --n_rows {n_rows} --kernel_size {kernel_size} {cent} --src_dir input_{dir_n} --output_dir output_{dir_n}_{name}")