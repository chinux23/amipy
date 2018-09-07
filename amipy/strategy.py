import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import copy

template = """<?xml version="1.0" encoding="ISO-8859-1"?>
<AmiBroker-Analysis CompactMode="0">
<General>
<FormatVersion>1</FormatVersion>
<Symbol>XINA50</Symbol>
<FormulaPath>Formulas\\Albert\\COINS\\90299701_BTC_15_BollStd_20180622.afl</FormulaPath>
<FormulaContent>#include "Formulas/Custom/Helper/BacktestHelper.afl";//Use PlotPerformance()\r\n//Model file\t\r\n//#include "Formulas/Custom/Basic/TrendEXV.afl";\r\n\r\nStrategyName = "BTC_15_BollStd_20180622";\r\nStrategyID = 0;\r\n\r\nfunction BollStd(DayEnd,FollowReverse,Len,Wid)\r\n{\r\n\tKn = IndKn();\r\n\tHL = (High+Low)/2;\r\n\tMid = MA(HL,Len);\r\n\tStd = StDev(HL,Len);\r\n\tUpper = Mid+Wid*Std;\r\n\tLower = Mid-Wid*Std;\r\n\t\r\n\tSIG_L = HL&gt;Ref(Upper,-1);\t\t\r\n\tSIG_S = HL&lt;Ref(Lower,-1);\r\n\t\r\n\tBSIG = IIf(FollowReverse&gt;0,SIG_L,SIG_S);\r\n\tSSIG = IIf(FollowReverse&gt;0,SIG_S,SIG_L);\t\r\n\tLastKn = Kn&gt;Ref(Kn,1);\r\n\tCSIG = Cross(HL,Mid) || Cross(Mid,HL) || IIf(DayEnd&gt;0,LastKn,0);\r\n\r\n\treturn getCS(BSIG,SSIG,CSIG);\r\n}\r\n\r\nc101 = \tBollStd(0,1,200,1.5)\t;\r\nc102 =\tBollStd(0,1,300,1.5)\t;\r\nc103 =\tBollStd(0,1,500,1.5)\t;\r\nc104 =\tBollStd(0,1,600,1.5)\t;\r\nc105 =\tBollStd(0,1,200,2)\t;\r\nc106 =\tBollStd(0,1,300,2)\t;\r\nc107 =\tBollStd(0,1,500,2)\t;\r\nc108 =\tBollStd(0,1,600,2)\t;\r\nc109 =\tBollStd(0,1,200,2.5)\t;\r\nc110 =\tBollStd(0,1,300,2.5)\t;\r\nc111 =\tBollStd(0,1,500,2.5)\t;\r\nc112 =\tBollStd(0,1,600,2.5)\t;\r\n\r\n\r\ncond = c101+c102+c103+c104+c105+c106+c107+c108+c109+c110+c111+c112;\r\ncond = c101;\r\nVote = 0;\r\nBSIG = Cond &gt; Vote;\r\nSSIG = Cond &lt; -Vote;\r\nCSIG = Cond == 0;\r\n//-------------------------------------------------------------------\r\nBuy\t\t= BSIG;\r\nShort\t= SSIG;\r\nSell\t= Cover = CSIG;\r\nPlotPerformance(BSIG,SSIG,CSIG,StrategyID,StrategyName);\r\n</FormulaContent>
<ApplyTo>1</ApplyTo>
<RangeType>0</RangeType>
<RangeAmount>7</RangeAmount>
<FromDate>2016-12-20 00:00:00</FromDate>
<ToDate>2017-12-31</ToDate>
<SyncOnSelect>0</SyncOnSelect>
<RunEvery>0</RunEvery>
<RunEveryInterval>5min</RunEveryInterval>
<IncludeFilter>
<ExcludeMode>0</ExcludeMode>
<OrSelection>0</OrSelection>
<Favourite>0</Favourite>
<Index>0</Index>
<Type0>0</Type0>
<Category0>-1</Category0>
<Type1>1</Type1>
<Category1>-1</Category1>
<Type2>2</Type2>
<Category2>-1</Category2>
<Type3>3</Type3>
<Category3>-1</Category3>
<Type4>4</Type4>
<Category4>-1</Category4>
<Type5>5</Type5>
<Category5>-1</Category5>
<Type6>6</Type6>
<Category6>-1</Category6>
</IncludeFilter>
<ExcludeFilter>
<ExcludeMode>1</ExcludeMode>
<OrSelection>0</OrSelection>
<Favourite>0</Favourite>
<Index>0</Index>
<Type0>0</Type0>
<Category0>-1</Category0>
<Type1>1</Type1>
<Category1>-1</Category1>
<Type2>2</Type2>
<Category2>-1</Category2>
<Type3>3</Type3>
<Category3>-1</Category3>
<Type4>4</Type4>
<Category4>-1</Category4>
<Type5>5</Type5>
<Category5>-1</Category5>
<Type6>6</Type6>
<Category6>-1</Category6>
</ExcludeFilter>
</General>
<BacktestSettings>
<InitialEquity>10000</InitialEquity>
<TradeFlags>3</TradeFlags>
<MaxLossStopMode>0</MaxLossStopMode>
<MaxLossStopValue>0</MaxLossStopValue>
<MaxLossStopAtStop>1</MaxLossStopAtStop>
<ProfitStopMode>0</ProfitStopMode>
<ProfitStopValue>0</ProfitStopValue>
<ProfitStopAtStop>1</ProfitStopAtStop>
<TrailingStopMode>0</TrailingStopMode>
<TrailingStopPeriods>0</TrailingStopPeriods>
<TrailingStopValue>0</TrailingStopValue>
<TrailingStopAtStop>1</TrailingStopAtStop>
<CommissionMode>0</CommissionMode>
<CommissionValue>0</CommissionValue>
<BuyPriceField>0</BuyPriceField>
<BuyDelay>0</BuyDelay>
<SellPriceField>0</SellPriceField>
<SellDelay>0</SellDelay>
<ShortPriceField>0</ShortPriceField>
<ShortDelay>0</ShortDelay>
<CoverPriceField>0</CoverPriceField>
<CoverDelay>0</CoverDelay>
<ReportSystemFormula>0</ReportSystemFormula>
<ReportSystemSettings>0</ReportSystemSettings>
<ReportOverallSummary>1</ReportOverallSummary>
<ReportSummary>1</ReportSummary>
<ReportTradeList>1</ReportTradeList>
<LoadRemainingQuotes>1</LoadRemainingQuotes>
<Periodicity>-2</Periodicity>
<InterestRate>0</InterestRate>
<ReportOutPositions>1</ReportOutPositions>
<UseConstantPriceArrays>0</UseConstantPriceArrays>
<PointsOnlyTest>1</PointsOnlyTest>
<AllowShrinkingPosition>0</AllowShrinkingPosition>
<RangeType>0</RangeType>
<RangeLength>6</RangeLength>
<RangeFromDate>2016-12-20 00:00:00</RangeFromDate>
<RangeToDate>2017-12-31</RangeToDate>
<ApplyTo>1</ApplyTo>
<FilterQty>2</FilterQty>
<IncludeFilter>
<ExcludeMode>0</ExcludeMode>
<OrSelection>0</OrSelection>
<Favourite>0</Favourite>
<Index>0</Index>
<Type0>0</Type0>
<Category0>-1</Category0>
<Type1>1</Type1>
<Category1>-1</Category1>
<Type2>2</Type2>
<Category2>-1</Category2>
<Type3>3</Type3>
<Category3>-1</Category3>
<Type4>4</Type4>
<Category4>-1</Category4>
<Type5>5</Type5>
<Category5>-1</Category5>
<Type6>6</Type6>
<Category6>-1</Category6>
</IncludeFilter>
<ExcludeFilter>
<ExcludeMode>1</ExcludeMode>
<OrSelection>0</OrSelection>
<Favourite>0</Favourite>
<Index>0</Index>
<Type0>0</Type0>
<Category0>-1</Category0>
<Type1>1</Type1>
<Category1>-1</Category1>
<Type2>2</Type2>
<Category2>-1</Category2>
<Type3>3</Type3>
<Category3>-1</Category3>
<Type4>4</Type4>
<Category4>-1</Category4>
<Type5>5</Type5>
<Category5>-1</Category5>
<Type6>6</Type6>
<Category6>-1</Category6>
</ExcludeFilter>
<UseOptimizedEvaluation>0</UseOptimizedEvaluation>
<BacktestRangeType>0</BacktestRangeType>
<BacktestRangeLength>6</BacktestRangeLength>
<BacktestRangeFromDate>2016-12-20 00:00:00</BacktestRangeFromDate>
<BacktestRangeToDate>2017-12-31</BacktestRangeToDate>
<MarginRequirement>100</MarginRequirement>
<SameDayStops>0</SameDayStops>
<RoundLotSize>0</RoundLotSize>
<TickSize>0</TickSize>
<DrawdownPriceField>0</DrawdownPriceField>
<ReverseSignalForcesExit>1</ReverseSignalForcesExit>
<NoDefaultColumns>0</NoDefaultColumns>
<AllowSameBarExit>1</AllowSameBarExit>
<ExtensiveOptimizationWarning>1</ExtensiveOptimizationWarning>
<WaitForBackfill>0</WaitForBackfill>
<MaxRanked>4</MaxRanked>
<MaxTraded>1</MaxTraded>
<MaxTracked>100</MaxTracked>
<PortfolioReportMode>0</PortfolioReportMode>
<MinShares>0.1</MinShares>
<SharpeRiskFreeReturn>5</SharpeRiskFreeReturn>
<PortfolioMode>0</PortfolioMode>
<PriceBoundCheck>1</PriceBoundCheck>
<AlignToReferenceSymbol>0</AlignToReferenceSymbol>
<ReferenceSymbol>^DJI</ReferenceSymbol>
<UPIRiskFreeReturn>5.4</UPIRiskFreeReturn>
<NBarStopMode>0</NBarStopMode>
<NBarStopValue>0</NBarStopValue>
<NBarStopReentryDelay>0</NBarStopReentryDelay>
<MaxLossStopReentryDelay>0</MaxLossStopReentryDelay>
<ProfitStopReentryDelay>0</ProfitStopReentryDelay>
<TrailingStopReentryDelay>0</TrailingStopReentryDelay>
<AddFutureBars>0</AddFutureBars>
<DistChartSpacing>5</DistChartSpacing>
<ProfitDistribution>1</ProfitDistribution>
<MAFEDistribution>1</MAFEDistribution>
<IndividualDetailedReports>0</IndividualDetailedReports>
<PortfolioReportTradeList>1</PortfolioReportTradeList>
<LimitTradeSizeAsPctVol>10</LimitTradeSizeAsPctVol>
<DisableSizeLimitWhenVolumeIsZero>1</DisableSizeLimitWhenVolumeIsZero>
<UsePrevBarEquityForPosSizing>0</UsePrevBarEquityForPosSizing>
<NBarStopHasPriority>0</NBarStopHasPriority>
<UseCustomBacktestProc>0</UseCustomBacktestProc>
<CustomBacktestProcFormulaPath/>
<MinPosValue>0</MinPosValue>
<MaxPosValue>0</MaxPosValue>
<ChartInterval>2160001</ChartInterval>
<DisableRuinStop>0</DisableRuinStop>
<OptTarget>HuangIndex</OptTarget>
<WFMode>0</WFMode>
<GenerateReport>1</GenerateReport>
<MaxLongPos>0</MaxLongPos>
<MaxShortPos>0</MaxShortPos>
<SeparateLongShortRank>0</SeparateLongShortRank>
<TotalSymbolQty>2</TotalSymbolQty>
<EnableUserReportCharts>1</EnableUserReportCharts>
<ChartWidth>800</ChartWidth>
<ChartHeight>480</ChartHeight>
<SettlementDelay>0</SettlementDelay>
<PortfolioReportSystemFormula>1</PortfolioReportSystemFormula>
<InterestRateSymbol/>
<MarginRate>0</MarginRate>
<IncludeBHStats>1</IncludeBHStats>
<BHSymbol>^DJI</BHSymbol>
<MCEnable>1</MCEnable>
<MCRuns>1000</MCRuns>
<MCPosSizeMethod>0</MCPosSizeMethod>
<MCPosSizeShares>100</MCPosSizeShares>
<MCPosSizeValue>1000</MCPosSizeValue>
<MCPosSizePctEquity>5</MCPosSizePctEquity>
<MCChartEquityCurves>1</MCChartEquityCurves>
<MCStrawBroomLines>0</MCStrawBroomLines>
<Scenario>0</Scenario>
<MCChartEquityScale>0</MCChartEquityScale>
<MCUseEquityChanges>0</MCUseEquityChanges>
<MCLogScaleFinalEquity>0</MCLogScaleFinalEquity>
<MCLogScaleDrawdown>0</MCLogScaleDrawdown>
<MCNegativeDrawdown>1</MCNegativeDrawdown>
<ISEnabled>1</ISEnabled>
<ISStartDate>2000-01-01</ISStartDate>
<ISEndDate>2004-01-01</ISEndDate>
<ISLastDate>2016-01-01</ISLastDate>
<ISStep>1</ISStep>
<ISStepUnit>3</ISStepUnit>
<ISAnchored>0</ISAnchored>
<ISLastUsesToday>1</ISLastUsesToday>
<OSEnabled>1</OSEnabled>
<OSStartDate>2004-01-01</OSStartDate>
<OSEndDate>2005-01-01</OSEndDate>
<OSLastDate>2017-01-01</OSLastDate>
<OSStep>1</OSStep>
<OSStepUnit>3</OSStepUnit>
<OSAnchored>0</OSAnchored>
<OSLastUsesToday>1</OSLastUsesToday>
</BacktestSettings>
</AmiBroker-Analysis>
"""

