import os
import sys
import socket
import signal
import errno
import argparse
import configparser
from multiprocessing import Process
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
import datetime
import json
import daemon
from pathlib import Path
from colorama import init, Fore, Style
import platform
from importlib import import_module

init()

def worker(sock, app, concurrency):
    pool = Pool(concurrency)

    while True:
        try:
            client_connection, client_address = sock.accept()
            server = WSGIServer(sock.getsockname(), app, spawn=pool)
            server.handle(client_connection, client_address)
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise

class Zuicorn:
    def __init__(self, app, host='127.0.0.1', port=8000, workers=4, concurrency=1000):
        self.host = host
        self.port = port
        self.workers = workers
        self.concurrency = concurrency
        self.worker_processes = []
        self.app = app
        self.logs = []

    def start_worker_processes(self):
        for _ in range(self.workers):
            worker_process = Process(target=worker, args=(self.sock, self.app, self.concurrency))
            self.worker_processes.append(worker_process)
            worker_process.start()

    def stop_worker_processes(self):
        for worker_process in self.worker_processes:
            worker_process.terminate()
            worker_process.join()

    def run(self, is_daemon=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.start_worker_processes()

        try:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGQUIT, signal.SIG_IGN)
            signal.signal(signal.SIGUSR1, signal.SIG_IGN)

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_message = f"[{timestamp}] {Fore.GREEN}INFO:{Style.RESET_ALL} Starting WSGI server"
            self.logs.append(log_message)

            print(log_message)

            log_message = f"[{timestamp}] {Fore.GREEN}INFO:{Style.RESET_ALL} Listening at: {Fore.BLUE}http://{self.host}:{self.port}{Style.RESET_ALL} ({os.getpid()})"
            self.logs.append(log_message)

            print(log_message)

            log_message = f"[{timestamp}] {Fore.GREEN}INFO:{Style.RESET_ALL} Using worker: {Fore.YELLOW}gevent{Style.RESET_ALL}"
            self.logs.append(log_message)

            print(log_message)

            for worker_process in self.worker_processes:
                log_message = f"[{timestamp}] {Fore.GREEN}INFO:{Style.RESET_ALL} Booting worker with pid: {worker_process.pid}"
                self.logs.append(log_message)

                print(log_message)

            if is_daemon:
                log_message = f"[{timestamp}] {Fore.CYAN}INFO:{Style.RESET_ALL} Running as a daemon process"
                self.logs.append(log_message)

                while True:
                    pass
            else:
                for worker_process in self.worker_processes:
                    worker_process.join()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_worker_processes()

    def reload(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {Fore.YELLOW}INFO:{Style.RESET_ALL} Reloading worker processes"
        self.logs.append(log_message)

        print(log_message)

        self.stop_worker_processes()
        self.start_worker_processes()

        for worker_process in self.worker_processes:
            log_message = f"[{timestamp}] {Fore.GREEN}INFO:{Style.RESET_ALL} Booting worker with pid: {worker_process.pid}"
            self.logs.append(log_message)

            print(log_message)

    def stop(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {Fore.RED}INFO:{Style.RESET_ALL} Stopping the server"
        self.logs.append(log_message)

        print(log_message)

        self.stop_worker_processes()

    def save_logs(self, log_path):
        with open(log_path, 'w') as log_file:
            json.dump(self.logs, log_file)


def log_request(environ, start_response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    remote_addr = environ.get('REMOTE_ADDR', '-')
    method = environ.get('REQUEST_METHOD', '-')
    path = environ.get('PATH_INFO', '-')
    protocol = environ.get('SERVER_PROTOCOL', '-')
    status = start_response.status.split()[0] if hasattr(start_response, 'status') else '-'
    content_length = start_response.headers.get('Content-Length', '-')
    response_time = (datetime.datetime.now() - start_response.start_time).total_seconds()
    response_time = f"{response_time:.6f}" if response_time is not None else '-'

    log_line = f"{remote_addr} - - [{timestamp}] \"{method} {path} {protocol}\" {status} {content_length} {response_time}"
    colored_log_line = f"[{timestamp}] {Fore.CYAN}{log_line}{Style.RESET_ALL}"

    print(colored_log_line)


def main():
    parser = argparse.ArgumentParser(description='WSGI server')
    parser.add_argument('app', help='The WSGI application object (e.g., module:app)')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker processes (default: 4)')
    parser.add_argument('--concurrency', type=int, default=1000, help='Concurrency level (default: 1000)')
    parser.add_argument('--host', default='localhost', help='Host address (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    parser.add_argument('--config', help='Configuration file (default: None)')
    parser.add_argument('--daemon', action='store_true', help='Run as a daemon process')
    parser.add_argument('--reload', action='store_true', help='Reload worker processes')
    parser.add_argument('--stop', action='store_true', help='Stop the server')
    parser.add_argument('--kill', type=int, metavar='PID', help='Kill the daemon process with the given PID')
    args = parser.parse_args()

    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)
        server_config = config['server']
        app_config = server_config['app']
        workers_config = int(server_config.get('workers', args.workers))
        concurrency_config = int(server_config.get('concurrency', args.concurrency))
        host_config = server_config.get('host', args.host)
        port_config = int(server_config.get('port', args.port))
    else:
        app_config = args.app
        workers_config = args.workers
        concurrency_config = args.concurrency
        host_config = args.host
        port_config = args.port

    module_name, app_name = app_config.split(':')
    module_file = os.path.abspath(os.path.join(os.getcwd(), module_name.replace('.', os.sep) + '.py'))
    module_dir = os.path.dirname(module_file)

    sys.path.insert(0, module_dir)
    module = import_module(module_name)
    app = getattr(module, app_name)

    server = Zuicorn(app, host=host_config, port=port_config, workers=workers_config, concurrency=concurrency_config)

    if args.kill:
        try:
            os.kill(args.kill, signal.SIGTERM)
        except ProcessLookupError:
            print(f"{Fore.RED}No such process exists.{Style.RESET_ALL}")
            sys.exit(1)
        else:
            print(f"{Fore.GREEN}Daemon process killed.{Style.RESET_ALL}")
            sys.exit(0)
    elif args.daemon:
        with daemon.DaemonContext():
            server.run(is_daemon=True)
    elif args.reload:
        server.reload()
    elif args.stop:
        server.stop()
    else:
        server.run()

    # Save logs
    if platform.system() == 'Windows':
        log_dir = os.path.join(os.getenv('APPDATA'), 'zyloWSGI', 'logs')
    else:
        log_dir = os.path.join(Path.home(), 'zyloWSGI', 'logs')

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'wsgi.json')

    server.save_logs(log_path)


if __name__ == '__main__':
    main()

