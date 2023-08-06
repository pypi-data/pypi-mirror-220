#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Author: Zhaojuan Guo <zguo@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2023 Red Hat, Inc.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from abc import ABCMeta, abstractmethod
import os


class BaseSriov(metaclass=ABCMeta):
    """ Abstract class
    """
    def __init__(self, hca_id):
        self.hca_id = hca_id
        self.pci_device = self.get_pci_from_hca_id()

    def get_pci_from_hca_id(self):
        # get the pci device associated with a given Infiniband device
        pcidevlist = os.listdir("/sys/bus/pci/devices")

        for pcidev in pcidevlist:
            if os.path.isdir(f"/sys/bus/pci/devices/{pcidev}/infiniband"):
                if os.listdir(f"/sys/bus/pci/devices/{pcidev}/infiniband/") == [self.hca_id]:
                    return pcidev

    @staticmethod
    @abstractmethod
    def get_pf_name_from_pf_bus(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def get_pf_bus_from_pf_name(pf_name):
        pass

    @staticmethod
    @abstractmethod
    def get_all_vfs_from_pf_bus(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def create_vfs(pf_bus, num):
        pass

    @staticmethod
    @abstractmethod
    def delete_vfs(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def get_pf_name_from_vf_name(vf_name):
        pass

    # @staticmethod
    # @abstractmethod
    # def get_pf_bus_from_vf_name(vf_name):
    #     pass
