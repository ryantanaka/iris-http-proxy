#!/usr/bin/env python

import os
from Pegasus.DAX3 import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create a abstract dag
dax = ADAG("TEST-WORKFLOW", auto=False)

# Add executable(s)
wc = Executable(name="wc", installed=False, arch=Arch.X86_64, os=OS.LINUX)
wc.addPFN(PFN(BASE_DIR + "/wc.sh", "local"))
dax.addExecutable(wc)

tar = Executable(name="tar", installed=True, arch=Arch.X86_64, os=OS.LINUX)
tar.addPFN(PFN("/usr/bin/tar", "condorpool"))
dax.addExecutable(tar)

# Add input files
if_1 = File("input_1.txt")
if_1.addPFN(PFN(BASE_DIR + "/inputs/input_1.txt", "local"))
dax.addFile(if_1)

if_2 = File("input_2.txt")
if_2.addPFN(PFN(BASE_DIR + "/inputs/input_2.txt", "local"))
dax.addFile(if_2)

if_3 = File("input_3.txt")
if_3.addPFN(PFN(BASE_DIR + "/inputs/input_3.txt", "local"))
dax.addFile(if_3)

if_4 = File("input_4.txt")
if_4.addPFN(PFN(BASE_DIR + "/inputs/input_4.txt", "local"))
dax.addFile(if_4)


# Add jobs
of = File("output.txt")
wc_job = Job(wc)
wc_job.addArguments(if_1, if_2, if_3, if_4, of)
wc_job.uses(if_1, link=Link.INPUT, transfer=False)
wc_job.uses(if_2, link=Link.INPUT, transfer=False)
wc_job.uses(if_3, link=Link.INPUT, transfer=False)
wc_job.uses(if_4, link=Link.INPUT, transfer=False)
wc_job.uses(of, link=Link.OUTPUT, transfer=True)
dax.addJob(wc_job)

final_of = File("final_output.tar.gz")
tar_job = Job(tar)
tar_job.addArguments("cvzf", final_of, if_1, if_2, if_3, if_4, of)
tar_job.uses(f_1, link=Link.INPUT, transfer=False)
tar_job.uses(f_2, link=Link.INPUT, transfer=False)
tar_job.uses(f_3, link=Link.INPUT, transfer=False)
tar_job.uses(f_4, link=Link.INPUT, transfer=False)
tar_job.uses(of, link=Link.INPUT, transfer=False)
tar_job.uses(final_of, link=Link.OUTPUT, transfer=True)
dax.addJob(tar_job)

# Add dependency
dax.addDependency(Dependency(parent=wc_job, child=tar_job))


# Write the DAX to a file
with open("workflow.xml", "w") as f:
    dax.writeXML(f)
