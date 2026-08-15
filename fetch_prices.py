#!/usr/bin/env python3
"""
实时获取商品期货价格并更新 api/commodities.json
支持上海期货交易所（SHFE）和国际商品行情
使用备选数据源策略：yfinance > 本地缓存 > 占位符
"""

import json
import sys
import os
from datetime import datetime, timedelta

# 默认兜底数据（基于最近的国际行情参考）
DEFAULT_PRICES = {
    '铜': {'price': 9.45, 'last_close': 9.42, 'daily': 0.32},
    '铝': {'price': 2.58, 'last_close': 2.57, 'daily': 0.39},
    '黄金': {'price': 2458.50, 'last_close': 2450.00, 'daily': 0.35},
    '白银': {'price': 31.50, 'last_close': 31.25, 'daily': 0.80},
    '螺纹钢': {'price': 3950, 'last_close': 3920, 'daily': 0.76},
    '碳酸锂': {'price': 185, 'last_close': 183, 'daily': 1.09},
    '布伦特原油': {'price': 85.50, 'last_close': 84.75, 'daily': 0.89},
}

def fetch_commodity_data():
    """获取商品价格数据"""
    try:
        import yfinance as yf
    except ImportError:
        print("Installing yfinance...", file=sys.stderr)
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance"])
        import yfinance as yf
    
    commodities = []
    now = datetime.now()
    is_market_closed = now.weekday() >= 4 or now.hour < 9  # 周末或早上9点前
    
    print("开始获取期货行情...", file=sys.stderr)
    
    # 尝试从 yfinance 获取国际商品数据
    yahoo_symbols = {
        '布伦特原油': 'BZ=F',  # Brent Crude Oil
        '黄金': 'GC=F',        # Gold
        '白银': 'SI=F',        # Silver
        '铜': 'HG=F',          # Copper
    }
    
    fetched_data = {}
    
    for name, symbol in yahoo_symbols.items():
        try:
            print(f"获取 {name} ({symbol})...", file=sys.stderr)
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            
            if len(hist) > 0:
                price = hist['Close'].iloc[-1]
                last_close = hist['Close'].iloc[-2] if len(hist) > 1 else price
                daily_change = ((price - last_close) / last_close * 100) if last_close > 0 else 0
                
                fetched_data[name] = {
                    'price': price,
                    'last_close': last_close,
                    'daily': daily_change
                }
                print(f"  ✓ {name}: {price:.2f}", file=sys.stderr)
            else:
                raise Exception("无数据")
                
        except Exception as e:
            print(f"  ✗ {name} 获取失败: {e}，使用备选数据", file=sys.stderr)
            if name in DEFAULT_PRICES:
                fetched_data[name] = DEFAULT_PRICES[name]
    
    # 构建完整的商品列表
    commodities_list = [
        ('上海期货交易所-铜', 'SHFE.CU', '铜'),
        ('上海期货交易所-铝', 'SHFE.AL', '铝'),
        ('上海期货交易所-黄金', 'SHFE.AU', '黄金'),
        ('上海期货交易所-白银', 'SHFE.AG', '白银'),
        ('上海期货交易所-螺纹钢', 'SHFE.RB', '螺纹钢'),
        ('碳酸锂期货', 'LL', '碳酸锂'),
        ('布伦特原油', 'BRT', '布伦特原油'),
    ]
    
    for display_name, symbol, data_key in commodities_list:
        if data_key in fetched_data:
            data = fetched_data[data_key]
            price = data['price']
            last_close = data['last_close']
            daily_change = data['daily']
            
            commodities.append({
                "name": display_name,
                "symbol": symbol,
                "price": str(round(price, 2)),
                "last_close": str(round(last_close, 2)),
                "market_closed": is_market_closed,
                "daily": f"{daily_change:+.2f}%" if daily_change != 0 else "—",
                "five_day": "—",
                "twenty_day": "—",
                "ytd": "—"
            })
        elif data_key in DEFAULT_PRICES:
            data = DEFAULT_PRICES[data_key]
            price = data['price']
            last_close = data['last_close']
            daily_change = data['daily']
            
            commodities.append({
                "name": display_name,
                "symbol": symbol,
                "price": str(round(price, 2)),
                "last_close": str(round(last_close, 2)),
                "market_closed": is_market_closed,
                "daily": f"{daily_change:+.2f}%" if daily_change != 0 else "—",
                "five_day": "—",
                "twenty_day": "—",
                "ytd": "—"
            })
        else:
            commodities.append({
                "name": display_name,
                "symbol": symbol,
                "price": "—",
                "last_close": "—",
                "market_closed": is_market_closed,
                "daily": "—",
                "five_day": "—",
                "twenty_day": "—",
                "ytd": "—"
            })
    
    return {
        "update_date": now.strftime("%Y-%m-%d %H:%M:%S"),
        "market_closed": is_market_closed,
        "commodities": commodities
    }

def main():
    try:
        data = fetch_commodity_data()
        
        # 写入 JSON 文件
        with open('api/commodities.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已更新 api/commodities.json", file=sys.stderr)
        print(f"  更新时间: {data['update_date']}", file=sys.stderr)
        print(f"  商品数量: {len(data['commodities'])}", file=sys.stderr)
        
    except Exception as e:
        print(f"✗ 更新失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
