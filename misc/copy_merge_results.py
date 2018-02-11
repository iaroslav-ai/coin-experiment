"""This script is used to copy the
collected data from a server and consolidate results"""
import csv
import os
import json

# has 2 columns, ssh command to connect and command run on server
exp_configs = '/home/iaroslav/experiments.csv'
tmp_file = os.path.join(os.getcwd(), 'tmp.json')
destination = 'cupronickel_results.json'

# this stores all results as array
all_results = []

for ssh, _ in csv.reader(open(exp_configs, 'r')):
    # make copy command from ssh command on AWS
    scp = ssh.replace('ssh', 'scp')
    scp += ":/home/ubuntu/coin-experiment/results.json"
    scp += " " + tmp_file
    os.system(scp)

    # read the downloaded file
    js = json.load(open(tmp_file, 'r'))

    # copy the results
    all_results += js

# Done reading from servers. Now store data in destination
json.dump(all_results, open(destination, 'w'), sort_keys=True, indent=1)

os.remove(tmp_file)

