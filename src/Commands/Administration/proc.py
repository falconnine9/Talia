"""
Talia Discord Bot
GNU General Public License v3.0
proc.py (Commands/Administration)

proc command
"""
import psutil
import os
from Utils import user, message, other

name = "proc"
dm_capable = True


async def run(bot, msg, conn):
    total_cpu = round(psutil.cpu_percent(), 1)
    vm_memory = psutil.virtual_memory()
    total_memory = round((vm_memory.total - vm_memory.available) / vm_memory.total, 1)

    process = psutil.Process(os.getpid())
    usage_cpu = round(process.cpu_percent(), 1)
    usage_memory = round(process.memory_percent(), 1)
    running_threads = process.num_threads()
    open_files = len(process.open_files())
    connections = len(process.connections())

    await message.send_message(msg, f"""Total CPU usage: {total_cpu}%
Total memory usage: {total_memory}%
Process CPU usage: {usage_cpu}%
Process memory usage: {usage_memory}%
Running threads: {running_threads}
Open files: {open_files}
Open sockets: {connections}""", title="Process")
