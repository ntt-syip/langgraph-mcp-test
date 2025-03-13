# agent_client.py (クライアントエージェント側)
import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# LLMモデルの用意（OpenAIのGPT-4を使用。APIキーは環境変数で設定済み）
model = ChatOpenAI(model="gpt-4o")  # 必要に応じて "gpt-3.5-turbo" 等にも変更可

# MCPサーバー(math_server.py)を標準入出力経由で起動する設定
server_params = StdioServerParameters(
    command="python",
    args=["./math_server.py"],
)


# MCPサーバーに接続してセッション開始、エージェントを生成
async def main():
    # サーバーとの接続を確立（サブプロセスとしてmath_server.pyを起動）
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # セッション初期化
            await session.initialize()
            # MCPサーバー上の全ツールを取得
            tools = await load_mcp_tools(session)
            # LLMモデルと取得したツールでエージェントを作成
            agent = create_react_agent(model, tools)
            # （ここまででエージェントの準備が完了）
            # エージェントに質問を送り、ツールを使った回答を取得
            query = "What's (3 + 5) x 12?"  # 質問内容の例
            result = await agent.ainvoke({"messages": query})
            print("Agent's answer:", result)


# スクリプトを実行
asyncio.run(main())
