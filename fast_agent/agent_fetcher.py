import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application

fast = FastAgent("FastAgent Example")
@fast.agent(
    "url_fetcher",
    "Given a URL, provide a complete and comprehensive summary",
    servers=["fetch"], # Name of an MCP Server defined in fastagent.config.yaml
)
@fast.agent(
    "social_media",
    """
    Write a 280 character social media post for the given text. Your goal is to get people to share it. Your target audience is old people.
    """,
)

@fast.agent(
  "jira_fetcher",
  """
  Retrieve information about jira tickets"
  """,
  servers=["jira", "filesystem"],
)

@fast.agent(
    "audio_transcriber",
    """
    Transcribe audio from a given video file
    """,
    servers=["audio_tools", "filesystem"],
)

async def main():
    async with fast.run() as agent:
        await agent()
        await agent.prompt()

if __name__ == "__main__":
    asyncio.run(main())