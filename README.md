# Daily Track - 商品价格看板

📊 实时商品期货价格看板（布伦特原油、铜、铝、黄金、白银、螺纹钢、碳酸锂）

## ✨ 核心特性

- 🔄 **自动定时更新** - 通过 GitHub Actions 每日4次自动获取最新价格
- 📡 **实时数据源** - 使用 Yahoo Finance 获取国际商品期货价格
- 💾 **双重缓存机制** - 优先加载实时数据，失败时自动回退到本地数据
- 🔌 **API-ready** - 架构支持灵活接入不同数据源
- 📱 **响应式设计** - 支持桌面和移动设备查看

## 📋 项目结构

```
├── index.html                    # 看板网页（主入口）
├── style.css                     # 样式文件
├── data.json                     # 本地备用数据
├── api/commodities.json          # 自动更新的实时数据源
├── fetch_prices.py              # 数据爬取脚本
├── .github/workflows/           # GitHub Actions 自动化配置
│   └── update-prices.yml        # 定时更新工作流
└── README.md                     # 本说明
```

## 🚀 快速开始

### 本地查看
```bash
# 启动本地 HTTP 服务器
python3 -m http.server 8000

# 打开浏览器访问
# http://localhost:8000
```

### 在线查看
仓库已启用 GitHub Pages，访问：[daily-track](https://github.com/weiweiwuxi83-tech/daily-track/wiki)

## 📊 数据源

### 实时数据流
1. **优先级 1** - Yahoo Finance API（通过 `fetch_prices.py` 脚本获取）
   - 布伦特原油、黄金、白银、铜等国际商品期货
   
2. **优先级 2** - 本地同源 API（`api/commodities.json`）
   - 由 GitHub Actions 自动更新
   
3. **优先级 3** - 备用本地数据（`data.json`）
   - 当网络不可用时作为最后兜底

4. **优先级 4** - 内置默认数据
   - 页面中嵌入的最近参考价格

### 自动更新配置
GitHub Actions 工作流每天在以下时间自动运行（UTC+0）：
- 00:00 (UTC) → 08:00 (北京时间)
- 02:00 (UTC) → 10:00 (北京时间)
- 06:00 (UTC) → 14:00 (北京时间)
- 08:00 (UTC) → 16:00 (北京时间)

## 🛠️ 手动更新数据

### 方式一：本地运行脚本
```bash
python3 fetch_prices.py
```

### 方式二：GitHub Actions 手动触发
1. 进入仓库 Actions 页面
2. 选择 "🔄 定时更新商品价格" 工作流
3. 点击 "Run workflow"

## 📝 数据格式

```json
{
  "update_date": "2026-08-15 14:03:51",
  "market_closed": true,
  "commodities": [
    {
      "name": "布伦特原油",
      "symbol": "BRT",
      "price": "88.52",
      "last_close": "87.07",
      "market_closed": true,
      "daily": "+1.67%",
      "five_day": "—",
      "twenty_day": "—",
      "ytd": "—"
    }
  ]
}
```

### 字段说明
- `name` - 商品中文名称
- `symbol` - 交易代码
- `price` - 当前价格（市场休市时为上一交易日收盘价）
- `last_close` - 上一交易日收盘价
- `market_closed` - 市场是否休市
- `daily` - 日涨跌幅（百分比）
- `five_day`, `twenty_day`, `ytd` - 其他周期涨跌幅

## 🔧 定制说明

### 修改监控的商品
编辑 `fetch_prices.py`，修改 `yahoo_symbols` 字典：
```python
yahoo_symbols = {
    '布伦特原油': 'BZ=F',  # Brent Crude Oil
    '黄金': 'GC=F',        # Gold
    # ... 添加更多商品
}
```

### 修改自动更新频率
编辑 `.github/workflows/update-prices.yml`，修改 `cron` 表达式。
参考：[Cron 表达式文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)

### 切换数据源
修改 `index.html` 中的 `LIVE_API_URL`：
```javascript
const LIVE_API_URL = 'your-api-endpoint-here';
```

## 📝 许可证
MIT

## 🙌 贡献
欢迎提交 Issue 和 Pull Request！
`https://weiweiwuxi83-tech.github.io/daily-track/`

## 配置 GitHub Pages
1. 进入仓库 Settings
2. 左侧选择 "Pages"
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "main"，文件夹选择 "/(root)"
5. Save

几分钟后就能在上面的链接访问你的看板！
