import asyncio
import itertools
import time

from commoner import Chalk


async def cycle(iterable):
    i = 0
    while True:
        print(iterable[i])
        await asyncio.sleep(0.1)
        i = (i + 1) % len(iterable)


async def start(iterable):
    task = asyncio.create_task(cycle(iterable))
    await task


def stop(task):
    task.cancel()


asyncio.run(start(['|', '/', '-', '\\']))
time.sleep(1)


class Wait:
    """
    A utility class for printing a loading animation to the console.

    Methods:
        start(): Starts the loading animation.
        stop(): Stops the loading animation.
        wait(seconds): Waits for the specified amount of time.
        input(message, color): Waits for the user to press a key.
    """

    class Loading:
        def start():
            """
            Starts the loading animation.

            Returns:
                None
            """
            # Start the loading animation
            for i in itertools.cycle(["|", "/", "-", "\\"]):
                print(f"\rLoading {i}", end="")
                time.sleep(0.05)

        def stop():
            """
            Stops the loading animation.

            Returns:
                None
            """
            # Stop the loading animation
            print("\r Completed! ", end="")

    @staticmethod
    def wait(seconds):
        """
        Waits for the specified amount of time.

        Parameters:
            seconds (int): The amount of time to wait.

        Returns:
            None
        """
        time.sleep(seconds)

    @staticmethod
    def input(message="Press any key to continue . . .", color="white"):
        """
        Waits for the user to press a key.

        Parameters:
            message (str): The message to print.
            color (str): The color of the message.

        Returns:
            None
        """
        input(f"{Chalk.set(color)}{message}{Chalk.reset()}")

    class Progress:
        """
        A utility class for printing a progress bar to the console.

        Methods:
            progress(current, total, message): Prints a progress bar.
            timed_progress(seconds, message): Prints a progress bar that counts down from a specified amount of time.
        """

        def __init__(self, total, character="#", reverse=False):
            self.total = total
            self.current = 0
            self.character = character
            self.reverse = reverse

        def display(percent, character, message="Loading . . .", reverse=False):
            """
            Displays a progress bar.

            Parameters:
                current (int): The current progress.
                total (int): The total progress.
                message (str): The message to print.

            Returns:
                None
            """
            bar = character * int(percent * 20)
            spaces = " " * (20 - len(bar))
            if reverse:
                print(f"\r{message} [{bar}{spaces}] {100 - percent * 100:.2f}%", end="")
            else:
                print(f"\r{message} [{bar}{spaces}] {percent * 100:.2f}%", end="")

        def start(self, message="Loading . . ."):
            """
            Prints a progress bar.

            Parameters:
                message (str): The message to print.

            Returns:
                None
            """
            Wait.Progress.display(0, self.character, message, self.reverse)

        def update(self, current, message="Loading . . ."):
            """
            Updates the progress bar.

            Parameters:
                current (int): The current progress.
                message (str): The message to print.

            Returns:
                None
            """
            percent = current / self.total
            Wait.Progress.display(percent, self.character, message, self.reverse)

        def finish(self, message="Finished!"):
            print("\r", end="")
            Wait.Progress.display(1, self.character, message)

        def timed(seconds, character="#", message="Loading . . .", reverse=False):
            """
            Displays a progress bar that counts down from a specified amount of time.

            Parameters:
                seconds (int): The amount of time to count down from.
                character (str): The character to use for the progress bar.
                message (str): The message to print.

            Returns:
                None
            """
            bar = Wait.Progress(1, character, reverse)
            bar.start(message)
            for i in range(seconds):
                bar.update(i / seconds, message)
                time.sleep(1)
            bar.finish()
