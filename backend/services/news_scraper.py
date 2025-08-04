import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import feedparser
from bs4 import BeautifulSoup
import yfinance as yf
from newsapi import NewsApiClient
import re

from models.schemas import NewsArticle

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.news_api = NewsApiClient(api_key=self._get_news_api_key())
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Finance news sources
        self.finance_sources = [
            'reuters.com',
            'bloomberg.com',
            'cnbc.com',
            'marketwatch.com',
            'yahoo.com/finance',
            'seekingalpha.com',
            'investing.com',
            'financialtimes.com'
        ]
        
        # RSS feeds for finance news
        self.rss_feeds = [
            'https://feeds.reuters.com/reuters/businessNews',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
            'https://www.marketwatch.com/rss/topstories',
            'https://feeds.finance.yahoo.com/rss/2.0/headline'
        ]
    
    def _get_news_api_key(self) -> str:
        """Get News API key from environment"""
        import os
        return os.getenv("NEWS_API_KEY", "")
    
    async def initialize(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def close(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def get_latest_news(self, query: Optional[str] = None, limit: int = 20) -> List[NewsArticle]:
        """Get latest financial news from multiple sources"""
        try:
            articles = []
            
            # Get news from News API
            if self._get_news_api_key():
                api_articles = await self._get_news_api_articles(query, limit)
                articles.extend(api_articles)
            
            # Get news from RSS feeds
            rss_articles = await self._get_rss_articles(limit // 2)
            articles.extend(rss_articles)
            
            # Get news from web scraping
            scraped_articles = await self._scrape_finance_sites(limit // 4)
            articles.extend(scraped_articles)
            
            # Remove duplicates and sort by date
            unique_articles = self._deduplicate_articles(articles)
            unique_articles.sort(key=lambda x: x.published_at or datetime.min, reverse=True)
            
            return unique_articles[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get latest news: {e}")
            return []
    
    async def _get_news_api_articles(self, query: Optional[str], limit: int) -> List[NewsArticle]:
        """Get articles from News API"""
        try:
            if not self._get_news_api_key():
                return []
            
            # Search for finance-related news
            search_query = query or "finance OR stocks OR market OR economy"
            
            response = self.news_api.get_everything(
                q=search_query,
                language='en',
                sort_by='publishedAt',
                page_size=min(limit, 100)
            )
            
            articles = []
            for article in response.get('articles', []):
                try:
                    news_article = NewsArticle(
                        title=article.get('title', ''),
                        description=article.get('description', ''),
                        content=article.get('content', ''),
                        url=article.get('url', ''),
                        source=article.get('source', {}).get('name', 'Unknown'),
                        published_at=self._parse_date(article.get('publishedAt')),
                        sentiment=self._analyze_sentiment(article.get('title', '') + ' ' + (article.get('description') or '')),
                        relevance_score=self._calculate_relevance(article, query)
                    )
                    articles.append(news_article)
                except Exception as e:
                    logger.warning(f"Failed to parse News API article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to get News API articles: {e}")
            return []
    
    async def _get_rss_articles(self, limit: int) -> List[NewsArticle]:
        """Get articles from RSS feeds"""
        try:
            articles = []
            
            for feed_url in self.rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:limit // len(self.rss_feeds)]:
                        try:
                            news_article = NewsArticle(
                                title=entry.get('title', ''),
                                description=entry.get('summary', ''),
                                content=entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '',
                                url=entry.get('link', ''),
                                source=feed.feed.get('title', 'RSS Feed'),
                                published_at=self._parse_date(entry.get('published')),
                                sentiment=self._analyze_sentiment(entry.get('title', '') + ' ' + (entry.get('summary') or '')),
                                relevance_score=0.7
                            )
                            articles.append(news_article)
                        except Exception as e:
                            logger.warning(f"Failed to parse RSS entry: {e}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Failed to parse RSS feed {feed_url}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to get RSS articles: {e}")
            return []
    
    async def _scrape_finance_sites(self, limit: int) -> List[NewsArticle]:
        """Scrape articles from finance websites"""
        try:
            articles = []
            
            # Scrape from Reuters
            reuters_articles = await self._scrape_reuters(limit // 3)
            articles.extend(reuters_articles)
            
            # Scrape from MarketWatch
            marketwatch_articles = await self._scrape_marketwatch(limit // 3)
            articles.extend(marketwatch_articles)
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to scrape finance sites: {e}")
            return []
    
    async def _scrape_reuters(self, limit: int) -> List[NewsArticle]:
        """Scrape articles from Reuters"""
        try:
            if not self.session:
                return []
            
            url = "https://www.reuters.com/markets/finance"
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    articles = []
                    article_elements = soup.find_all('article')[:limit]
                    
                    for element in article_elements:
                        try:
                            title_elem = element.find('h3') or element.find('h2')
                            link_elem = element.find('a')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = "https://www.reuters.com" + link_elem.get('href', '')
                                
                                news_article = NewsArticle(
                                    title=title,
                                    description="",
                                    content="",
                                    url=url,
                                    source="Reuters",
                                    published_at=datetime.now(),
                                    sentiment=self._analyze_sentiment(title),
                                    relevance_score=0.8
                                )
                                articles.append(news_article)
                        except Exception as e:
                            logger.warning(f"Failed to parse Reuters article: {e}")
                            continue
                    
                    return articles
                else:
                    return []
                    
        except Exception as e:
            logger.error(f"Failed to scrape Reuters: {e}")
            return []
    
    async def _scrape_marketwatch(self, limit: int) -> List[NewsArticle]:
        """Scrape articles from MarketWatch"""
        try:
            if not self.session:
                return []
            
            url = "https://www.marketwatch.com/latest-news"
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    articles = []
                    article_elements = soup.find_all('div', class_='article__content')[:limit]
                    
                    for element in article_elements:
                        try:
                            title_elem = element.find('a', class_='link')
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                url = "https://www.marketwatch.com" + title_elem.get('href', '')
                                
                                news_article = NewsArticle(
                                    title=title,
                                    description="",
                                    content="",
                                    url=url,
                                    source="MarketWatch",
                                    published_at=datetime.now(),
                                    sentiment=self._analyze_sentiment(title),
                                    relevance_score=0.8
                                )
                                articles.append(news_article)
                        except Exception as e:
                            logger.warning(f"Failed to parse MarketWatch article: {e}")
                            continue
                    
                    return articles
                else:
                    return []
                    
        except Exception as e:
            logger.error(f"Failed to scrape MarketWatch: {e}")
            return []
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        try:
            # Try different date formats
            formats = [
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%a, %d %b %Y %H:%M:%S %Z",
                "%a, %d %b %Y %H:%M:%S %z"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        positive_words = ['positive', 'gain', 'rise', 'up', 'bullish', 'growth', 'profit', 'success']
        negative_words = ['negative', 'loss', 'fall', 'down', 'bearish', 'decline', 'loss', 'failure']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_relevance(self, article: Dict[str, Any], query: Optional[str]) -> float:
        """Calculate relevance score for an article"""
        if not query:
            return 0.7
        
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        query_terms = query.lower().split()
        
        relevance_score = 0.0
        for term in query_terms:
            if term in title:
                relevance_score += 0.3
            if term in description:
                relevance_score += 0.2
        
        return min(relevance_score, 1.0)
    
    def _deduplicate_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            # Normalize title for comparison
            normalized_title = re.sub(r'[^\w\s]', '', article.title.lower())
            
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_articles.append(article)
        
        return unique_articles
    
    async def get_stock_news(self, symbol: str, limit: int = 10) -> List[NewsArticle]:
        """Get news specific to a stock symbol"""
        try:
            # Get news from News API
            if self._get_news_api_key():
                response = self.news_api.get_everything(
                    q=f"{symbol} stock",
                    language='en',
                    sort_by='publishedAt',
                    page_size=limit
                )
                
                articles = []
                for article in response.get('articles', []):
                    try:
                        news_article = NewsArticle(
                            title=article.get('title', ''),
                            description=article.get('description', ''),
                            content=article.get('content', ''),
                            url=article.get('url', ''),
                            source=article.get('source', {}).get('name', 'Unknown'),
                            published_at=self._parse_date(article.get('publishedAt')),
                            sentiment=self._analyze_sentiment(article.get('title', '') + ' ' + (article.get('description') or '')),
                            relevance_score=0.9
                        )
                        articles.append(news_article)
                    except Exception as e:
                        logger.warning(f"Failed to parse stock news article: {e}")
                        continue
                
                return articles
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get stock news: {e}")
            return [] 