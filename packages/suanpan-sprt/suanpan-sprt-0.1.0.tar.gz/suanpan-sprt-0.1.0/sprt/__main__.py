import sys
import signal
import asyncio
import click
from hypercorn.asyncio import serve
from hypercorn.config import Config
from logging.config import dictConfig
from . import server


@click.command()
@click.option('-h', '--host', default='localhost', envvar='RT_HOST', help='Runtime host')
@click.option('-p', '--port', default=9988, envvar='RT_PORT', help='Runtime port')
@click.option('-l', '--log', default='debug', envvar='RT_LOGGING', help='logging level')
@click.option('-w', '--working-dir', default='.', envvar='RT_WORKING_DIR', help='working dir')
def main(host, port, log: str, working_dir: str):
    if log.upper() in ('CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG'):
        dictConfig({
            'version': 1,
            'loggers': {
                'sprt.server': {
                    'level': log.upper(),
                },
            },
        })

    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    app = server.create_app(working_dir)

    config = Config()
    config.bind = [f"{host}:{port}"]
    asyncio.run(serve(app, config))


def receive_signal(signal_number, frame):
    print('receive_signal', signal_number)
    sys.exit(128 + signal_number)


if __name__ == "__main__":
    main()
