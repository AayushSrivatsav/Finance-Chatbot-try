import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.base_url = "http://localhost:3001"  # Default MCP server URL
        self.session = None
        self.available_tools = []
        
    async def initialize(self):
        """Initialize MCP server connection"""
        try:
            self.session = aiohttp.ClientSession()
            
            # Test connection
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    logger.info("MCP server connection established")
                    await self._discover_tools()
                else:
                    logger.warning("MCP server not available")
                    
        except Exception as e:
            logger.warning(f"Failed to connect to MCP server: {e}")
    
    async def close(self):
        """Close MCP server connection"""
        if self.session:
            await self.session.close()
    
    async def _discover_tools(self):
        """Discover available tools from MCP server"""
        try:
            async with self.session.get(f"{self.base_url}/tools") as response:
                if response.status == 200:
                    tools = await response.json()
                    self.available_tools = tools.get("tools", [])
                    logger.info(f"Discovered {len(self.available_tools)} MCP tools")
                    
        except Exception as e:
            logger.error(f"Failed to discover MCP tools: {e}")
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool through MCP server"""
        try:
            if not self.session:
                return {"error": "MCP server not connected"}
            
            payload = {
                "tool": tool_name,
                "parameters": parameters,
                "timestamp": datetime.now().isoformat()
            }
            
            async with self.session.post(f"{self.base_url}/execute", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return {"error": f"Tool execution failed: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Failed to execute MCP tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get enhanced market data through MCP tools"""
        try:
            # Try to get data from MCP server if available
            if "market_data" in [tool.get("name") for tool in self.available_tools]:
                result = await self.execute_tool("market_data", {"symbol": symbol})
                if "error" not in result:
                    return result
            
            # Fallback to basic data
            return {"symbol": symbol, "source": "fallback"}
            
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {e}")
            return {"error": str(e)}
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using MCP tools"""
        try:
            if "sentiment_analysis" in [tool.get("name") for tool in self.available_tools]:
                result = await self.execute_tool("sentiment_analysis", {"text": text})
                if "error" not in result:
                    return result
            
            # Fallback to basic sentiment analysis
            return {"sentiment": "neutral", "confidence": 0.5, "source": "fallback"}
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {"error": str(e)}
    
    async def get_news_analysis(self, query: str) -> Dict[str, Any]:
        """Get enhanced news analysis through MCP tools"""
        try:
            if "news_analysis" in [tool.get("name") for tool in self.available_tools]:
                result = await self.execute_tool("news_analysis", {"query": query})
                if "error" not in result:
                    return result
            
            # Fallback
            return {"query": query, "analysis": "Basic analysis", "source": "fallback"}
            
        except Exception as e:
            logger.error(f"Failed to get news analysis: {e}")
            return {"error": str(e)}
    
    async def get_technical_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get technical analysis through MCP tools"""
        try:
            if "technical_analysis" in [tool.get("name") for tool in self.available_tools]:
                result = await self.execute_tool("technical_analysis", {"symbol": symbol})
                if "error" not in result:
                    return result
            
            # Fallback
            return {"symbol": symbol, "analysis": "Basic technical analysis", "source": "fallback"}
            
        except Exception as e:
            logger.error(f"Failed to get technical analysis: {e}")
            return {"error": str(e)}
    
    async def get_risk_assessment(self, symbol: str) -> Dict[str, Any]:
        """Get risk assessment through MCP tools"""
        try:
            if "risk_assessment" in [tool.get("name") for tool in self.available_tools]:
                result = await self.execute_tool("risk_assessment", {"symbol": symbol})
                if "error" not in result:
                    return result
            
            # Fallback
            return {"symbol": symbol, "risk_level": "medium", "source": "fallback"}
            
        except Exception as e:
            logger.error(f"Failed to get risk assessment: {e}")
            return {"error": str(e)}
    
    def get_available_tools(self) -> List[str]:
        """Get list of available MCP tools"""
        return [tool.get("name") for tool in self.available_tools]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check MCP server health"""
        try:
            if not self.session:
                return {"status": "disconnected", "error": "No session"}
            
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    return {"status": "healthy", "tools": len(self.available_tools)}
                else:
                    return {"status": "unhealthy", "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"status": "error", "error": str(e)} 