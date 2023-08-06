from importlib import import_module, reload
import asyncio
from typing import Type
from arkitekt import Arkitekt
from watchfiles import awatch
from rich.prompt import Prompt
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.tree import Tree
from rich.traceback import Traceback
from rich.console import Group
from watchfiles.filters import BaseFilter, PythonFilter
import os
from rich import get_console
import sys
import inspect
import site

def import_builder(builder) -> Type[Arkitekt]:
    module_path, function_name = builder.rsplit(".", 1)
    module = import_module(module_path)
    function = getattr(module, function_name)
    return function



async def build_and_run(builder, identifier, version, entrypoint):

    app = builder(identifier, version)

    async with app:
        await app.rekuest.run()


    

class EntrypointFilter(PythonFilter):

    def __init__(self, entrypoint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entrypoint = entrypoint


    def __call__(self, change, path: str) -> bool:
        x = super().__call__(change, path)
        if not x:
            return False

        x = os.path.basename(path)
        module_name = x.split(".")[0]

        return module_name == self.entrypoint


class DeepFilter(PythonFilter):

    def __call__(self, change, path: str) -> bool:
        return super().__call__(change, path)

   

def reload_deeps(changes: set):
    normalized = [os.path.normpath(file) for modified, file in changes]

    reloadable_modules = set()
        
    for key, v in sys.modules.items():
        try:
            filepath = inspect.getfile(v)
        except:
            continue

        for i in normalized:
            if filepath.startswith(i):
                reloadable_modules.add(key)


    for module in reloadable_modules:
        reload(sys.modules[module])



async def dev_module(identifier, version, entrypoint,  builder: str = "arkitekt.builders.easy", deep: bool = False):

    

        
    builder_func = import_builder(builder)


    console = get_console()

    generation_message = f"Watching your arkitekt app"
   

    panel = Panel(generation_message, style="bold green", border_style="green")
    console.print(panel)


    try:
        module = import_module(entrypoint)
    except Exception as e:
        console.print_exception()
        panel = Panel(f"Error while importing your entrypoint please fix your file {entrypoint} and save", style="bold red", border_style="red")
        console.print(panel)
        module = None


    def callback(future):
        if future.cancelled():
            return
        else:
            try:
                raise future.exception()
            except Exception as e:
                console.print_exception()


    x = asyncio.create_task(build_and_run(builder_func, identifier, version, entrypoint))
    x.add_done_callback(callback)

    async for changes in awatch(".", watch_filter=EntrypointFilter(entrypoint) if not deep else DeepFilter(), debounce=2000, step=500):

        


        panel = Panel("Detected file changes", style="bold blue", border_style="bold blue")
        console.print(panel)
        # Cancelling the app
        if not x or x.done():
            pass

        else:
            x.cancel()
            panel = Panel("Cancelling old app", style="bold yellow", border_style="yellow")
            console.print(panel)
            try:
                await x

            except asyncio.CancelledError:
                pass

        
        # Restarting the app
        try:
            with console.status("Reloading module..."):
                if not module:
                    module = import_module(entrypoint)
                else:
                    if deep:
                        reload_deeps(changes)
                    else:
                        reload(module)

        except Exception as e:
            console.print_exception()
            panel = Panel("Reload unsucessfull please fix your app and save", style="bold red", border_style="red")
            console.print(panel)
            continue

        panel = Panel("Started App", style="bold green", border_style="green")
        console.print(panel)
        x = asyncio.create_task(build_and_run(builder_func, identifier, version, entrypoint))
        x.add_done_callback(callback)

   

    
    







