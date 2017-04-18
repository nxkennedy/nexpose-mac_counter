
# Nexpose Automated MAC Address Counter

Often Nexpose discovery scans of VIPs, VMs, and hypervisors return results of
duplicate MAC addresses or no MAC at all. This tool sheds light on asset detection accuracy by determining unique MACs found, assets missing MACs, dupes, and the
10 most common dupes.

<table>
    <tr>
        <th>Version</th>
        <td>1.0.0</td>
    </tr>
    <tr>
       <th>Author</th>
       <td>Nolan Kennedy
    </tr>
    <tr>
        <th>Github</th>
        <td><a href="http://github.com/nxkennedy/nexpose-mac_counter">http://github.com/nxkennedy/nexpose-mac_counter</a></td>
    </tr>
</table>

## Use Case

Count MAC addresses discovered in a scan to determine asset detection accuracy

## Requirements
1. python 3.x
2. Nexpose SQL export report generated with the following query:
```sql

SELECT mac_address AS "MAC", da.ip_address AS "IP", host_name AS "Host Name",
dos.description AS "OS", dht.description AS "Host Type"
FROM fact_asset_discovery
  JOIN dim_asset da USING (asset_id)
  JOIN dim_operating_system dos USING (operating_system_id)
  JOIN dim_host_type dht USING (host_type_id)

```

## Setup
1. Clone the repo

    `git clone https://github.com/nxkennedy/nexpose-mac_counter.git`

2. Install requirements

    `pip3 install collections`

3. This script scans it's current dir for any csv reports. Place the reports you
want scanned in the same directory

## Usage

     python3 nexpose-mac_counter.py

## Output
Progress is printed to the terminal in the following format:

```

>> Stats for:  DiscoveryReport.csv
_____
> Active Assets Found in Scan:  1510
> Duplicate MACs:  124
> Hosts/IPs Without MACs:  1002
=====
> Total Unique MACs:  384
=====

> Top 10 Occuring Dupes:
84:80:69:fd:22:69 x 5
00:25:82:06:e0:70 x 4
4e:56:83:16:24:71 x 3
9a:81:19:84:76:72 x 3
8e:98:a5:24:26:73 x 3
00:25:86:06:74:cf x 3
7e:6a:85:9e:75:76 x 3
00:25:77:06:e1:ef x 3
46:87:d4:78:e3:60 x 3
82:88:91:79:6a:39 x 3

> Sample of Hosts Missing MACs:
['10.1.1.2', '']
['10.1.1.3', '']
['10.1.1.4', 'random-host1.com']
['10.1.1.5', 'random-host2.com]
['10.1.1.6', 'random-host3.com']
['10.1.1.7', '']
['10.1.1.8', 'random-host4.com']
['10.1.1.9', 'random-host5.com']
['10.1.1.10', '']
['10.1.1.11', 'random-host6.com']

```
