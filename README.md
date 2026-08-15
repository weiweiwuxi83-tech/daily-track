# Daily Track - 商品价格看板

这是一个简单的静态数据看板，用于追踪商品价格和涨跌幅。

## 项目结构

- `index.html` - 看板网页（在浏览器中打开查看）
- `data.json` - 数据文件（每天更新这个文件）
- `style.css` - 样式文件（美化界面）

## 如何使用

### 1. 查看看板
打开 `index.html` 文件即可看到看板。也可以在网页上查看（启用 GitHub Pages）。

### 2. 更新数据
编辑 `data.json` 文件，修改商品数据和日期。

### 3. 查看更新
刷新浏览器，看板会显示最新数据。

### 4. 接入真实行情 API
在 `index.html` 中将 `LIVE_API_URL` 改成真实接口地址即可。浏览器会优先尝试调用该接口，失败时自动回退到本地 `data.json`。

示例接口返回格式：

```json
{
  "update_date": "2026-08-15",
  "market_closed": true,
  "commodities": [
    {
      "name": "上海期货交易所-铜",
      "symbol": "SHFE.CU",
      "price": "74250",
      "last_close": "73880",
      "market_closed": true,
      "daily": "+0.8%",
      "five_day": "+2.9%",
      "twenty_day": "+6.1%",
      "ytd": "+15%"
    }
  ]
}
```

注意：GitHub Pages 是静态站点，如果真实行情 API 不支持 CORS，需要在后端增加代理接口，前端再请求代理地址。

## 在线查看
启用 GitHub Pages 后，可以通过以下链接在线查看：
`https://weiweiwuxi83-tech.github.io/daily-track/`

## 配置 GitHub Pages
1. 进入仓库 Settings
2. 左侧选择 "Pages"
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "main"，文件夹选择 "/(root)"
5. Save

几分钟后就能在上面的链接访问你的看板！
