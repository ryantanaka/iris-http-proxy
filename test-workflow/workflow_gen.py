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

# Add input file
_if = File("input.txt")
_if.addPFN(PFN(BASE_DIR + "/input.txt", "local"))
dax.addFile(_if)

# Add jobs
of = File("output.txt")
wc_job = Job(wc)
wc_job.addArguments(_if.name, of.name)
wc_job.uses(_if, link=Link.INPUT, transfer=False)
wc_job.uses(of, link=Link.OUTPUT, transfer=True)
dax.addJob(wc_job)

final_of = File("final_output.tar.gz")
tar_job = Job(tar)
tar_job.addArguments("cvzf", final_of, _if, of)
tar_job.uses(_if, link=Link.INPUT, transfer=False)
tar_job.uses(of, link=Link.INPUT, transfer=False)
tar_job.uses(final_of, link=Link.OUTPUT, transfer=True)
dax.addJob(tar_job)

# Add dependency 
dax.addDependency(Dependency(parent=wc_job, child=tar_job))


# Write the DAX to a file
with open("workflow.xml", "w") as f:
    dax.writeXML(f)

