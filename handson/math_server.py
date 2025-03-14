# math_server.py
from mcp.server.fastmcp import FastMCP

# サーバーの初期化（"Math"はサーバー名）
mcp = FastMCP("Math")


# ツールの定義: 2数の足し算
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# ツールの定義: 2数の掛け算
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


if __name__ == "__main__":
    # MCPサーバーを起動（標準入出力経由のトランスポートを使用）
    mcp.run(transport="stdio")
