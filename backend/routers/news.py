from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from models.schemas import NewsArticle, NewsRequest
from services.news_scraper import NewsScraper

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize news scraper
news_scraper = NewsScraper()

@router.get("/latest", response_model=List[NewsArticle])
async def get_latest_news(
    query: Optional[str] = Query(None, description="Search query for news"),
    limit: int = Query(20, ge=1, le=50, description="Number of articles to return"),
    category: Optional[str] = Query(None, description="News category")
):
    """Get latest financial news"""
    try:
        articles = await news_scraper.get_latest_news(query, limit)
        return articles
        
    except Exception as e:
        logger.error(f"Failed to get latest news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest news")

@router.get("/stock/{symbol}", response_model=List[NewsArticle])
async def get_stock_news(
    symbol: str,
    limit: int = Query(10, ge=1, le=20, description="Number of articles to return")
):
    """Get news specific to a stock symbol"""
    try:
        articles = await news_scraper.get_stock_news(symbol, limit)
        return articles
        
    except Exception as e:
        logger.error(f"Failed to get stock news for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock news")

@router.get("/sources")
async def get_news_sources():
    """Get available news sources"""
    try:
        return {
            "sources": [
                "Reuters",
                "Bloomberg",
                "CNBC",
                "MarketWatch",
                "Yahoo Finance",
                "Seeking Alpha",
                "Investing.com",
                "Financial Times"
            ],
            "rss_feeds": [
                "https://feeds.reuters.com/reuters/businessNews",
                "https://feeds.bloomberg.com/markets/news.rss",
                "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                "https://www.marketwatch.com/rss/topstories",
                "https://feeds.finance.yahoo.com/rss/2.0/headline"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get news sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to get news sources")

@router.get("/categories")
async def get_news_categories():
    """Get available news categories"""
    try:
        return {
            "categories": [
                "markets",
                "stocks",
                "bonds",
                "commodities",
                "currencies",
                "cryptocurrency",
                "economy",
                "earnings",
                "mergers",
                "ipo"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get news categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get news categories")

@router.post("/search", response_model=List[NewsArticle])
async def search_news(request: NewsRequest):
    """Search for news articles"""
    try:
        articles = await news_scraper.get_latest_news(request.query, request.limit)
        return articles
        
    except Exception as e:
        logger.error(f"Failed to search news: {e}")
        raise HTTPException(status_code=500, detail="Failed to search news") 