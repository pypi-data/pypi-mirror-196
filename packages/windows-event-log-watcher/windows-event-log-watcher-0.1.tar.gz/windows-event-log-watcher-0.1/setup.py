from setuptools import setup, find_packages

setup(
    name='windows-event-log-watcher',
    version='0.1',
    packages=find_packages(),
    install_requires=['pypiwin32'],
    entry_points={
        'console_scripts': [
            'watch_event_log=my_windows_event_log_watcher:watch_event_log',
            'realtime_event_log=my_windows_event_log_watcher:realtime_event_log'
        ]
    }
)
