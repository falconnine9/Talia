import asyncio

import discord


class TaliaInstance(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {}
        self.aliases = {}
        self.services = {}
        self.prefixes = {}
        self.cld_timers = {}
        self.inv_timers = {}
        self.conn = None

    def run_wrapper(self, *args, **kwargs):
        for service in self.services:
            self.loop.create_task(self.services[service].func())

        try:
            self.start(*args, **kwargs)
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.close())
        finally:
            self.loop.close()
            if self.conn is not None:
                self.conn.close()

    def command(self, command_):
        def decor(func):
            command_.func = func
            self.commands[command_.name] = command_
            for alias in command_.aliases:
                self.aliases[alias] = command_
            return func
        return decor

    def service(self, service_):
        def decor(func):
            service_.func = func
            self.services[service_.name] = service_
            return func
        return decor


intents = discord.Intents.all()
client = TaliaInstance(intents=intents)