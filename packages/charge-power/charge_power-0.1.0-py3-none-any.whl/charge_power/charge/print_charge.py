"""Function used to print battery charge change is defined here."""
import datetime
import time
from typing import Callable, Iterable, NoReturn, TextIO

from rich.console import Console


def _prepare_print(  # pylint: disable=too-many-arguments
    iteration: int,
    old_time_ns: int,
    old_value: float,
    new_time_ns: int,
    new_value: float,
    full_wattage: float,
) -> str:
    """Prepare concrete measurement of wattage difference message for rich.Console print"""
    real_delay = new_time_ns - old_time_ns
    delay_seconds = round(real_delay / 1_000_000_000)
    difference = new_value - old_value

    per_hour = difference * 1_000_000_000 * 3600 / real_delay
    if difference == 0:
        return (
            f"{datetime.datetime.now().strftime('%m-%d %H:%M:%S')} ({iteration:3}):    stable"
            f" [cyan]{0.0}[/cyan]W per hour: [green]{new_value:5.2f}[/green]W of"
            f" {full_wattage:.2f}W ({new_value / full_wattage * 100:.1f}%)"
        )
    time_left = (full_wattage - new_value) / per_hour * 60 if difference > 0 else (new_value) / -per_hour * 60
    time_left_str = (
        f"{time_left:4.1f} minutes" if time_left < 60 else f"{time_left // 60:.0f}:{time_left % 60:02.0f} hours"
    )
    if difference > 0:
        return (
            f"{datetime.datetime.now().strftime('%m-%d %H:%M:%S')} ({iteration:3}):    charge"
            f" {difference * 1000:7.2f}mW per {delay_seconds} seconds"
            f" ([green]{per_hour:7.2f}[/green]W per hour):"
            f" [yellow]{old_value:5.2f}[/yellow]W -> [green]{new_value:5.2f}[/green]W of"
            f" {full_wattage:.2f}W ({new_value / full_wattage * 100:.1f}%,"
            f" [i]{time_left_str} minutes to full[/i])"
        )
    return (
        f"{datetime.datetime.now().strftime('%m-%d %H:%M:%S')} ({iteration:3}): discharge"
        f" {difference * 1000:7.2f}mW per {delay_seconds} seconds ([red]{per_hour:7.2f}[/red]W per hour):"
        f" [yellow]{old_value:5.2f}[/yellow]W -> [red]{new_value:5.2f}[/red]W of"
        f" {full_wattage:.2f}W ({new_value / full_wattage * 100:.1f}%,"
        f" [i]{time_left_str} minutes to zero[/i])"
    )


def print_battery_charge(  # pylint: disable=too-many-arguments
    get_charge: Callable[[], int],
    full_wattage: float,
    delay_seconds: int,
    rng: Iterable,
    console: Console = ...,
    logfile: TextIO | None = None,
) -> None | NoReturn:
    """Print battery charge/discharge status for values in the given range

    Args:
        get_charge (Callable[[], int]): function used to get current charge value in Watts
        delay_seconds (int): delay between measurements in seconds
        rng (Iterable): range for printing values
        console (Console, optional): rich.Console object to print to

    Returns:
        None | NoReturn: if range is endless, never return.
    """
    if console is ... or console is None:
        console = Console(highlight=False, emoji=False)

    if logfile is not None:
        console_file = Console(file=logfile)

        def print_result(text: str):
            console.print(text)
            console_file.print(text)

    else:

        def print_result(text: str):
            console.print(text)

    for i, _ in enumerate(rng):
        old_value = get_charge()
        old_time = time.clock_gettime_ns(time.CLOCK_REALTIME)
        time.sleep(delay_seconds)
        new_value = get_charge()
        new_time = time.clock_gettime_ns(time.CLOCK_REALTIME)

        print_result(_prepare_print(i, old_time, old_value, new_time, new_value, full_wattage))
