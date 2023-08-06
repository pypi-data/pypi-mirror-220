# topology-deployer
Python tool to deploy topologies from the defined json config files.

## Table of Contents
1. [Prerequisites](#prereq)
2. [Network](#network_types)
    1. [Management Network](#mgmt_nw)
    2. [Custom NAT Network](#nat_nw)
    3. [Isolated Network](#iso_nw)
3. [Virtual Manchines](#vms)
4. [JSON Topology Config](#json_conf)
    1. [JSON Network Config](#json_nw)
    2. [JSON Virtual Machine Config](#json_vm)

## Prerequisites <a name = "prereq"></a>

### Required Packages
```
sudo apt-get install -y bridge-utils libvirt-clients libvirt-daemon qemu qemu-kvm libvirt-dev libvirt-daemon-system libguestfs-tools virt-manager libosinfo-bin iptables-persistent python3-dev python3-pip
```

### Add user to appropriate groups
```
sudo usermod -a -G libvirt $USER
sudo usermod -a -G libvirt-qemu $USER
```

## Networks <a name = "network_types"></a>
1. Management network
2. Custom NAT network
3. Isolated network

Libvirt implicitly installs a default NAT network. However libvirt's NAT network automatically inserts iptables rules whether you want them or not — in an order that is difficult to control — unless you disable the default network completely

Disbale libvirt's default network. We will create a Custom NAT Network.
```
virsh net-destroy default
virsh net-autostart --disable default
```

### Management Network <a name = "mgmt_nw"></a>
This is a libvirt managed host only network used for SSH connections. During creation of VM, one of the network should be connected to virtual bridge for the management network.

### Custom NAT Network <a name = "nat_nw"></a>
To overcome the challenges of libvirt's NAT network, we will create a Custom NAT network using four main components: a dummy network interface, a virtual bridge, some iptables rules, and dnsmasq.

### Isolated Network <a name = "iso_nw"></a>
Isolated Network are completely private to guest systems. All the guests on same isolated network will be able to communicate to each other

## Virtual Machines <a name = "vms"></a>
For our topology we will create virtual machines using libvirt. There are 2 pre-defined flavors for VMs, which will have configured memory, vcpus and disk size. This can be overriden from the json config if required.

#### PE Virtual Machine
1. Memory : 16G
2. vCPUs : 8
3. Disk : 80G

#### CE Virtual Machine
1. Memory : 8G
2. vCPUs : 4
3. Disk : 40G

## JSON Topology Config <a name = "json_conf"></a>
The json config to define topologies comprises of 2 sections.
1. Networks
2. Virtual Machines

### JSON Network Config <a name = "json_nw"></a>
The JSON network object comprises of array of required type of networks. A network object skeleton is shown below

```json
{
    "networks" : {
        "nat" : [],
        "isolated" : [],
        "management" : []
    }
}
```

#### Add NAT network in JSON network object
For nat network, `name` and `subnet4` are mandatory fields. `subnet6` is optional in case you need v6 network in your topology. To have multiple NAT networks, you can add multiple objects in the networks.nat json object.

```json
{
    "networks" : {
        "nat" : [{
            "name" : "",
            "subnet4" : "",
            "subnet6" : ""
        }]
    }
}
```

#### Add Management network in JSON network object
For management network, `name` and `subnet4` are mandatory fields. Currently we do not support v6 management network. To have multiple NAT networks, you can add multiple objects in the networks.management json object.

```json
{
    "networks" : {
        "management" : [{
            "name" : "",
            "subnet4" : ""
        }]
    }
}
```

#### Add Isolated network in JSON network object
For isolated network, `name` is mandatory fields. To have multiple NAT networks, you can add multiple objects in the networks.isolated json object.

```json
{
    "networks" : {
        "isolated" : [{
            "name" : ""
        }]
    }
}
```

### JSON Virtual Machine Config <a name = "json_vm"></a>
The vms object is array of multiple vm objects. For the vm object on the JSON config, `name`, `flavor`, `vnc_port` and `networks` are mandatory fields. You can optionally use `ram`, `vcpus` and `disk` to override the defaults for the flavor. A vms object skeleton is shown below

```json
{
    "vms" : [{
        "name" : "",
        "flavor" : "",
        "vnc_port" : "",
        "networks" : {
            "<nw_name1>" : {
                "v4" : ""
            },
            "<nw_name2>" : {
                "v4" : "",
                "v6" : ""
            }
        }
    }]
}
```

To define networks for the vm, you have to use the network name as key and provide `v4` address. You can also add a `v6` address if the network type is NAT.

## Sample Topology Configurations

### A two PE and two CE topology
```
|-------|      |---------|                |---------|      |-------|
|  CE1  |======|   PE1   |================|   PE2   |======|  CE2  |
|       |======|         |================|         |======|       |
|-------|      |---------|                |---------|      |-------|
```

Topology Config : [2PE-CE.json](topologies/2PE-CE.json)
