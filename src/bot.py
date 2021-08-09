import asyncio

import discord

from talia.obj.command import Command
from talia.obj.service import Service


class TaliaInstance(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {}
        self.services = {}
        self.conn = None

    def run_wrapper(self, *args, **kwargs):
        for service in self.services:
            self.loop.create_task(self.services[service].func())
        self.run(*args, **kwargs)

    def command(self, **kw):
        def decor(func):
            if "name" not in kw:
                raise ValueError("command name not given")
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("function is not coroutine")
            kw["func"] = func
            self.commands[kw["name"]] = Command(**kw)
            return func
        return decor

    def service(self, **kw):
        def decor(func):
            if "name" not in kw:
                raise ValueError("service name not given")
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("function is not coroutine")
            kw["func"] = func
            self.services[kw["name"]] = Service(**kw)
            return func
        return decor


client = TaliaInstance()