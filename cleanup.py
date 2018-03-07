import os

print "deleting filelist_???.npy"
os.system("rm filelist_???.npy")

print "deleting job_???.sbatch .err .out"
os.system("rm job_???.sbatch")
os.system("rm job_???.err")
os.system("rm job_???.out")

print "deleting test.err .out"
os.system("rm test.err")
os.system("rm test.out")
