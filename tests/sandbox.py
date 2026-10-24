import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

def start():
    print("1")

    with asyncio.Runner() as runner:
        runner.run(main())

    print("2")

if (__name__ == "__main__"):
    start()