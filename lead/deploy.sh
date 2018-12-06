#!/usr/bin/env bash

############A############### DESCRIPTION ###############################
# This script deploys a folder (recursively) to an IP address given as #
# argument, or, if none, to the DHCP leases.						   #
#																       #
# DEPENDENCIES: sshpass, scp										   #
########################################################################


############################ CONFIGURATION #############################
lease_file=/var/lib/misc/dnsmasq.leases
leases=() # IPs array
# Target machine
username="pi" 
password="raspberry"

restart_process=1 # Whether to restart the process on the target machine, after uploading the code
process_to_kill="nohup"
process_name="cd ~/slave/ && nohup python3 client_node.py" # Name of the process to restart (with arguments)
folder=~/slave/ # Absolute path to the code folder to upload to the target machine(s)


############################ FUNCTIONS #################################
function auto_deploy {
	parse_leases
	for i in "${leases[@]}"
	do
		deploy_to $i
	done
}

# Parses the DHCP leases in $lease_file and popluate the
# leases array used for deployment.
function parse_leases {
	echo "[*] Parsing DHCP leases..."
	regex=164\.24\.1\.[0-9]{1,3}
	while read -r line; do
		if [[ $line =~ $regex ]]; then
			leases+=("${BASH_REMATCH[0]}")
		fi
	done < $lease_file

	echo "[*] Found ${#leases[@]} nodes"
}

# Deploys the code folder to the target machine (first argument) using SCP (cp
# over ssh) and sshpass for painless password passing.
function deploy_to {
	echo "[*] Deploying $folder to $1 ..."
	set -e;
	sshpass -p "$password" scp -r "$folder" "$username"@"$1":~/ &>/dev/null || EXIT_CODE=$? && true;
	if [[ EXIT_CODE -eq 1 ]]; then
		echo "[!] Node down."
	else
		echo "[*] Ok!"
		if [[ $restart_process -eq 1 ]]; then
			echo "[*] Restarting target process ..."
			sshpass -p "$password" ssh "$username"@"$1" "pkill $process_to_kill -9" &>/dev/null || RETURN_CODE=$? && true;
			sshpass -p "$password" ssh "$username"@"$1" "$process_name" &>/dev/null || RETURN_CODE=$? && true;
		fi
	fi
	unset EXIT_CODE
	unset RETURN_CODE
}


############################ MAIN #################################
if [[ $# -lt 1 ]]; then
	echo "[*] No argument received: Auto mode."
	auto_deploy
else
	deploy_to $1
fi

echo "Done!"


