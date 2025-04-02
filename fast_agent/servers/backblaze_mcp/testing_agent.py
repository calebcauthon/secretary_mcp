import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Agent for testing the backblaze mcp")
@fast.agent(
    "Backblaze Agent",
    "You will be an interface to the Backblaze Cloud",
    servers=["backblaze", "filesystem"],
)

async def main():
    async with fast.run() as agent:
        await agent.send("I want to verify my authorization works. List all buckets in a nice markdown table.")
        await agent.prompt()

if __name__ == "__main__":
    print("Starting agent...")
    asyncio.run(main())
