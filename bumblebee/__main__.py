import signal
from threading import Thread

from appdirs import AppDirs

from bumblebee.bqclient import BQClient
from bumblebee.host import Host
from bumblebee.host.framework.ioc import Resolver
from bumblebee.host.must_be_host_guard import MustBeHostGuard

resolver = Resolver.get()

app_dirs = AppDirs(appname='BQClient')
resolver.instance(app_dirs)

# This ensures that the events of BQClient are registered
client = resolver(BQClient)

must_be_host_guard: MustBeHostGuard = resolver(MustBeHostGuard)

must_be_host_guard()

host: Host = resolver(Host)

thread = Thread(target=host.run)


def stop_host():
    host.stop()


signal.signal(signal.SIGINT, stop_host)

thread.start()
thread.join()
