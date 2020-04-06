#!/usr/bin/env python

import os
from Pegasus.DAX3 import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create a abstract dag
dax = ADAG("workflow_that_will_fail", auto=False)

# Add executable(s)
wc = Executable(name="wc")
wc.addPFN(PFN(BASE_DIR + "/wc.sh", "local"))
wc.addProfile(Profile(Namespace.ENV, "http_proxy", "http://workflow.isi.edu:8000")
dax.addExecutable(wc)

# Add input file
_if = File("input.txt")
_if.addPFN(PFN(BASE_DIR + "/input.txt", "local"))

# Add jobs
of = File("output.txt")
wc_job1 = Job(wc)
wc_job1.addArguments(_if.name, of.name)
wc_job1.uses(_if, link=Link.INPUT, transfer=False)
wc_job1.uses(of, link=Link.OUTPUT, transfer=False)
dax.addJob(wc_job1)

wc_job2 = Job(wc)
wc_job2.addArguments(_if.name, of.name)
wc_job2.uses(_if, link=Link.INPUT, transfer=False)
wc_job2.uses(of, link=Link.OUTPUT, transfer=True)
dax.addJob(wc_job2)

# Add dependency 
# we want wc_job2 to run after wc_job1 so that we see cache miss, then hit
dax.addDependency(Dependency(parent=wc_job1, child=wc_job2))

# Write the DAX to a file
with open("workflow.xml", "w") as f:
    dax.writeXML(f)

