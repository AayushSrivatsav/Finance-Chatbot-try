from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from models.schemas import StockInfo, StockRecommendation
from services.stock_service import StockService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize stock service
stock_service = StockService()

@router.get("/info/{symbol}", response_model=StockInfo)
async def get_stock_info(symbol: str):
    """Get comprehensive stock information"""
    try:
        stock_info = await stock_service.get_stock_info(symbol)
        if not stock_info:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get stock info for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock information")

@router.get("/recommendation/{symbol}", response_model=StockRecommendation)
async def get_stock_recommendation(symbol: str):
    """Get AI-powered stock recommendation"""
    try:
        recommendation = await stock_service.get_stock_recommendation(symbol)
        if not recommendation:
            raise HTTPException(status_code=404, detail="Unable to generate recommendation")
        return recommendation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get recommendation for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendation")

@router.get("/market-overview")
async def get_market_overview():
    """Get market overview with major indices"""
    try:
        overview = await stock_service.get_market_overview()
        return overview
        
    except Exception as e:
        logger.error(f"Failed to get market overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch market overview")

@router.get("/search")
async def search_stocks(query: str = Query(..., min_length=1, description="Search query for stocks")):
    """Search for stocks by symbol or company name"""
    try:
        results = await stock_service.search_stocks(query)
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Failed to search stocks: {e}")
        raise HTTPException(status_code=500, detail="Failed to search stocks")

@router.get("/popular")
async def get_popular_stocks():
    """Get list of popular stocks"""
    try:
        popular_stocks = [
            {"symbol": "AAPL", "name": "Apple Inc."},
            {"symbol": "MSFT", "name": "Microsoft Corporation"},
            {"symbol": "GOOGL", "name": "Alphabet Inc."},
            {"symbol": "AMZN", "name": "Amazon.com Inc."},
            {"symbol": "TSLA", "name": "Tesla Inc."},
            {"symbol": "META", "name": "Meta Platforms Inc."},
            {"symbol": "NVDA", "name": "NVIDIA Corporation"},
            {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
            {"symbol": "JNJ", "name": "Johnson & Johnson"},
            {"symbol": "V", "name": "Visa Inc."}
        ]
        
        # Get current info for each stock
        stock_data = []
        for stock in popular_stocks:
            try:
                info = await stock_service.get_stock_info(stock["symbol"])
                if info:
                    stock_data.append(info)
            except Exception:
                # If we can't get info, still include the basic data
                stock_data.append(stock)
        
        return {"stocks": stock_data}
        
    except Exception as e:
        logger.error(f"Failed to get popular stocks: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular stocks")

@router.get("/watchlist")
async def get_watchlist():
    """Get user's watchlist (placeholder - would be user-specific in real app)"""
    try:
        # This would typically fetch from a database based on user ID
        watchlist_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        
        watchlist_data = []
        for symbol in watchlist_symbols:
            try:
                info = await stock_service.get_stock_info(symbol)
                if info:
                    watchlist_data.append(info)
            except Exception:
                continue
        
        return {"watchlist": watchlist_data}
        
    except Exception as e:
        logger.error(f"Failed to get watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch watchlist")

@router.get("/sectors")
async def get_sector_performance():
    """Get sector performance data"""
    try:
        # This would typically fetch real sector data
        # For now, return placeholder data
        sectors = [
            {"name": "Technology", "performance": 2.5, "change": 1.2},
            {"name": "Healthcare", "performance": -0.8, "change": -0.3},
            {"name": "Financial", "performance": 1.1, "change": 0.5},
            {"name": "Consumer Discretionary", "performance": 0.7, "change": 0.2},
            {"name": "Energy", "performance": -1.2, "change": -0.8},
            {"name": "Industrials", "performance": 0.3, "change": 0.1}
        ]
        
        return {"sectors": sectors}
        
    except Exception as e:
        logger.error(f"Failed to get sector performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sector performance") 