from js import window, console

import asyncio
from pyodide.ffi import create_once_callable


async def waitAnimationFrame():
    event = asyncio.Event()

    def callback(*args):
        console.log('waitAnimationFrame callback!')
        console.log(args)
        event.set()

    window.requestAnimationFrame(create_once_callable(callback))
    await event.wait()
    console.log('waitAnimationFrame done')
