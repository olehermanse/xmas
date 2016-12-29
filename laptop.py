from jenkins_status.Jenkins import Jenkins
from subprocess import call
from time import sleep

jenkins = Jenkins("ci.cfengine.com", verbose = True, directory = "./data")
with open("./data/ready", "w") as f:
    f.write("ready")

while True:
    jenkins.update()
    call(["scp", "./data/jenkins_jobs.json", "olehermanse@10.25.0.195:new_jobs.json"])
    call(["scp", "./data/ready", "olehermanse@10.25.0.195:ready"])
    sleep(8)
