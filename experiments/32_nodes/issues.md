## Issue 1:

Sometimes flannel fails to start with CrashLoopBackOff error message (kubectl logs and describe do not work on the failed container)
Restarting the make up/kubeadm-join couple of times makes it work after a while

=> Consequence is that kubeadm-join will hang because the network does not exist
=> Important to check with 'kubectl get pods -A' that both flannel and coredns containers are started properly before adding any workers

TODO : identify why flannel is failing

## Issue 2 : 

Whe launching a cluster with Flux Operator

DNS message leaves host1, makes it to host0,DNS gets requests and answers, message disappears between flannel.1 and eth0 on host0 so we don’t receive an answer
So flux workers don’t join the master

On host 0 : incoming com, without any answer

10:36:35.586423 IP flux-user000001.internal.cloudapp.net.40651 > flux-user000000.internal.cloudapp.net.8472: OTV, flags [I] (0x08), overlay 0, instance 1
IP 10.244.13.2.42747 > 10.244.0.2.domain: 37725+ A? flux-sample-0.flux-service.default.svc.cluster.local.default.svc.cluster.local. (96)


DNS receiving and answering : 

10:34:40.776272 flannel.1 In  IP 10.244.13.2.55999 > 10.244.0.2.domain: 57194+ A? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776302 cni0  Out IP 10.244.13.2.55999 > 10.244.0.2.domain: 57194+ A? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776304 veth78b87eb8 Out IP 10.244.13.2.55999 > 10.244.0.2.domain: 57194+ A? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776326 flannel.1 In  IP 10.244.13.2.55999 > 10.244.0.2.domain: 19821+ AAAA? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776336 cni0  Out IP 10.244.13.2.55999 > 10.244.0.2.domain: 19821+ AAAA? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776338 veth78b87eb8 Out IP 10.244.13.2.55999 > 10.244.0.2.domain: 19821+ AAAA? flux-sample-0.flux-service.default.svc.cluster.local. (70)
10:34:40.776536 veth78b87eb8 P   IP 10.244.0.2.domain > 10.244.13.2.55999: 19821*- 0/1/0 (163)
10:34:40.776536 cni0  In  IP 10.244.0.2.domain > 10.244.13.2.55999: 19821*- 0/1/0 (163)
10:34:40.776558 flannel.1 Out IP 10.244.0.2.domain > 10.244.13.2.55999: 19821*- 0/1/0 (163)
10:34:40.776704 veth78b87eb8 P   IP 10.244.0.2.domain > 10.244.13.2.55999: 57194*- 1/0/0 A 10.244.19.2 (138)
10:34:40.776704 cni0  In  IP 10.244.0.2.domain > 10.244.13.2.55999: 57194*- 1/0/0 A 10.244.19.2 (138)
10:34:40.776762 flannel.1 Out IP 10.244.0.2.domain > 10.244.13.2.55999: 57194*- 1/0/0 A 10.244.19.2 (138)


### flannel.1 configuration on working setup

```
cat /var/log/containers/kube-flannel-ds-9dpjb_kube-flannel_kube-flannel-31ac9cf012d5d9deeeb00d1a52598be6244aadab4bb31b3cd0b3dc24f192df84.log
...
2025-03-19T13:10:34.486656453Z stderr F I0319 13:10:34.486578       1 match.go:211] Determining IP address of default interface
2025-03-19T13:10:34.48728136Z stderr F I0319 13:10:34.487188       1 match.go:264] Using interface with name eth0 and address 10.100.151.100
2025-03-19T13:10:34.487354281Z stderr F I0319 13:10:34.487208       1 match.go:286] Defaulting external address to interface address (10.100.151.100)
2025-03-19T13:10:34.487361495Z stderr F I0319 13:10:34.487271       1 vxlan.go:141] VXLAN config: VNI=1 Port=8472 GBP=false Learning=false DirectRouting=false
...
```


```
azureuser@flux-user000000:/opt$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:22:48:a7:27:e0 brd ff:ff:ff:ff:ff:ff
    inet 172.16.0.4/24 metric 100 brd 172.16.0.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::222:48ff:fea7:27e0/64 scope link 
       valid_lft forever preferred_lft forever
3: enP27815s1: <BROADCAST,MULTICAST,SLAVE,UP,LOWER_UP> mtu 1500 qdisc mq master eth0 state UP group default qlen 1000
    link/ether 00:22:48:a7:27:e0 brd ff:ff:ff:ff:ff:ff
    altname enP27815p0s2
    inet6 fe80::222:48ff:fea7:27e0/64 scope link 
       valid_lft forever preferred_lft forever
4: ibP257s71127: <BROADCAST,MULTICAST> mtu 4092 qdisc noop state DOWN group default qlen 1000
    link/infiniband 00:00:01:28:fe:80:00:00:00:00:00:00:00:15:5d:ff:fd:33:ff:95 brd 00:ff:ff:ff:ff:12:40:1b:80:04:00:00:00:00:00:00:ff:ff:ff:ff
    altname ibP257p0s0
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:53:a8:fa:f2 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
```

