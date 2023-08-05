#!/usr/bin/python

from .. import __version__
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import logging
import os
import pgworkload_odbc.models.run
import pgworkload_odbc.models.util
import pgworkload_odbc.utils.util
import platform
import re
import sys
import typer
import yaml


EPILOG = "GitHub: <https://github.com/fabiog1901/pgworkload>"

logger = logging.getLogger(__name__)

app = typer.Typer(
    epilog=EPILOG,
    no_args_is_help=True,
    help=f"pgworkload v{__version__}: Workload utility for the PostgreSQL protocol.",
)

# util_app = typer.Typer(
#     epilog=EPILOG,
#     no_args_is_help=True,
#     help="Generate YAML data generation files and CSV datasets.",
# )
# app.add_typer(util_app, name="util")


version: bool = typer.Option(True)


class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"


class Param:
    LogLevel = typer.Option(
        "info", "--log-level", "-l", show_choices=True, help="Set the logging level."
    )

    WorkloadPath = typer.Option(
        ...,
        "--workload",
        "-w",
        help="Filepath to the workload module.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )

    Procs = typer.Option(
        None,
        "--procs",
        "-x",
        help="Number of processes to spawn. Defaults to <system-cpu-count>.",
        show_default=False,
    )

    DBUrl = typer.Option(
        "postgres://root@localhost:26257/postgres?sslmode=disable",
        "--url",
        help="The connection string to the database.",
    )

    Args = typer.Option(
        None, help="JSON string, or filepath to a JSON/YAML file, to pass to Workload."
    )

    HTTPServerPort = typer.Option(
        3000,
        "-p",
        "--port",
        help="The port of the http server that servers the CSV files.",
    )

    HTTPServerHostName = typer.Option(
        None,
        "-n",
        "--hostname",
        show_default=False,
        help="The hostname of the http server that serves the CSV files.",
    )

    CSVMaxRows = typer.Option(100000, help="Max count of rows per resulting CSV file.")


@app.command(help="Run the workload.", epilog=EPILOG, no_args_is_help=True)
def run(
    workload_path: Optional[Path] = Param.WorkloadPath,
    dburl: str = Param.DBUrl,
    procs: int = Param.Procs,
    args: str = Param.Args,
    concurrency: int = typer.Option(
        1, "-c", "--concurrency", help="Number of concurrent workers."
    ),
    ramp: int = typer.Option(0, "-r", "--ramp", help="Ramp up time in seconds."),
    iterations: int = typer.Option(
        None,
        "-i",
        "--iterations",
        help="Total number of iterations. Defaults to <ad infinitum>.",
        show_default=False,
    ),
    duration: int = typer.Option(
        None,
        "-d",
        "--duration",
        help="Duration in seconds. Defaults to <ad infinitum>.",
        show_default=False,
    ),
    conn_duration: int = typer.Option(
        None,
        "-k",
        "--conn-duration",
        show_default=False,
        help="The number of seconds to keep database connection alive before restarting. Defaults to <ad infinitum>.",
    ),
    app_name: Optional[str] = typer.Option(
        None,
        "--app-name",
        "-a",
        help="The application name specified by the client. Defaults to <db-name>.",
        show_default=False,
    ),
    autocommit: bool = typer.Option(
        True,
        "--no-autocommit",
        show_default=False,
        help="Unset autocommit in the connections.",
    ),
    frequency: int = typer.Option(
        10, "-s", "--stats-frequency", help="How often to display the stats in seconds."
    ),
    prom_port: int = typer.Option(
        26260, "-p", "--port", help="The port of the Prometheus server."
    ),
    log_level: LogLevel = Param.LogLevel,
):
    logger.setLevel(log_level.upper())

    logger.debug("Executing run()")

    procs, dburl, args = __validate(procs, dburl, app_name, args, workload_path)

    pgworkload_odbc.models.run.run(
        conc=concurrency,
        workload_path=workload_path,
        frequency=frequency,
        prom_port=prom_port,
        iterations=iterations,
        procs=procs,
        ramp=ramp,
        dburl=dburl,
        autocommit=autocommit,
        duration=duration,
        conn_duration=conn_duration,
        args=args,
        log_level=log_level.upper(),
    )



def __validate(procs: int, dburl: str, app_name: str, args: str, workload_path: str):
    """Performs pgworkload initialization steps

    Args:
        args (argparse.Namespace): args passed at the CLI

    Returns:
        argparse.Namespace: updated args
    """
    workload = pgworkload_odbc.utils.util.import_class_at_runtime(workload_path)

    if not procs:
        procs = os.cpu_count()
    

    # load args dict from file or string
    if args:
        if os.path.exists(args):
            with open(args, "r") as f:
                args = f.read()
                # parse into JSON if it's a JSON string
                try:
                    args = json.load(args)
                except Exception as e:
                    pass
        else:
            args = yaml.safe_load(args)
            if isinstance(args, str):
                logger.error(
                    f"The value passed to '--args' is not a valid path to a JSON/YAML file, nor has no key:value pairs: '{args}'"
                )
                sys.exit(1)
    else:
        args = {}
    return procs, dburl, args


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pgworkload : {__version__}")
        typer.echo(f"Python     : {platform.python_version()}")
        raise typer.Exit()


@app.callback()
def version_option(
    _: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=_version_callback,
        help="Print the version and exit",
    ),
) -> None:
    pass
