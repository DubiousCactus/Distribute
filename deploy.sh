#!/usr/bin/env bash

leases=() # IPs array
username="pi"
password="raspberry"
folder=node/

function auto_deploy {
	parse_leases
	for i in "${leases[@]}"
	do
		deploy_to $i
	done
}

function parse_leases {
	echo "[*] Parsing DHCP leases..."
	regex=164\.24\.1\.[0-9]{1,3}
	while read -r line; do
		if [[ $line =~ $regex ]]; then
			leases+=("${BASH_REMATCH[0]}")
		fi
	done < /var/lib/misc/dnsmasq.leases

	echo "[*] Found ${#leases[@]} nodes"
}

function deploy_to {
	echo "[*] Deploying code to $1 ..."
	set -e;
	sshpass -p "$password" scp -r $folder "$username"@"$1":~/ &>/dev/null || EXIT_CODE=$? && true;
	echo "[*] Restarting target process ..."
	sshpass -p "$password" ssh -c "pkill python3" "$username"@"$1"
	if [[ EXIT_CODE -eq 1 ]]; then
		echo "[!] Node down."
	else
		echo "[*] Ok!"
	fi
}

if [[ $# -lt 1 ]]; then
	echo "[*] No argument received: Auto mode."
	auto_deploy
else
	deploy_to $1
fi

echo "Done!"