```
azureuser@flux-user000000:/opt$ sudo nsenter --net=/proc/6910/ns/net
root@flux-user000000:/opt# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default 
    link/ether 16:95:0d:6d:7e:e0 brd ff:ff:ff:ff:ff:ff
    inet 10.244.0.0/32 scope global flannel.1
       valid_lft forever preferred_lft forever
    inet6 fe80::1495:dff:fe6d:7ee0/64 scope link 
       valid_lft forever preferred_lft forever
3: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000
    link/ether ba:03:ed:79:64:b0 brd ff:ff:ff:ff:ff:ff
    inet 10.244.0.1/24 brd 10.244.0.255 scope global cni0
       valid_lft forever preferred_lft forever
    inet6 fe80::b803:edff:fe79:64b0/64 scope link 
       valid_lft forever preferred_lft forever
4: veth482f2c81@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP group default qlen 1000
    link/ether 16:5d:63:a2:21:04 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::145d:63ff:fea2:2104/64 scope link 
       valid_lft forever preferred_lft forever
5: vethaaa0d8eb@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master cni0 state UP group default qlen 1000
    link/ether a2:9c:b0:0b:12:ad brd ff:ff:ff:ff:ff:ff link-netnsid 2
    inet6 fe80::a09c:b0ff:fe0b:12ad/64 scope link 
       valid_lft forever preferred_lft forever
9: eth0@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:0a:64:97:64 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.100.151.100/24 brd 10.100.151.255 scope global eth0
       valid_lft forever preferred_lft forever
```

```
azureuser@flux-user000000:/opt$ ip route
default via 172.16.0.1 dev eth0 proto dhcp src 172.16.0.4 metric 100 
168.63.129.16 via 172.16.0.1 dev eth0 proto dhcp src 172.16.0.4 metric 100 
169.254.169.254 via 172.16.0.1 dev eth0 proto dhcp src 172.16.0.4 metric 100 
172.16.0.0/24 dev eth0 proto kernel scope link src 172.16.0.4 metric 100 
172.16.0.1 dev eth0 proto dhcp scope link src 172.16.0.4 metric 100 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
```

```
azureuser@flux-user000000:/opt$ sudo iptables -vL
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DOCKER-USER  all  --  any    any     anywhere             anywhere            
    0     0 DOCKER-ISOLATION-STAGE-1  all  --  any    any     anywhere             anywhere            
    0     0 ACCEPT     all  --  any    docker0  anywhere             anywhere             ctstate RELATED,ESTABLISHED
    0     0 DOCKER     all  --  any    docker0  anywhere             anywhere            
    0     0 ACCEPT     all  --  docker0 !docker0  anywhere             anywhere            
    0     0 ACCEPT     all  --  docker0 docker0  anywhere             anywhere            

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain DOCKER (1 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain DOCKER-ISOLATION-STAGE-1 (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DOCKER-ISOLATION-STAGE-2  all  --  docker0 !docker0  anywhere             anywhere            
    0     0 RETURN     all  --  any    any     anywhere             anywhere            

Chain DOCKER-ISOLATION-STAGE-2 (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  any    docker0  anywhere             anywhere            
    0     0 RETURN     all  --  any    any     anywhere             anywhere            

Chain DOCKER-USER (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 RETURN     all  --  any    any     anywhere             anywhere  
```

```
ip -json -pretty link show flannel.1
[ {
        "ifindex": 2,
        "ifname": "flannel.1",
        "flags": [ "BROADCAST","MULTICAST","UP","LOWER_UP" ],
        "mtu": 1450,
        "qdisc": "noqueue",
        "operstate": "UNKNOWN",
        "linkmode": "DEFAULT",
        "group": "default",
        "link_type": "ether",
        "address": "16:95:0d:6d:7e:e0",
        "broadcast": "ff:ff:ff:ff:ff:ff"
    } ]

bridge link show flannel.1
4: veth482f2c81@flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 master cni0 state forwarding priority 32 cost 2 
5: vethaaa0d8eb@flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 master cni0 state forwarding priority 32 cost 2

bridge vlan show flannel.1
port              vlan-id  
cni0              1 PVID Egress Untagged
veth482f2c81      1 PVID Egress Untagged
vethaaa0d8eb      1 PVID Egress Untagged
```

