import asyncio

from cli.episode import afetch, aprune


async def amain():
    await afetch()
    # await aprune()
    print("terminated!")


if __name__ == "__main__":
    asyncio.run(amain())
