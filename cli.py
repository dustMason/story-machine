import asyncio
from typing import Optional

from rich.console import Console
from story import Story

if __name__ == "__main__":
    async def run():
        console = Console(width=80)
        subject = console.input("Enter a story subject:\n")
        story = Story(subject=subject)

        async def step(choice: Optional[int] = None):
            line_width = 0
            async for bit in story.generate_next_bit(choice):
                line_width += len(bit)
                start = ""
                if bit == "\n":
                    line_width = 0
                if bit and bit[0] == " " and line_width > 80 and bit[-1] != "." and bit[-1] != ",":
                    start = "\n"
                    line_width = 0
                console.print(start + bit, end="")
            console.print("\n")
            with console.status("Updating synopsis..."):
                await story.generate_next_synopsis_item()

        await step()
        while True:
            choice = int(console.input("\n[bold red]What is your choice?[/] "))
            await step(choice)

    asyncio.run(run())