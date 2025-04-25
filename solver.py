from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, value  # type: ignore

# 30日間のビットコインの値動き
coin_prices = [
    11840000, 11880000, 12130000, 12540000, 12500000,
    12580000, 12590000, 12380000, 12060000, 12090000,
    12110000, 12500000, 11900000, 12090000, 11880000,
    12130000, 12080000, 11660000, 12040000, 11920000,
    11300000, 11590000, 12390000, 12480000, 12940000,
    13040000, 12550000, 12380000, 13560000, 12380000,
]

# 取引手数料（Taker手数料を想定）
TRADING_FEE_RATE = 0.002  # 0.2%

# 最適化問題を作成
prob = LpProblem("Bitcoin_Trading_Optimization", LpMaximize)

# 初期資金（100万円）
initial_cash = 1_000_000

# 1BTCの最小取引単位（例: 0.00000001 BTC = 1 Satoshi）
min_trade_unit = 0.00000001

# 決定変数の作成
# 各日の現金残高を表す変数
cash_balance = [LpVariable(f"cash_{i}", 0, None) for i in range(31)]  # 0日目から30日目まで
# 各日のビットコイン残高を表す変数
btc_balance = [LpVariable(f"btc_{i}", 0, None) for i in range(31)]  # 0日目から30日目まで
# 各日の取引量
buy = [LpVariable(f"buy_{i}", 0, None) for i in range(30)]
sell = [LpVariable(f"sell_{i}", 0, None) for i in range(30)]

# 初期状態の設定
prob += cash_balance[0] == initial_cash, "initial_cash"
prob += btc_balance[0] == 0, "initial_btc"

# 各日の取引による資金とビットコインの残高を追跡
for i in range(30):
    # 購入コストが利用可能な現金を超えないように制約
    prob += coin_prices[i] * buy[i] * (1 + TRADING_FEE_RATE) <= cash_balance[i], f"buy_limit_{i}"
    
    # 売却量が保有BTCを超えないように制約
    prob += sell[i] <= btc_balance[i], f"sell_limit_{i}"
    
    # その日のビットコインの売買による収支（手数料を考慮）
    buy_cost = coin_prices[i] * buy[i] * (1 + TRADING_FEE_RATE)  # 購入額 + 手数料
    sell_revenue = coin_prices[i] * sell[i] * (1 - TRADING_FEE_RATE)  # 売却額 - 手数料
    
    # 次の日の残高を計算
    prob += cash_balance[i+1] == cash_balance[i] - buy_cost + sell_revenue, f"cash_balance_update_{i}"
    prob += btc_balance[i+1] == btc_balance[i] + buy[i] - sell[i], f"btc_balance_update_{i}"

# 目的関数の設定（最終日の資金残高を最大化）
prob += cash_balance[30]

# 問題を解く
prob.solve()

# 結果の表示
print(f"Status: {LpStatus[prob.status]}")
print(f"最終資金: {value(cash_balance[30]):,.0f}円")
print(f"利益: {value(cash_balance[30]) - initial_cash:,.0f}円")
print(f"\n取引手数料: {TRADING_FEE_RATE*100:.1f}%")
print("\n最適な取引戦略:")

total_volume = 0
total_fee = 0
for i in range(30):
    buy_amount = value(buy[i])
    sell_amount = value(sell[i])
    if buy_amount > min_trade_unit:
        trade_amount = buy_amount * coin_prices[i]
        fee = trade_amount * TRADING_FEE_RATE
        print(f"{i+1}日目: {buy_amount:.8f} BTCを購入 (取引額: {trade_amount:,.0f}円, 手数料: {fee:,.0f}円)")
        print(f"        現金残高: {value(cash_balance[i+1]):,.0f}円, BTC残高: {value(btc_balance[i+1]):.8f} BTC")
        total_volume += trade_amount
        total_fee += fee
    if sell_amount > min_trade_unit:
        trade_amount = sell_amount * coin_prices[i]
        fee = trade_amount * TRADING_FEE_RATE
        print(f"{i+1}日目: {sell_amount:.8f} BTCを売却 (取引額: {trade_amount:,.0f}円, 手数料: {fee:,.0f}円)")
        print(f"        現金残高: {value(cash_balance[i+1]):,.0f}円, BTC残高: {value(btc_balance[i+1]):.8f} BTC")
        total_volume += trade_amount
        total_fee += fee

print(f"\n取引総額: {total_volume:,.0f}円")
print(f"手数料総額: {total_fee:,.0f}円")