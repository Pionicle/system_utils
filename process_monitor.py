"""Show processes table: pid, name, cpu%, memory% (sorted by cpu%)."""

import time
import psutil
from tabulate import tabulate

HEADERS = ["pid", "name", "cpu_percent", "memory_percent"]


def collect_processes() -> list[dict]:
    """Return list of processes."""
    processes = list(psutil.process_iter(HEADERS))

    time.sleep(10)

    result = []
    for p in processes:
        try:
            result.append(p.as_dict(attrs=HEADERS))
        except psutil.NoSuchProcess, psutil.AccessDenied:
            pass

    return result


def create_table(processes: list[dict]) -> list[list]:
    """Return formatted table for print."""
    table = []
    for process in processes:
        table.append([process[header] for header in HEADERS])
    return tabulate(table, headers=HEADERS)


if __name__ == "__main__":
    processes = collect_processes()
    processes.sort(key=lambda p: (p["cpu_percent"], p["memory_percent"]), reverse=True)
    table = create_table(processes)
    print(table)
