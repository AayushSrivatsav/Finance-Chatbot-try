import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass

from models.schemas import StockInfo, StockRecommendation
from services.news_scraper import NewsScraper

logger = logging.getLogger(__name__)

@dataclass
class TechnicalIndicators:
    rsi: float
    macd: float
    sma_20: float
    sma_50: float
    bollinger_upper: float
    bollinger_lower: float
    volume_avg: float

class StockService:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    async def get_stock_info(self, symbol: str) -> Optional[StockInfo]:
        """Get comprehensive stock information"""
        try:
            # Check cache first
            cache_key = f"stock_info_{symbol}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_duration:
                    return cached_data
            
            # Get stock data from yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price data
            hist = ticker.history(period="1d")
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close else 0
            
            stock_info = StockInfo(
                symbol=symbol.upper(),
                name=info.get('longName', symbol.upper()),
                price=current_price,
                change=change,
                change_percent=change_percent,
                market_cap=info.get('marketCap'),
                volume=info.get('volume'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
            )
            
            # Cache the result
            self.cache[cache_key] = (stock_info, datetime.now())
            
            return stock_info
            
        except Exception as e:
            logger.error(f"Failed to get stock info for {symbol}: {e}")
            return None
    
    async def get_stock_recommendation(self, symbol: str) -> Optional[StockRecommendation]:
        """Generate AI-powered stock recommendation"""
        try:
            # Get stock data
            ticker = yf.Ticker(symbol)
            
            # Get historical data for analysis
            hist = ticker.history(period="6mo")
            if hist.empty:
                return None
            
            # Calculate technical indicators
            indicators = self._calculate_technical_indicators(hist)
            
            # Get news sentiment
            news_articles = await self.news_scraper.get_stock_news(symbol, limit=10)
            news_sentiment = self._analyze_news_sentiment(news_articles)
            
            # Generate recommendation based on technical and fundamental analysis
            recommendation, confidence, reasoning = self._generate_recommendation(
                hist, indicators, news_sentiment, ticker.info
            )
            
            # Calculate price target
            price_target = self._calculate_price_target(hist, indicators)
            
            # Determine risk level
            risk_level = self._determine_risk_level(hist, indicators)
            
            return StockRecommendation(
                symbol=symbol.upper(),
                recommendation=recommendation,
                confidence=confidence,
                reasoning=reasoning,
                price_target=price_target,
                risk_level=risk_level,
                news_sentiment=news_sentiment
            )
            
        except Exception as e:
            logger.error(f"Failed to generate recommendation for {symbol}: {e}")
            return None
    
    def _calculate_technical_indicators(self, hist: pd.DataFrame) -> TechnicalIndicators:
        """Calculate technical indicators for stock analysis"""
        try:
            # RSI (Relative Strength Index)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = hist['Close'].ewm(span=12).mean()
            exp2 = hist['Close'].ewm(span=26).mean()
            macd = exp1 - exp2
            
            # Simple Moving Averages
            sma_20 = hist['Close'].rolling(window=20).mean()
            sma_50 = hist['Close'].rolling(window=50).mean()
            
            # Bollinger Bands
            sma_20_bb = hist['Close'].rolling(window=20).mean()
            std_20 = hist['Close'].rolling(window=20).std()
            bollinger_upper = sma_20_bb + (std_20 * 2)
            bollinger_lower = sma_20_bb - (std_20 * 2)
            
            # Volume average
            volume_avg = hist['Volume'].rolling(window=20).mean()
            
            return TechnicalIndicators(
                rsi=rsi.iloc[-1],
                macd=macd.iloc[-1],
                sma_20=sma_20.iloc[-1],
                sma_50=sma_50.iloc[-1],
                bollinger_upper=bollinger_upper.iloc[-1],
                bollinger_lower=bollinger_lower.iloc[-1],
                volume_avg=volume_avg.iloc[-1]
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate technical indicators: {e}")
            return None
    
    def _analyze_news_sentiment(self, articles: List) -> str:
        """Analyze sentiment from news articles"""
        if not articles:
            return "neutral"
        
        positive_count = sum(1 for article in articles if article.sentiment == "positive")
        negative_count = sum(1 for article in articles if article.sentiment == "negative")
        total_count = len(articles)
        
        if total_count == 0:
            return "neutral"
        
        positive_ratio = positive_count / total_count
        negative_ratio = negative_count / total_count
        
        if positive_ratio > 0.6:
            return "positive"
        elif negative_ratio > 0.6:
            return "negative"
        else:
            return "neutral"
    
    def _generate_recommendation(self, hist: pd.DataFrame, indicators: TechnicalIndicators, 
                                news_sentiment: str, info: Dict[str, Any]) -> tuple:
        """Generate stock recommendation based on analysis"""
        try:
            current_price = hist['Close'].iloc[-1]
            score = 0
            reasoning_points = []
            
            # Technical analysis (40% weight)
            if indicators:
                # RSI analysis
                if indicators.rsi < 30:
                    score += 20
                    reasoning_points.append("RSI indicates oversold conditions")
                elif indicators.rsi > 70:
                    score -= 20
                    reasoning_points.append("RSI indicates overbought conditions")
                
                # Moving average analysis
                if current_price > indicators.sma_20 > indicators.sma_50:
                    score += 15
                    reasoning_points.append("Price above both 20-day and 50-day moving averages")
                elif current_price < indicators.sma_20 < indicators.sma_50:
                    score -= 15
                    reasoning_points.append("Price below both 20-day and 50-day moving averages")
                
                # MACD analysis
                if indicators.macd > 0:
                    score += 5
                    reasoning_points.append("MACD is positive")
                else:
                    score -= 5
                    reasoning_points.append("MACD is negative")
            
            # News sentiment analysis (30% weight)
            if news_sentiment == "positive":
                score += 15
                reasoning_points.append("Recent news sentiment is positive")
            elif news_sentiment == "negative":
                score -= 15
                reasoning_points.append("Recent news sentiment is negative")
            
            # Fundamental analysis (30% weight)
            pe_ratio = info.get('trailingPE')
            if pe_ratio and pe_ratio < 15:
                score += 10
                reasoning_points.append("P/E ratio indicates undervaluation")
            elif pe_ratio and pe_ratio > 25:
                score -= 10
                reasoning_points.append("P/E ratio indicates overvaluation")
            
            # Determine recommendation
            if score >= 20:
                recommendation = "buy"
                confidence = min(0.9, 0.6 + (score / 100))
            elif score <= -20:
                recommendation = "sell"
                confidence = min(0.9, 0.6 + (abs(score) / 100))
            else:
                recommendation = "hold"
                confidence = 0.7
            
            reasoning = ". ".join(reasoning_points) if reasoning_points else "Insufficient data for strong recommendation"
            
            return recommendation, confidence, reasoning
            
        except Exception as e:
            logger.error(f"Failed to generate recommendation: {e}")
            return "hold", 0.5, "Unable to generate recommendation due to insufficient data"
    
    def _calculate_price_target(self, hist: pd.DataFrame, indicators: TechnicalIndicators) -> Optional[float]:
        """Calculate price target based on technical analysis"""
        try:
            if not indicators:
                return None
            
            current_price = hist['Close'].iloc[-1]
            
            # Simple price target based on Bollinger Bands
            if current_price < indicators.bollinger_lower:
                # Stock is oversold, target upper Bollinger Band
                target = indicators.bollinger_upper
            elif current_price > indicators.bollinger_upper:
                # Stock is overbought, target lower Bollinger Band
                target = indicators.bollinger_lower
            else:
                # Stock is in range, target middle of Bollinger Bands
                target = (indicators.bollinger_upper + indicators.bollinger_lower) / 2
            
            return round(target, 2)
            
        except Exception as e:
            logger.error(f"Failed to calculate price target: {e}")
            return None
    
    def _determine_risk_level(self, hist: pd.DataFrame, indicators: TechnicalIndicators) -> str:
        """Determine risk level based on volatility and technical indicators"""
        try:
            # Calculate volatility
            returns = hist['Close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            if volatility > 0.4:
                return "high"
            elif volatility > 0.2:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            logger.error(f"Failed to determine risk level: {e}")
            return "medium"
    
    async def get_market_overview(self) -> Dict[str, Any]:
        """Get market overview with major indices"""
        try:
            indices = ['^GSPC', '^DJI', '^IXIC', '^VIX']  # S&P 500, Dow Jones, NASDAQ, VIX
            overview = {}
            
            for index in indices:
                ticker = yf.Ticker(index)
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = hist['Open'].iloc[-1]
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    overview[index] = {
                        "price": current_price,
                        "change": change,
                        "change_percent": change_percent
                    }
            
            return overview
            
        except Exception as e:
            logger.error(f"Failed to get market overview: {e}")
            return {}
    
    async def search_stocks(self, query: str) -> List[Dict[str, Any]]:
        """Search for stocks based on company name or symbol"""
        try:
            # This is a simplified search - in a real implementation, you'd use a proper stock database
            # For now, we'll return some common stocks that match the query
            common_stocks = [
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
            
            query_lower = query.lower()
            results = []
            
            for stock in common_stocks:
                if (query_lower in stock["symbol"].lower() or 
                    query_lower in stock["name"].lower()):
                    results.append(stock)
            
            return results[:10]  # Limit to 10 results
            
        except Exception as e:
            logger.error(f"Failed to search stocks: {e}")
            return [] 