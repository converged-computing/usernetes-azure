#!/bin/bash

template_name="flux-user"
template_username="azureuser"
# Assume a huge number. This will error with Azure because they 
# eventually dive into alpha numeric, but this works for a small demo
NODELIST=${template_name}000[000-999]

# The lead broker can be anything, azure is not predictable
lead_broker=${template_name}000000

flux R encode --hosts=$NODELIST --local > R
sudo mv R /etc/flux/system/R
sudo chown ${template_username} /etc/flux/system/R

# Figure out the lead broker, the first in the list
echo "The lead broker is $lead_broker"
host=$(hostname)
echo "The host is $host"

# Make the run directories in case not made yet
sudo mkdir -p /home/${template_username}/run/flux /run/flux /opt/run/flux
mkdir -p /home/${template_username}/run/flux
sudo chown -R ${template_username} /home/${template_username}/run/flux /run/flux /opt/run/flux

# Write updated broker.toml
cat <<EOF | tee /tmp/broker.toml
# Flux needs to know the path to the IMP executable
[exec]
imp = "/usr/libexec/flux/flux-imp"

# Allow users other than the instance owner (guests) to connect to Flux
# Optionally, root may be given "owner privileges" for convenience
[access]
allow-guest-user = true
allow-root-owner = true

# Point to resource definition generated with flux-R(1).
# Uncomment to exclude nodes (e.g. mgmt, login), from eligibility to run jobs.
[resource]
path = "/etc/flux/system/R"

# Point to shared network certificate generated flux-keygen(1).
# Define the network endpoints for Flux's tree based overlay network
# and inform Flux of the hostnames that will start flux-broker(1).
[bootstrap]
curve_cert = "/etc/flux/system/curve.cert"

default_port = 8050
default_bind = "tcp://eth0:%p"
default_connect = "tcp://%h:%p"

# Rank 0 is the TBON parent of all brokers unless explicitly set with
# parent directives.
# The actual ip addresses (for both) need to be added to /etc/hosts
# of each VM for now.
hosts = [
   { host = "$NODELIST" },
]
# Speed up detection of crashed network peers (system default is around 20m)
[tbon]
tcp_user_timeout = "2m"
EOF

sudo mkdir -p /etc/flux/system/conf.d
sudo mv /tmp/broker.toml /etc/flux/system/conf.d/broker.toml

# Write new service file
cat <<EOF | tee /tmp/flux.service
[Unit]
Description=Flux message broker
Wants=munge.service

[Service]
Type=notify
NotifyAccess=main
TimeoutStopSec=90
KillMode=mixed
ExecStart=/bin/bash -c '\
  XDG_RUNTIME_DIR=/run/user/$UID \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$UID/bus \
  /usr/bin/flux broker \
  --config-path=/etc/flux/system/conf.d \
  -Scron.directory=/etc/flux/system/cron.d \
  -Srundir=/opt/run/flux \
  -Sstatedir=/var/lib/flux \
  -Slocal-uri=local:///opt/run/flux/local \
  -Slog-stderr-level=6 \
  -Slog-stderr-mode=local \
  -Sbroker.rc2_none \
  -Sbroker.quorum=1 \
  -Sbroker.quorum-timeout=none \
  -Sbroker.exit-norestart=42 \
  -Sbroker.sd-notify=1 \
  -Scontent.restore=auto'
SyslogIdentifier=flux
ExecReload=/usr/bin/flux config reload
Restart=always
RestartSec=5s
RestartPreventExitStatus=42
SuccessExitStatus=42
User=${template_username}
RuntimeDirectory=flux
RuntimeDirectoryMode=0755
StateDirectory=flux
StateDirectoryMode=0700
PermissionsStartOnly=true
DefaultLimitMEMLOCK=infinity
LimitMEMLOCK=infinity
DefaultLimitMEMLOCK=infinity
TasksMax=infinity
LimitNPROC=infinity
# ExecStartPre=/usr/bin/loginctl enable-linger flux
# ExecStartPre=bash -c 'systemctl start user@$(id -u flux).service'

#
# Delegate cgroup control to user flux, so that systemd doesn't reset
#  cgroups for flux initiated processes, and to allow (some) cgroup
#  manipulation as user flux.
#
Delegate=yes

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/flux.service /lib/systemd/system/flux.service

# See the README.md for commands how to set this manually without systemd
sudo systemctl daemon-reload
sudo systemctl restart flux.service
sudo systemctl status flux.service

# Just sanity check we own everything still
sudo chown -R ${template_username} /home/${template_username}

# sanity check everything is loaded
# This I think only persists until VM restart
echo "START modprobe"
sudo modprobe vxlan
sudo modprobe ip_tables
sudo modprobe ip6_tables
sudo modprobe ip6table_nat
sudo modprobe iptable_nat
sudo systemctl daemon-reload
sudo sysctl -p
sudo systemctl daemon-reload
sudo sysctl --system || true
