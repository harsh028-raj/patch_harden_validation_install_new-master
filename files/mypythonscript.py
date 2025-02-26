import subprocess
import os
import csv
 
 
#host_param = os.environ.get("HOSTS")
#hosts = host_param.split(",") if host_param else []
 
jenkins_workspace = os.environ.get("WORKSPACE")
output_csv_path = os.path.join(jenkins_workspace, "new_output.csv")
 
# Create a CSV file
with open(output_csv_path, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Host", "Patch Version", "Patch Date", "Harden Version", "Harden Date", "Uptime", "Repo Version"])
 
    for host in hosts:
        if not host:
           print("Invalid host: {}".format(host))
           continue
        # Execute the first Linux command
        try:
            result = subprocess.check_output(["ssh", host, "cat /etc/ppstie_host_metadata.yml"], universal_newlines=True, stderr=subprocess.STDOUT)
            data = result.splitlines()
        except subprocess.CalledProcessError as e:
            print("Error running command on {}: {}".format(host, e.output))
            data = []
 
        new_patch_version = next((line.split(":")[1].strip() for line in data if "patch_version" in line), "Not Found")
        new_patch_date = next((line.split(":")[1].strip() for line in data if "patch_date" in line), "Not Found")
        new_harden_version = next((line.split(":")[1].strip() for line in data if "tie_builder_playbooks_harden_version" in line), "Not Found")
        new_harden_date = next((line.split(":")[1].strip() for line in data if "harden_date" in line), "Not Found")
 
        # Execute the fifth Linux command
        try:
            uptime = subprocess.check_output(["ssh", host, "uptime"], universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            uptime = "Not Found"
 
        # Execute the sixth Linux command
        try:
            repo_version = subprocess.check_output(["ssh", host, "uname", "-r"], universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            repo_version = "Not Found"
 
        # Append the data to the CSV file
        csvwriter.writerow([host, new_patch_version, new_patch_date, new_harden_version, new_harden_date, uptime, repo_version])
has context menu
