# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower ClientManager."""


import random
import threading
from abc import ABC, abstractmethod
from logging import INFO
from typing import Dict, List, Optional

from daisyfl.common.logger import log
from daisyfl.common import CREDENTIAL, NO_CREDENTIAL, ZONE_CREDENTIAL

from .client_proxy import ClientProxy


class ClientManager(ABC):
    """Abstract base class for managing Flower clients."""

    @abstractmethod
    def num_available(self) -> int:
        """Return the number of available clients."""

    @abstractmethod
    def register(self, client: ClientProxy) -> bool:
        """Register Flower ClientProxy instance.

        Returns:
            bool: Indicating if registration was successful
        """

    @abstractmethod
    def unregister(self, client: ClientProxy) -> None:
        """Unregister Flower ClientProxy instance."""

    @abstractmethod
    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients."""

    @abstractmethod
    def wait_for(self, num_clients: int, timeout: int) -> bool:
        """Wait until at least `num_clients` are available."""

    @abstractmethod
    def get_available_clients(
        self,
        min_num_clients: int = 2,
        credential: str = NO_CREDENTIAL,
        strict: bool = True,
    ) -> List[ClientProxy]:
        """get all available Daisy ClientProxy instances."""


class SimpleClientManager(ClientManager):
    """Provides a pool of available clients."""

    def __init__(self) -> None:
        self.clients: Dict[str, Dict[str, ClientProxy]] = {
            NO_CREDENTIAL: {},
            ZONE_CREDENTIAL: {},
        }
        self._cv = threading.Condition()

    def __len__(self,) -> int:
        return len(self.clients)

    def wait_for(self, num_clients: int, credential: str = NO_CREDENTIAL, strict: bool = True, timeout: int = 86400) -> bool:
        """Block until at least `num_clients` are available or until a timeout
        is reached.

        Current timeout default: 1 day.
        """
        if credential not in self.clients:
            self.clients[credential] = {}

        with self._cv:
            return self._cv.wait_for(
                lambda: self.num_available(credential, strict) >= num_clients, timeout=timeout
            )

    def num_available(self, credential, strict=True,) -> int:
        """Return the number of available clients."""
        if credential not in self.clients:
            self.clients[credential] = {}

        nums = len(self.clients[credential])
        if credential != ZONE_CREDENTIAL:
            nums = nums + len(self.clients[ZONE_CREDENTIAL])
        if (not strict) and (credential != NO_CREDENTIAL):
            nums = nums + len(self.clients[NO_CREDENTIAL])

        return nums

    def register(self, client: ClientProxy) -> bool:
        """Register Flower ClientProxy instance.

        Returns:
            bool: Indicating if registration was successful. False if ClientProxy is
                already registered or can not be registered for any reason
        """
        if client.cid in self.clients:
            return False
        if hasattr(client, "metadata_dict"):
            metadata_dict = getattr(client, "metadata_dict")
            if ZONE_CREDENTIAL in metadata_dict:
                self.clients[ZONE_CREDENTIAL][client.cid] = client
            elif CREDENTIAL in metadata_dict:
                credential = metadata_dict[CREDENTIAL]
                if credential not in self.clients:
                    self.clients[credential] = {}
                self.clients[credential][client.cid] = client
            else:
                self.clients[NO_CREDENTIAL][client.cid] = client
        else:
            self.clients[NO_CREDENTIAL][client.cid] = client
        
        with self._cv:
            self._cv.notify_all()

        return True

    def unregister(self, client: ClientProxy) -> None:
        """Unregister Flower ClientProxy instance.

        This method is idempotent.
        """
        if hasattr(client, "metadata_dict"):
            metadata_dict = getattr(client, "metadata_dict")
            if ZONE_CREDENTIAL in metadata_dict:
                credential = ZONE_CREDENTIAL
            elif CREDENTIAL in metadata_dict:
                credential = metadata_dict[CREDENTIAL]
            else:
                credential = NO_CREDENTIAL
        else:
            credential = NO_CREDENTIAL
        
        if credential in self.clients:
            if client.cid in self.clients[credential]:
                del self.clients[credential][client.cid]
                with self._cv:
                    self._cv.notify_all()

    def all(self) -> Dict[str, Dict[str, ClientProxy]]:
        """Return all available clients."""
        return self.clients

    def get_available_clients(
        self,
        min_num_clients: int = 2,
        credential: str = NO_CREDENTIAL,
        strict: bool = True,
    ) -> List[ClientProxy]:
        """get all available Daisy ClientProxy instances."""
        # Block until at least num_clients are connected.
        self.wait_for(min_num_clients, credential, strict)
        available_cids = list(self.clients[credential])
        available_cids_zone_credential = list(self.clients[ZONE_CREDENTIAL])
        available_cids_no_credential = list(self.clients[NO_CREDENTIAL]) \
            if (credential == NO_CREDENTIAL) or strict else []
        
        clients = [self.clients[credential][cid] for cid in available_cids]
        clients_zone_credential = [self.clients[ZONE_CREDENTIAL][cid] for cid in available_cids_zone_credential]
        clients_no_credential = [self.clients[NO_CREDENTIAL][cid] for cid in available_cids_no_credential]
        clients = clients + clients_zone_credential + clients_no_credential
        return clients

# TODO: 多個Task共用Clients如何確保Client availability
# TODO: 多個Task共用Clients如何確定選中Clients (其他Task不能來搶)