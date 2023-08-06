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
"""Flower server."""


import concurrent.futures
import timeit
from threading import Event, Condition
from queue import Queue
from logging import DEBUG, INFO
from typing import Dict, List, Optional, Tuple, Union, Callable

from daisyfl.common import (
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    Code,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
    NO_CREDENTIAL,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.server.history import History

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]
EVENT_SET = "EVENT_SET"
FAILURES_NUM = "FAILURES_NUM"
RESULTS_NUM = "RESULTS_NUM"
SELECTED_NUM = "SELECTED_NUM"    

class Server:
    """Flower server."""

    def __init__(
        self, *, 
        client_manager: ClientManager,
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self._max_workers: Optional[int] = None
        self.tickets = {}

    # set Server attributes
    def set_max_workers(self, max_workers: Optional[int]) -> None:
        """Set the max_workers used by ThreadPoolExecutor."""
        self._max_workers = max_workers

    # get Server attributes
    def get_client_manager(self) -> ClientManager:
        """Return ClientManager."""
        return self._client_manager

    def get_max_workers(self) -> Optional[int]:
        """Return max_workers."""
        return self._max_workers
    
    # ClientManager APIs 
    def num_available(self, credential: str = NO_CREDENTIAL, strict: bool = True,) -> int:
        return self._client_manager.num_available(credential=credential, strict=strict)
        
    def get_available_clients(
        self,
        min_num_clients: int = 2,
        credential: str = NO_CREDENTIAL,
        strict: bool = True,
    ) -> List[ClientProxy]:
        return self._client_manager.get_available_clients(
            min_num_clients=min_num_clients,
            credential=credential,
            strict=strict,
        )

    # TODO:
    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        all_clients = self.get_client_manager().all()
        clients = [all_clients[k] for k in all_clients.keys()]
        instruction = ReconnectIns(seconds=None)
        client_instructions = [(client_proxy, instruction) for client_proxy in clients]
        _ = self._reconnect_clients(
            client_instructions=client_instructions,
            max_workers=self.get_max_workers(),
            timeout=timeout,
        )

    def fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
        ticket: int,
    ) -> None:
        event = Event()
        self.tickets[ticket] = {
            EVENT_SET: event.set,
            SELECTED_NUM: len(client_instructions),
            RESULTS_NUM: 0,
            FAILURES_NUM: 0,
        }
        return self._fit_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
            timeout=timeout,
            returns_q=returns_q,
            event=event,
            ticket=ticket,
        )
    
    def evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
        ticket: int,
    ) -> None:
        event = Event()
        self.tickets[ticket] = {
            EVENT_SET: event.set,
            SELECTED_NUM: len(client_instructions),
            RESULTS_NUM: 0,
            FAILURES_NUM: 0,
        }
        return self._evaluate_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
            timeout=timeout,
            returns_q=returns_q,
            event=event,
            ticket=ticket,
        )

    def stop_return(self, ticket: int) -> bool:
        if self.check_ticket(ticket):
            self.tickets[ticket][EVENT_SET]()
            del self.tickets[ticket]
            return True
        return False

    def query_status(self, ticket: int,) -> Tuple[int, int, int]:
        if self.check_ticket(ticket):
            return self.tickets[ticket][SELECTED_NUM], self.tickets[ticket][RESULTS_NUM], self.tickets[ticket][FAILURES_NUM]
    
    def check_ticket(self, ticket) -> bool:
        if ticket in self.tickets:
            return True
        return False

    def _reconnect_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, ReconnectIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> ReconnectResultsAndFailures:
        """Instruct clients to disconnect and never reconnect."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._reconnect_client, self, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }
            finished_fs, _ = concurrent.futures.wait(
                fs=submitted_fs,
                timeout=None,  # Handled in the respective communication stack
            )

        # Gather results
        results: List[Tuple[ClientProxy, DisconnectRes]] = []
        failures: List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]] = []
        for future in finished_fs:
            failure = future.exception()
            if failure is not None:
                failures.append(failure)
            else:
                result = future.result()
                results.append(result)
        return results, failures


    def _reconnect_client(
        self,
        client: ClientProxy,
        reconnect: ReconnectIns,
        timeout: Optional[float],
    ) -> Tuple[ClientProxy, DisconnectRes]:
        """Instruct client to disconnect and (optionally) reconnect later."""
        disconnect = client.reconnect(
            reconnect,
            timeout=timeout,
        )
        return client, disconnect


    def _fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
        event: Event,
        ticket: int,
    ) -> None:
        """Refine parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._fit_client, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }
            
            for f in submitted_fs:
                f.add_done_callback(self._get_future_callback_fn(returns_q=returns_q, event=event, ticket=ticket))
            return 


    def _fit_client(
        self, client: ClientProxy, ins: FitIns, timeout: Optional[float]
    ) -> Tuple[ClientProxy, FitRes]:
        """Refine parameters on a single client."""
        fit_res = client.fit(ins, timeout=timeout)
        return client, fit_res


    def _evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
        event: Event,
        ticket: int,
    ) -> None:
        """Evaluate parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._evaluate_client, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }

            for f in submitted_fs:
                f.add_done_callback(self._get_future_callback_fn(returns_q=returns_q, event=event, ticket=ticket))
            return


    def _evaluate_client(
        self,
        client: ClientProxy,
        ins: EvaluateIns,
        timeout: Optional[float],
    ) -> Tuple[ClientProxy, EvaluateRes]:
        """Evaluate parameters on a single client."""
        evaluate_res = client.evaluate(ins, timeout=timeout)
        return client, evaluate_res


    def _get_future_callback_fn(
        self,
        returns_q: Queue,
        event: Event,
        ticket: int,
    ) -> None:
        """Convert finished future into either a result or a failure."""
        def future_callback_fn(future: concurrent.futures.Future):
            # Expired
            if event.is_set():
                return
            self._handle_future(future, returns_q, ticket)
        return future_callback_fn

    # TODO: results and failures to job
    def _handle_future(self, future, returns_q: Queue, ticket: int) -> None:
        # Check if there was an exception
        failure: Union[Tuple[ClientProxy, EvaluateRes], BaseException] = future.exception()
        if failure is not None:
            self.tickets[ticket][FAILURES_NUM] = self.tickets[ticket][FAILURES_NUM] + 1
            return
        
        # Successfully received a result from a client
        result: Tuple[ClientProxy, FitRes] = future.result()
        _, res = result

        # Check result status code
        if res.status.code == Code.OK:
            self.tickets[ticket][RESULTS_NUM] = self.tickets[ticket][RESULTS_NUM] + 1
            returns_q.put(result)
            return
        
        # Not successful, client returned a result where the status code is not OK
        self.tickets[ticket][FAILURES_NUM] = self.tickets[ticket][FAILURES_NUM] + 1
        return

