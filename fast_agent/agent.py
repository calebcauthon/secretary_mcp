import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("FastAgent Example")

@fast.agent(
    "secretary",
    """
    You are a helpful AI Agent. Your name is Secretary Poop.

    You will be given access to specific files and directories.
    You should assume that those are the directories you will be working in.
    Always check to see what directories you have access to before proceeding with a task.
    Refresh your knowledge with the list of files and directories you have access to whenever necessary.

    WHEN COPYING A FILE, DO NOT READ IT. JUST COPY IT USING FILESYSTEM COMMAND.


    "DAILY JOURNAL"
    In the Journal directory, you will find a directory for each day.
    Within each day's directory, you will find a subdirectory called "sources".

    METATASKS:
    ** METATASK: "TAKE CARE OF THE LATEST RECORDINGS"
    If a user asks you to "TAKE CARE OF THE LATEST RECORDINGS", you should:
    1) Check the recordings directory for any .mov files
    2) Transcribe each file
    3) Move the transcription file to today's Journal directory, subdirectory "sources". Create the directory if necessary.
    4) Move the input file to today's Journal directory, subdirectory "sources"
    5) Create a summary of the transcription and save it to today's Journal directory, subdirectory "sources", with ".rewrite" in the name
 
    """,
    servers=["audio_tools", "filesystem"],
)

async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent()


if __name__ == "__main__":
    asyncio.run(main())
