import json
import signal as os_signal
import os
from time import sleep
from typing import List
from rich import print as rich_rprint
from rich.progress import Progress, SpinnerColumn, TextColumn
import grpc
import typer
from .lib.broker import Broker

app = typer.Typer(help=help)


@app.command(help="List signals names on broker")
def signal_names(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    broker = Broker(url, api_key)
    # print("Listing available signals")
    available_signals = broker.list_signal_names()
    print(json.dumps(available_signals))


@app.command(help="Subscribe to signals")
def subscribe(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY'),
        signal: List[str] = typer.Option(..., help="Roles to apply"),
        namespace: str = typer.Option(..., help="Cloud Broker API-KEY or access token",
                                      envvar='REMOTIVE_BROKER_API_KEY'),
        on_change_only: bool = typer.Option(default=False, help="Only get signal if value is changed"),
        # samples: int = typer.Option(default=0, he)

):
    broker = Broker(url, api_key)
    print("Subscribing to signals, press Ctrl+C to exit")

    def exit_on_ctrlc(sig, frame):
        os._exit(0)

    def on_frame_func(x):
        rich_rprint(json.dumps(list(x)))

    os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

    #print(namespace)
    #signals2 = list(map( lambda s: s['signal'], broker.list_signal_names2(namespace)))

    broker.subscribe(signals, namespace, on_frame_func, on_change_only)


@app.command(help="List namespaces on broker")
def namespaces(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    broker = Broker(url, api_key)
    namespaces_json = broker.list_namespaces()
    print(json.dumps(namespaces_json))
