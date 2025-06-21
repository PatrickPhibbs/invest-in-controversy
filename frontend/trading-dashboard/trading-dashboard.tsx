"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Activity,
  Shield,
  BarChart3,
  Newspaper,
  Target,
  Zap,
} from "lucide-react"

export default function TradingDashboard() {
  // Mock data
  const portfolioValue = 125847.32
  const dailyPnL = 2847.21
  const dailyPnLPercent = 2.31

  const positions = [
    { symbol: "AAPL", shares: 150, value: 28500, pnl: 1250, pnlPercent: 4.58 },
    { symbol: "TSLA", shares: 75, value: 18750, pnl: -890, pnlPercent: -4.53 },
    { symbol: "NVDA", shares: 50, value: 22500, pnl: 2100, pnlPercent: 10.29 },
    { symbol: "META", shares: 100, value: 31200, pnl: 450, pnlPercent: 1.46 },
  ]

  const newsActivity = [
    {
      time: "09:34 AM",
      company: "Tesla Inc",
      controversy: "Regulatory Investigation",
      action: "SELL",
      reasoning: "SEC investigation announced - high volatility expected",
      sentiment: -0.78,
      source: "Reuters",
    },
    {
      time: "09:28 AM",
      company: "Apple Inc",
      controversy: "Product Recall",
      action: "BUY",
      reasoning: "Minor recall, market overreaction detected",
      sentiment: -0.34,
      source: "Bloomberg",
    },
    {
      time: "09:15 AM",
      company: "NVIDIA Corp",
      controversy: "Earnings Beat",
      action: "BUY",
      reasoning: "Strong earnings, positive sentiment surge",
      sentiment: 0.89,
      source: "CNBC",
    },
  ]

  const riskMetrics = [
    { label: "Portfolio Beta", value: "1.23", status: "moderate" },
    { label: "Max Drawdown", value: "8.4%", status: "good" },
    { label: "Sharpe Ratio", value: "1.67", status: "good" },
    { label: "VaR (95%)", value: "$4,250", status: "moderate" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black p-4">
      <div className="mx-auto max-w-7xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-yellow-400">News Trading Algorithm</h1>
            <p className="text-lg text-yellow-400/80 mt-1">Real-time controversy detection & automated trading</p>
          </div>
          <div className="flex items-center space-x-4">
            <Badge variant="outline" className="bg-green-500 text-white border-green-600">
              <CheckCircle className="w-4 h-4 mr-1" />
              Algorithm Active
            </Badge>
            <Badge variant="outline" className="bg-black text-yellow-400 border-black">
              <Activity className="w-4 h-4 mr-1" />
              Live Data
            </Badge>
          </div>
        </div>

        {/* Top Row - Performance Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-yellow-400 text-black border-black">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <DollarSign className="w-4 h-4 mr-2" />
                Portfolio Value
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${portfolioValue.toLocaleString()}</div>
              <div className={`text-sm flex items-center mt-1 ${dailyPnL >= 0 ? "text-green-400" : "text-red-400"}`}>
                {dailyPnL >= 0 ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}$
                {Math.abs(dailyPnL).toLocaleString()} ({dailyPnLPercent >= 0 ? "+" : ""}
                {dailyPnLPercent}%)
              </div>
            </CardContent>
          </Card>

          <Card className="bg-yellow-400 text-black border-black">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Target className="w-4 h-4 mr-2" />
                Success Rate
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">73.2%</div>
              <div className="text-sm text-green-400 mt-1">+2.1% vs last week</div>
            </CardContent>
          </Card>

          <Card className="bg-yellow-400 text-black border-black">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Newspaper className="w-4 h-4 mr-2" />
                News Signals
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">47</div>
              <div className="text-sm text-black/80 mt-1">Today's triggers</div>
            </CardContent>
          </Card>

          <Card className="bg-yellow-400 text-black border-black">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                Avg Response
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1.2s</div>
              <div className="text-sm text-green-400 mt-1">News to trade</div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - News Activity Feed */}
          <div className="lg:col-span-2 space-y-4">
            <Card className="bg-yellow-400 text-black border-black">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="w-5 h-5 mr-2" />
                  Real-Time Activity Feed
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {newsActivity.map((item, index) => (
                  <div key={index} className="border border-black/20 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <Badge
                          variant={item.action === "BUY" ? "default" : "destructive"}
                          className={item.action === "BUY" ? "bg-green-600" : "bg-red-600"}
                        >
                          {item.action}
                        </Badge>
                        <span className="font-semibold">{item.company}</span>
                        <span className="text-sm text-black/60">{item.time}</span>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {item.source}
                      </Badge>
                    </div>
                    <div className="text-sm mb-2">
                      <span className="text-black/80">Controversy:</span> {item.controversy}
                    </div>
                    <div className="text-sm mb-2">
                      <span className="text-black/80">Reasoning:</span> {item.reasoning}
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-black/60">Sentiment:</span>
                        <div
                          className={`text-xs px-2 py-1 rounded ${item.sentiment > 0 ? "bg-green-600" : "bg-red-600"}`}
                        >
                          {item.sentiment > 0 ? "+" : ""}
                          {item.sentiment}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Current Positions */}
            <Card className="bg-yellow-400 text-black border-black">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2" />
                  Current Positions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {positions.map((position, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 border border-black/20 rounded-lg"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="font-semibold">{position.symbol}</div>
                        <div className="text-sm text-black/60">{position.shares} shares</div>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold">${position.value.toLocaleString()}</div>
                        <div
                          className={`text-sm flex items-center ${position.pnl >= 0 ? "text-green-400" : "text-red-400"
                            }`}
                        >
                          {position.pnl >= 0 ? (
                            <TrendingUp className="w-3 h-3 mr-1" />
                          ) : (
                            <TrendingDown className="w-3 h-3 mr-1" />
                          )}
                          ${Math.abs(position.pnl)} ({position.pnlPercent >= 0 ? "+" : ""}
                          {position.pnlPercent}%)
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Risk Metrics & Algorithm Status */}
          <div className="space-y-4">
            <Card className="bg-yellow-400 text-black border-black">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="w-5 h-5 mr-2" />
                  Risk Metrics
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {riskMetrics.map((metric, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-black/80">{metric.label}</span>
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold">{metric.value}</span>
                      <div
                        className={`w-2 h-2 rounded-full ${metric.status === "good"
                            ? "bg-green-500"
                            : metric.status === "moderate"
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="bg-yellow-400 text-black border-black">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  Algorithm Health
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>API Status</span>
                    <Badge className="bg-green-600">Online</Badge>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Data Feed</span>
                    <Badge className="bg-green-600">Active</Badge>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>News Sources</span>
                    <span>12/12</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Last Update</span>
                    <span>2s ago</span>
                  </div>
                </div>
                <Separator className="bg-black/20" />
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>False Positives</span>
                    <span className="text-green-400">4.2%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Missed Signals</span>
                    <span className="text-yellow-400">1.8%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Avg Trade Size</span>
                    <span>$8,450</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-yellow-400 text-black border-black">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="w-5 h-5 mr-2" />
                  Top Controversies
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Regulatory Issues</span>
                    <span>23%</span>
                  </div>
                  <Progress value={23} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Earnings Surprises</span>
                    <span>31%</span>
                  </div>
                  <Progress value={31} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Legal Disputes</span>
                    <span>18%</span>
                  </div>
                  <Progress value={18} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Product Issues</span>
                    <span>28%</span>
                  </div>
                  <Progress value={28} className="h-2" />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
