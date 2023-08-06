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
"""Contextmanager managing a gRPC channel to the Flower server."""


from contextlib import contextmanager
from logging import DEBUG, INFO, WARNING
from queue import Queue
from typing import Callable, Iterator, Optional, Tuple

import grpc

from daisyfl.common import GRPC_MAX_MESSAGE_LENGTH
from daisyfl.common.logger import log
from daisyfl.proto.transport_pb2 import ClientMessage, ServerMessage
from daisyfl.proto.transport_pb2_grpc import FlowerServiceStub

# The following flags can be uncommented for debugging. Other possible values:
# https://github.com/grpc/grpc/blob/master/doc/environment_variables.md
# import os
# os.environ["GRPC_VERBOSITY"] = "debug"
# os.environ["GRPC_TRACE"] = "tcp,http"


def on_channel_state_change(channel_connectivity: str) -> None:
    """Log channel connectivity."""
    log(DEBUG, channel_connectivity)


@contextmanager
def grpc_connection(
    parent_address: str,
    max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    root_certificates: Optional[bytes] = None,
    metadata: Tuple = None,
) -> Iterator[Tuple[Callable[[], ServerMessage], Callable[[ClientMessage], None]]]:
    """Establish an insecure gRPC connection to a gRPC server.

    Parameters
    ----------
    server_address : str
        The IPv6 address of the server. If the Flower server runs on the same machine
        on port 8080, then `server_address` would be `"[::]:8080"`.
    max_message_length : int
        The maximum length of gRPC messages that can be exchanged with the Flower
        server. The default should be sufficient for most models. Users who train
        very large models might need to increase this value. Note that the Flower
        server needs to be started with the same value
        (see `flwr.server.start_server`), otherwise it will not know about the
        increased limit and block larger messages.
        (default: 536_870_912, this equals 512MB)
    root_certificates : Optional[bytes] (default: None)
        The PEM-encoded root certificates as a byte string. If provided, a secure
        connection using the certificates will be established to a SSL-enabled
        Flower server.

    Returns
    -------
    receive, send : Callable, Callable

    Examples
    --------
    Establishing a SSL-enabled connection to the server:

    >>> from pathlib import Path
    >>> with grpc_connection(
    >>>     server_address,
    >>>     max_message_length=max_message_length,
    >>>     root_certificates=Path("/crts/root.pem").read_bytes(),
    >>> ) as conn:
    >>>     receive, send = conn
    >>>     server_message = receive()
    >>>     # do something here
    >>>     send(client_message)
    """
    # Possible options:
    # https://github.com/grpc/grpc/blob/v1.43.x/include/grpc/impl/codegen/grpc_types.h
    channel_options = [
        ("grpc.max_send_message_length", max_message_length),
        ("grpc.max_receive_message_length", max_message_length),
    ]

    if root_certificates is not None:
        ssl_channel_credentials = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(
            parent_address, ssl_channel_credentials, options=channel_options
        )
        log(INFO, "Opened secure gRPC connection using certificates")
    else:
        channel = grpc.insecure_channel(parent_address, options=channel_options)
        log(INFO, "Opened insecure gRPC connection (no certificates were passed)")

    channel.subscribe(on_channel_state_change)

    queue: Queue[ClientMessage] = Queue(  # pylint: disable=unsubscriptable-object
        maxsize=1
    )
    stub = FlowerServiceStub(channel)

    server_message_iterator: Iterator[ServerMessage] = stub.Join(iter(queue.get, None), metadata=metadata)

    receive: Callable[[], ServerMessage] = lambda: next(server_message_iterator)
    send: Callable[[ClientMessage], None] = lambda msg: queue.put(msg, block=False)

    try:
        yield (receive, send)
    finally:
        # Make sure to have a final
        channel.close()
        log(DEBUG, "gRPC channel closed")

reconnect: bool = False
connect_to: str = ""
sleep_duration: int = 0

def reconnect_request(address: str = None, sleep: int = None) -> None:
    set_reconnect(True)
    if isinstance(address, str):
        set_connect_to(address)
    else:
        log(
            WARNING, "Parent address doesn't change. Parent = %s",
            connect_to,
        )
    if isinstance(sleep, int):
        set_sleep_duration(sleep)
    else:
        log(
            WARNING, "Sleep duration doesn't change. Sleep duration = %s",
            sleep_duration,
        )

def get_reconnect() -> bool:
    global reconnect
    return reconnect

def set_reconnect(rec: bool) -> None:
    global reconnect
    reconnect = rec

def get_connect_to() -> str:
    global connect_to
    return connect_to

def set_connect_to(con2: str) -> None:
    global connect_to
    connect_to = con2

def get_sleep_duration() -> int:
    global sleep_duration
    return sleep_duration

def set_sleep_duration(sleep: int) -> None:
    global sleep_duration
    sleep_duration = sleep
    