```
ip -json -pretty link show cni0
[ {
        "ifindex": 3,
        "ifname": "cni0",
        "flags": [ "BROADCAST","MULTICAST","UP","LOWER_UP" ],
        "mtu": 1450,
        "qdisc": "noqueue",
        "operstate": "UP",
        "linkmode": "DEFAULT",
        "group": "default",
        "txqlen": 1000,
        "link_type": "ether",
        "address": "ba:03:ed:79:64:b0",
        "broadcast": "ff:ff:ff:ff:ff:ff"
    } ]
```

```
root@flux-user000000:/opt# ethtool -k flannel.1
Features for flannel.1:
rx-checksumming: on
tx-checksumming: off
	tx-checksum-ipv4: off [fixed]
	tx-checksum-ip-generic: off
	tx-checksum-ipv6: off [fixed]
	tx-checksum-fcoe-crc: off [fixed]
	tx-checksum-sctp: off [fixed]
scatter-gather: on
	tx-scatter-gather: on
	tx-scatter-gather-fraglist: on
tcp-segmentation-offload: off
	tx-tcp-segmentation: off [requested on]
	tx-tcp-ecn-segmentation: off [requested on]
	tx-tcp-mangleid-segmentation: off [requested on]
	tx-tcp6-segmentation: off [requested on]
generic-segmentation-offload: on
generic-receive-offload: on
large-receive-offload: off [fixed]
rx-vlan-offload: off [fixed]
tx-vlan-offload: off [fixed]
ntuple-filters: off [fixed]
receive-hashing: off [fixed]
highdma: off [fixed]
rx-vlan-filter: off [fixed]
vlan-challenged: off [fixed]
tx-lockless: on [fixed]
netns-local: off [fixed]
tx-gso-robust: off [fixed]
tx-fcoe-segmentation: off [fixed]
tx-gre-segmentation: off [fixed]
tx-gre-csum-segmentation: off [fixed]
tx-ipxip4-segmentation: off [fixed]
tx-ipxip6-segmentation: off [fixed]
tx-udp_tnl-segmentation: off [fixed]
tx-udp_tnl-csum-segmentation: off [fixed]
tx-gso-partial: off [fixed]
tx-tunnel-remcsum-segmentation: off [fixed]
tx-sctp-segmentation: on
tx-esp-segmentation: off [fixed]
tx-udp-segmentation: on
tx-gso-list: on
fcoe-mtu: off [fixed]
tx-nocache-copy: off
loopback: off [fixed]
rx-fcs: off [fixed]
rx-all: off [fixed]
tx-vlan-stag-hw-insert: off [fixed]
rx-vlan-stag-hw-parse: off [fixed]
rx-vlan-stag-filter: off [fixed]
l2-fwd-offload: off [fixed]
hw-tc-offload: off [fixed]
esp-hw-offload: off [fixed]
esp-tx-csum-hw-offload: off [fixed]
rx-udp_tunnel-port-offload: off [fixed]
tls-hw-tx-offload: off [fixed]
tls-hw-rx-offload: off [fixed]
rx-gro-hw: off [fixed]
tls-hw-record: off [fixed]
rx-gro-list: off
macsec-hw-offload: off [fixed]
rx-udp-gro-forwarding: off
hsr-tag-ins-offload: off [fixed]
hsr-tag-rm-offload: off [fixed]
hsr-fwd-offload: off [fixed]
hsr-dup-offload: off [fixed]
```