class ProjectSetting:
    yearly = -4
    quarterly = -3
    monthly = -2
    weekly = -1
    daily = 0
    daynight = 1
    hourly = 2
    min_15 = 3
    min_5 = 4
    min_1 = 5
    min_3 = 10
    min_7 = 11
    min_10 = 12
    min_12 = 13
    min_20 = 14

    def __init__(self):
        # load the xml string
        self.root = ET.fromstring(copy.copy(template))
        self.General = self.root.getchildren()[0]
        self.BacktestSettings = self.root.getchildren()[1]

        self._symbol = self.General.find("Symbol")
        self._formula = self.General.find("FormulaContent")
        self._formulapath = self.General.find("FormulaPath")
        self._period = self.BacktestSettings.find("Periodicity")

    @property
    def symbol(self):
        return self._symbol.text

    @symbol.setter
    def symbol(self, symbol):
        self._symbol.text = symbol

    @property
    def period(self):
        return self._period.text

    @period.setter
    def period(self, period):
        """
        settings.set_period(daily)
        """
        self._period.text = str(ProjectSetting.amibroker_period(int(period)))

    @property
    def formula(self):
        return self._formula.text

    def set_formula(self, text):
        self._formula.text = text

    @property
    def path(self):
        return self._formulapath.text

    @path.setter
    def path(self, path):
        self._formulapath.text = repr(path)

    def save(self, path):

        tree = ET.ElementTree(self.root)
        tree.write(path, encoding="ISO-8859-1")
        
        # content = ET.tostring(self.root, encoding="ISO-8859-1", method='xml')

        # with open(path, "wb") as f:
        #     f.write(content)

    @staticmethod
    def amibroker_period(interval):
        """
        amibroker uses a string to represent time intervals, which is different than literal translation.
        """
        dictionary = { 15 : ProjectSetting.min_15, 
                        5 : ProjectSetting.min_5,
                        1 : ProjectSetting.min_1,
                        3 : ProjectSetting.min_3, 
                        7 : ProjectSetting.min_7, 
                        10: ProjectSetting.min_10, 
                        12: ProjectSetting.min_12, 
                        20: ProjectSetting.min_20,
                        60: ProjectSetting.hourly,
                        720: ProjectSetting.daily, 
                        1440: ProjectSetting.daynight }

        return dictionary[interval]


