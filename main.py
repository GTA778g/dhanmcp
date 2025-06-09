import httpx
from mcp.server.fastmcp import FastMCP

# MCP Server setup
mcp = FastMCP("Dhan Trade Analyzer")

# API config
DHAN_API_URL = "https://api.dhan.co/trades"
ACCESS_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUwMDUxNjQ1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjgyMDMwMyJ9.0lOJBcoiazZDRmSYgoo5NSQQxBUc_UQZvkCJilbeE1COM7tQSesq1DfrDpXvFlBoOsW63QtikWf5gmflG1b-6A"

@mcp.tool()
async def get_today_trades(format: str = "text") -> str:
    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(DHAN_API_URL, headers=headers)

    if response.status_code != 200:
        return f"❌ Error: {response.status_code}, {response.text}"

    trades = response.json()

    processed = [
        {
            "symbol": t["tradingSymbol"],
            "type": t["transactionType"],
            "quantity": t["tradedQuantity"],
            "time": t["exchangeTime"],
            "price": t["tradedPrice"]
        }
        for t in trades
    ]

    if format == "json":
        return str(processed)

    summary = "\n".join([
        f"{i+1}. {t['type']} {t['symbol']}, quantity: {t['quantity']}, price: ₹{t['price']}, time: {t['time']}"
        for i, t in enumerate(processed)
    ])
    return summary

# Run the server
if __name__ == "__main__":
    mcp.run()
