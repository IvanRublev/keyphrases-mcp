import asyncio
from agents import Agent, Runner
import click
from openai.types.responses import ResponseTextDeltaEvent
from agents.mcp import MCPServerStdio
from collections import deque


# Set up and create the agent
async def build_agent(allowed_dir: str):
    # Keyphrases MCP Server. Pass the environment configuration for the MCP Server in the JSON
    server = MCPServerStdio(
        params={
            "command": "uv",
            "args": [
                "--directory",
                "../src/",  # change with the path to the MCP server
                "run",
                "main.py",
                "--allowed-dir",
                allowed_dir,
            ],
        },
        client_session_timeout_seconds=180,  # 3 minutes timeout
    )

    await server.connect()

    # Create and return the agent
    agent = Agent(
        name="Keyphrases Assistant",
        instructions=(
            "You are a helpful assistant capable of extracting keyphrases from the given text files."
            "Use the mcp server tool to extract keyphrases passing up to 6000 characters at once."
            "Store every answer in the Keyphrases Stream app:logger"
        ),
        mcp_servers=[server],
    )

    return agent


# CLI interaction
async def cli(agent, max_history=30):
    print(
        "🔧 Keyphrases Assistant CLI — Ask me to extract number of keyphrases "
        "from the text file at a given path (type 'exit' to quit):\n"
    )
    conversation_history = deque(maxlen=max_history)

    while True:
        q = input("❓> ")
        if q.strip().lower() in {"exit", "quit"}:
            break

        if len(q.strip()) > 0:
            # Format the context into a single string
            history = ""
            for turn in conversation_history:
                prefix = "User" if turn["role"] == "user" else "Assistant"
                history += f"{prefix}: {turn['content']}\n"

            context = f"Conversation history:/n{history.strip()} /n New question:/n{q.strip()}"
            result = Runner.run_streamed(agent, context)

            response_text = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
                    response_text += event.data.delta
            print("\n")

            # Add the user's message and the assistant's reply in history
            conversation_history.append({"role": "user", "content": q})
            conversation_history.append({"role": "assistant", "content": response_text})


# Main entry point
@click.command()
@click.option(
    "--allowed-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Allowed directory to read files from.",
)
def main(allowed_dir: str):
    asyncio.run(_main(allowed_dir))


async def _main(allowed_dir: str):
    agent = await build_agent(allowed_dir)
    await cli(agent)


if __name__ == "__main__":
    main()