class Strategy:
    
    """
    #TODO: Refactor all strategies so that they are all inherited from Strategy class.
        1. For amibroker, we need to create a singleton class.
    """

    def __init__(self, name, id, symbol, interval):
        self.name = name
        self.id = id
        self.symbol = symbol
        self.interval = interval

    def pnl(self):
        """
        Generate PnL for this strategy
        """
        raise NotImplementedError("subclass of strategy should implement this.")
    

class AmibrokerStrategy(Strategy):

    def __init__(self, name, id, symbol, interval, path):
        Strategy.__init__(name, id, symbol, interval)
        self.path = path
        self.settings = ProjectSetting()
        self.settings.symbol = symbol
        self.settings.period = interval
        self.settings.path = self.path
        self.destination = None

        with open(self.path, "rb") as f:
            # A little commment on what is happening below:
            # 1. After reading the file as binary and convert it to string, python will add b'' to the string
            # Therefore Remove b' in the beginning and ' in the end.
            # 2. Amibroker seems to add \r\n at the end of the file. So we are adding that as well to make it the same.
            formula = str(f.read())[2:-1] + r"\r\n"
            self.settings.set_formula(formula)

    def __str__(self):
        return "{id}_{symbol}_{period}_{name}".format(
            id=self.id, symbol=self.symbol, period=self.interval, name=self.name)

    def generate_apx(self, destination):
        """
        Generate Amibroker apx project file in the destination folder.
        """
        self.destination = destination
        self.settings.save(destination)