```
root@flux-user000000:/opt# ip route
default via 10.100.151.1 dev eth0 
10.100.151.0/24 dev eth0 proto kernel scope link src 10.100.151.100 
10.244.0.0/24 dev cni0 proto kernel scope link src 10.244.0.1 
10.244.1.0/24 via 10.244.1.0 dev flannel.1 onlink 
10.244.2.0/24 via 10.244.2.0 dev flannel.1 onlink 
10.244.3.0/24 via 10.244.3.0 dev flannel.1 onlink 
10.244.4.0/24 via 10.244.4.0 dev flannel.1 onlink 
10.244.5.0/24 via 10.244.5.0 dev flannel.1 onlink 
10.244.7.0/24 via 10.244.7.0 dev flannel.1 onlink 
10.244.8.0/24 via 10.244.8.0 dev flannel.1 onlink 
10.244.9.0/24 via 10.244.9.0 dev flannel.1 onlink 
10.244.10.0/24 via 10.244.10.0 dev flannel.1 onlink 
10.244.11.0/24 via 10.244.11.0 dev flannel.1 onlink 
10.244.12.0/24 via 10.244.12.0 dev flannel.1 onlink 
10.244.13.0/24 via 10.244.13.0 dev flannel.1 onlink 
10.244.14.0/24 via 10.244.14.0 dev flannel.1 onlink 
10.244.15.0/24 via 10.244.15.0 dev flannel.1 onlink 
10.244.16.0/24 via 10.244.16.0 dev flannel.1 onlink 
10.244.17.0/24 via 10.244.17.0 dev flannel.1 onlink 
10.244.18.0/24 via 10.244.18.0 dev flannel.1 onlink 
10.244.19.0/24 via 10.244.19.0 dev flannel.1 onlink 
10.244.20.0/24 via 10.244.20.0 dev flannel.1 onlink 
10.244.21.0/24 via 10.244.21.0 dev flannel.1 onlink 
10.244.22.0/24 via 10.244.22.0 dev flannel.1 onlink 
10.244.23.0/24 via 10.244.23.0 dev flannel.1 onlink 
10.244.24.0/24 via 10.244.24.0 dev flannel.1 onlink 
10.244.25.0/24 via 10.244.25.0 dev flannel.1 onlink 
10.244.26.0/24 via 10.244.26.0 dev flannel.1 onlink 
10.244.27.0/24 via 10.244.27.0 dev flannel.1 onlink 
10.244.28.0/24 via 10.244.28.0 dev flannel.1 onlink 
10.244.29.0/24 via 10.244.29.0 dev flannel.1 onlink 
10.244.30.0/24 via 10.244.30.0 dev flannel.1 onlink 
10.244.31.0/24 via 10.244.31.0 dev flannel.1 onlink 
10.244.32.0/24 via 10.244.32.0 dev flannel.1 onlink
```

```
root@flux-user000000:/opt# iptables -vL
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
 116K   75M KUBE-PROXY-FIREWALL  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes load balancer firewall */
3262K 3814M KUBE-NODEPORTS  all  --  any    any     anywhere             anywhere             /* kubernetes health check service ports */
 116K   75M KUBE-EXTERNAL-SERVICES  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes externally-visible service portals */
3275K 3818M KUBE-FIREWALL  all  --  any    any     anywhere             anywhere            

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
15157 1581K KUBE-PROXY-FIREWALL  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes load balancer firewall */
 141K   96M KUBE-FORWARD  all  --  any    any     anywhere             anywhere             /* kubernetes forwarding rules */
15157 1581K KUBE-SERVICES  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes service portals */
15157 1581K KUBE-EXTERNAL-SERVICES  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes externally-visible service portals */
15157 1581K FLANNEL-FWD  all  --  any    any     anywhere             anywhere             /* flanneld forward */

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
 102K   16M KUBE-PROXY-FIREWALL  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes load balancer firewall */
 102K   16M KUBE-SERVICES  all  --  any    any     anywhere             anywhere             ctstate NEW /* kubernetes service portals */
3236K 1259M KUBE-FIREWALL  all  --  any    any     anywhere             anywhere            

Chain FLANNEL-FWD (1 references)
 pkts bytes target     prot opt in     out     source               destination         
15157 1581K ACCEPT     all  --  any    any     10.244.0.0/16        anywhere             /* flanneld forward */
    0     0 ACCEPT     all  --  any    any     anywhere             10.244.0.0/16        /* flanneld forward */

Chain KUBE-EXTERNAL-SERVICES (2 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain KUBE-FIREWALL (2 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  any    any    !127.0.0.0/8          127.0.0.0/8          /* block incoming localnet connections */ ! ctstate RELATED,ESTABLISHED,DNAT

Chain KUBE-FORWARD (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  any    any     anywhere             anywhere             ctstate INVALID nfacct-name  ct_state_invalid_dropped_pkts
    0     0 ACCEPT     all  --  any    any     anywhere             anywhere             /* kubernetes forwarding rules */ mark match 0x4000/0x4000
  214 19911 ACCEPT     all  --  any    any     anywhere             anywhere             /* kubernetes forwarding conntrack rule */ ctstate RELATED,ESTABLISHED

Chain KUBE-KUBELET-CANARY (0 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain KUBE-NODEPORTS (1 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain KUBE-PROXY-CANARY (0 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain KUBE-PROXY-FIREWALL (3 references)
 pkts bytes target     prot opt in     out     source               destination         

Chain KUBE-SERVICES (2 references)
 pkts bytes target     prot opt in     out     source               destination
 ```
