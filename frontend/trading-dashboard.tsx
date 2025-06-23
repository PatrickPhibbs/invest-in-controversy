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


interface PositionInfo {
  'buy-price': number;
  quantity: number;
  'buy-date': string;
}

type Positions = {
  [ticker: string]: PositionInfo;
};

interface AccountData {
  'portfolio-value': number;
  pnl: number;
};

import positionsData from '../../Coinv/backend/data/positions.json';
import accountData from '../../Coinv/backend/data/portfolio-info.json';

const positions: Positions = positionsData as Positions;
const account: AccountData = accountData as AccountData;

export default function TradingDashboard() {
  // Mock data
  const portfolioValue = account['portfolio-value']
  const dailyPnL = account.pnl
  const dailyPnLPercent = (dailyPnL / portfolioValue) * 100;

  const positionsArray = Object.entries(positions).map(([symbol, info]) => ({
    symbol,
    shares: info.quantity,
    buyPrice: info['buy-price'],
    buyDate: info['buy-date'],
    value: info.quantity * info['buy-price'],
    pnl: 0,
    pnlPercent: 0
  }));

  // const newsActivity = [
  //   {
  //     time: "09:34 AM",
  //     company: "Tesla Inc",
  //     controversy: "Regulatory Investigation",
  //     action: "SELL",
  //     reasoning: "SEC investigation announced - high volatility expected",
  //     sentiment: -0.78,
  //     source: "Reuters",
  //   },
  //   {
  //     time: "09:28 AM",
  //     company: "Apple Inc",
  //     controversy: "Product Recall",
  //     action: "BUY",
  //     reasoning: "Minor recall, market overreaction detected",
  //     sentiment: -0.34,
  //     source: "Bloomberg",
  //   },
  //   {
  //     time: "09:15 AM",
  //     company: "NVIDIA Corp",
  //     controversy: "Earnings Beat",
  //     action: "BUY",
  //     reasoning: "Strong earnings, positive sentiment surge",
  //     sentiment: 0.89,
  //     source: "CNBC",
  //   },
  // ] ## Don't need any of this for now as news has been removed

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




        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - News Activity Feed */}
          <div className="lg:col-span-2 space-y-4">

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
                  {positionsArray.map((position, index) => (
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





          </div>
        </div>
      </div>
    </div>
  )
}
