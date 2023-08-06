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
from logging import INFO, WARNING
from typing import Dict, List, Optional, Tuple, TypedDict, Callable
from queue import Queue
from threading import Timer, Condition, Event
from daisyfl.operator.strategy import Strategy
from daisyfl.common import (
    Parameters,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
    PERIOD,
    NO_CREDENTIAL,
    CREDENTIAL,
    STRICT_SELECTION,
)
from daisyfl.common.logger import log

from daisyfl.operator.utils import (
    get_configure_fit,
    aggregate_fit,
    generate_fit_report,
    get_configure_evaluate,
    aggregate_evaluate,
    generate_evaluate_report,
    get_results_from_queue,
)


class ServerLogic():
    def __init__(self,
        server,
        strategy: Strategy,
        ticket_dispenser: Callable,
    ) -> None:
        self.server = server
        self.strategy: Strategy = strategy
        self.ticket_dispenser_fn = ticket_dispenser
        self.tickets = []

    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        self.server.disconnect_all_clients(timeout=timeout)

    def fit_round(
        self,
        parameters: Parameters,
        task: Task,
        returns_q: Queue,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        """Perform a single round fit."""
        # Get clients and their respective instructions from strategy
        ## credential
        credential = task.config[CREDENTIAL] if CREDENTIAL in task.config else NO_CREDENTIAL
        strict = task.config[STRICT_SELECTION] if STRICT_SELECTION in task.config else True
        ## get_clients
        client_instructions = get_configure_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            server=self.server,
            config=task.config,
            credential=credential,
            strict=strict,
        )
        # Collect `fit` results from all clients participating in this round
        ticket = self.ticket_dispenser_fn()
        self.tickets.append(ticket)
        self.server.fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
            returns_q=returns_q,
            ticket=ticket,
        )
        # periodically check
        event = Event()
        while(not event.is_set()):
            cnd = Condition()
            timer = Timer(task.config[PERIOD], self.notify, [cnd])
            timer.start()
            with cnd:
                cnd.wait()
            selected, results_num, failures_num = self.server.query_status(ticket)
            if not self.check_enough_returns(event, 0.8, 2, selected, results_num, failures_num):
                return parameters, generate_fit_report(task.config[CURRENT_ROUND], 0, {},)
        self.server.stop_return(ticket)
        results = get_results_from_queue(returns_q=returns_q)
        # Aggregate training results
        parameters_aggregated, samples, metrics_aggregated  = aggregate_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            results=results,
            failures=[],
        )
        # Get report
        report = generate_fit_report(
            server_round=task.config[CURRENT_ROUND],
            samples=samples,
            metrics_aggregated=metrics_aggregated,
        )

        return parameters_aggregated, report

    def evaluate_round(
        self,
        parameters: Parameters,
        task: Task,
        returns_q: Queue,
    ) -> Optional[Report]:
        """Validate current global model on a number of clients."""
        # Get clients and their respective instructions from strategy
        ## credential
        credential = task.config[CREDENTIAL] if CREDENTIAL in task.config else NO_CREDENTIAL
        strict = task.config[STRICT_SELECTION] if STRICT_SELECTION in task.config else True
        ## get_clients
        client_instructions = get_configure_evaluate(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            server=self.server,
            config=task.config,
            credential=credential,
            strict=strict,
        )
        # Collect `evaluate` results from all clients participating in this round
        ticket = self.ticket_dispenser_fn()
        self.server.evaluate_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
            returns_q=returns_q,
            ticket=ticket,
        )
        # periodically check
        event = Event()
        while(not event.is_set()):
            cnd = Condition()
            timer = Timer(task.config[PERIOD], self.notify, [cnd])
            timer.start()
            with cnd:
                cnd.wait()
            selected, results_num, failures_num = self.server.query_status(ticket)
            if not self.check_enough_returns(event, 0.8, 2, selected, results_num, failures_num):
                return parameters, generate_fit_report(task.config[CURRENT_ROUND], 0, {},)
        self.server.stop_return(ticket)
        results = get_results_from_queue(returns_q=returns_q)
        # Aggregate the evaluation results
        loss_aggregated, samples, metrics_aggregated = aggregate_evaluate(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            results=results,
            failures=[],
        )
        # Get report
        report = generate_evaluate_report(
            server_round=task.config[CURRENT_ROUND],
            samples=samples,
            loss_aggregated=loss_aggregated,
            metrics_aggregated=metrics_aggregated,
        )

        return report

    def notify(self, cnd: Condition):
        with cnd:
            cnd.notify()

    def check_enough_returns(self, event: Event, fraction: float, min_num: int, selected: int, results_num: int, failures_num: int) -> bool:
        if ((fraction * selected <= results_num) and (min_num <= results_num)):
            event.set()
            return True
        if ((fraction * selected) <= (selected - failures_num)) and (min_num <= (selected - failures_num)):
            return True
        return False
