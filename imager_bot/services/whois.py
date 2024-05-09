import asyncio
from asyncio import StreamReader
from asyncio.subprocess import Process

from loguru import logger


async def _write_output(stdout: StreamReader, buf: list):
    while line := await stdout.readline():
        buf.append(line.rstrip().decode())


async def get_whois_text(domain: str):
    program = ['whois', domain]
    logger.debug(f"Get request to whois, domain:{domain}")
    process: Process = await asyncio.create_subprocess_exec(*program, stdout=asyncio.subprocess.PIPE)
    buf: list[str] = []
    stdout_task = asyncio.create_task(_write_output(process.stdout, buf))
    return_code, _ = await asyncio.gather(process.wait(), stdout_task)
    return "\n".join(buf)
