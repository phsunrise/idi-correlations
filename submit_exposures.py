import os, sys, time

nprocs = 45
for rank in range(nprocs):
    with open("job_%03d.sbatch"%rank, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("#SBATCH --job-name=job_%03d\n"%rank)
        f.write("#SBATCH --output=job_%03d.out\n"%rank)
        f.write("#SBATCH --error=job_%03d.err\n"%rank)
        f.write("#SBATCH --time=3:00:00\n")
        f.write("#SBATCH --qos=normal\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --ntasks-per-node=1\n")
        if rank == nprocs-1:
            f.write("#SBATCH --mail-type=END\n")
            f.write("#SBATCH --mail-user=phsun@stanford.edu\n")
        f.write("\n")
        f.write("python exposures.py -s %d\n"%(rank*100+500))

    os.system("sbatch job_%03d.sbatch" % rank)
    time.sleep(1)
