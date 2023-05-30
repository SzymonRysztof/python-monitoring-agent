#!/usr/bin/env bash

# Unofficial bash strict mode thanks to http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

printf "--------------------\nLooking for docker group ID \n"
G_ID=$(ls -n /var/run/docker.sock | awk '{ print $4 }')
printf "--------------------\nDocker GID appears to be $G_ID \n"

if ! grep $G_ID /etc/group > /dev/null; then
  printf "--------------------\nAdding $user to $G_ID\n"
  addgroup docker --gid $G_ID && addgroup $user docker
else
  printf "--------------------\n$G_ID exists in the system already \n"
fi

printf "--------------------\nSwitching user to $user \n"
su $user -c "/app/.local/bin/pma"
