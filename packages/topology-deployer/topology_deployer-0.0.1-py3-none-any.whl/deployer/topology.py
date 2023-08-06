import json
import logging
import sys

import deployer.globals as globals
# from .config import NO_NETWORK, NO_VM, PRINT_NETWORK, PRINT_VM
from .network import Network
from .virtual_machine import VirtualMachine

class Topology:
    supported_network_types_ = ["nat", "isolated", "management"]
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Topology, cls).__new__(cls)
        return cls.instance

    def Init(self, config):
        with open(config) as conf_file:
            self.config = json.load(conf_file)

        if self.config is None:
            print("Error parsing config file")
            exit(1)

        self.networks = {}
        self.vms = {}

        if not globals.NO_NETWORK:
            self.CreateNetworks()

        if not globals.NO_VM:
            self.CreateVms()

        if globals.PRINT_NETWORK:
            self.PrintNetworks()

        if globals.PRINT_VM:
            self.PrintVms()

    def __is_nw_type_valid(self, nw_type: str) -> bool:
        return nw_type in self.supported_network_types_

    def __parse_networks(self):
        nw_config = self.config.get("networks", {})
        if nw_config:
            for nw_type in nw_config:
                if not self.__is_nw_type_valid(nw_type):
                    logging.critical("Unsupported network type {}")
                    sys.exit(1)
                for nw in nw_config[nw_type]:
                    self.networks[nw["name"]] = Network(nw_type, nw, self)
        else:
            logging.critical("No network config found. Exiting")
            sys.exit(1)

    def GetNetwork(self, name):
        return self.networks.get(name, None)

    def GetNetworkType(self, name):
        if self.GetNetwork(name) is not None:
            return self.networks[name].type_
        return ""

    def __parse_vms(self):
        vms_config = self.config.get("vms", [])
        if vms_config:
            for vm_conf in vms_config:
                if vm_conf is {}:
                    continue
                self.vms[vm_conf["name"]] = VirtualMachine(vm_conf, self)

    def PrintNetworks(self):
        for name, nw in self.networks.items():
            print("Network : {}".format(name))
            print(nw.ToString())

    def PrintVms(self):
        for name, vm in self.vms.items():
            print("Vm : {}".format(name))
            print(vm.ToString())

    def CreateNetworks(self):
        self.__parse_networks()
        for _, nw in self.networks.items():
            nw.Create()

    def CreateVms(self):
        self.__parse_vms()
        for _, vm in self.vms.items():
            vm.Create()
