
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("\n=== OMNITUTOR AI MCP TOOLS ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\n=== TEST 1: LEARN TOPIC ===")
            result = await session.call_tool(
                "learn_topic",
                {"topic": "Python variables"}
            )
            print(result.content)

            print("\n=== TEST 2: GENERATE QUIZ ===")
            result = await session.call_tool(
                "generate_quiz",
                {"topic": "Python"}
            )
            print(result.content)

            print("\n=== TEST 3: ANALYZE CODE ===")
            result = await session.call_tool(
                "analyze_code",
                {"code": "print('Hello')"}
            )
            print(result.content)

            print("\n=== TEST 4: CREATE STUDY PLAN ===")
            result = await session.call_tool(
                "create_study_plan",
                {"topic": "Python", "days": 5}
            )
            print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
