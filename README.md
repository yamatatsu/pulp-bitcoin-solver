このリポジトリはcursorで作成したものです。
細かい手修正は入れていますが、ほぼ全てAIによるコーディングです。

以下がコーディングに用いた全プロンプトです。

> pythonと線形計画のライブラリPuLPを使って過去30日間のビットコインの値動きをもとにどのような取引をしたら最も効率よく資金を増やせるか解いてください。
> 元手は100万円とし、取引手数料は0円であると仮定します。

> 毎日の取引について、円を表示して

> ビットコインの一般的な取引手数料を定義して

> 現在の実装では、毎日10000円を取引に使える、という実装になっていますか？

> pipenvを使ってpulpのバージョン管理を行ってください

> pipenvを用いたセットアップと実行方法をreadmeに記載してください

> pipfileにsolver.pyを実行するスクリプトを定義して

以下、cursorで作成したreadmeです。

# Bitcoin Trading Optimizer

ビットコインの過去30日間の価格データを基に、線形計画法（Linear Programming）を用いて最適な取引戦略を計算するプログラムです。

## 特徴

- PuLPライブラリを使用した線形計画問題の解決
- 取引手数料の考慮（0.2%）
- 利用可能な資金内での取引制限
- 現実的な取引量の制約

## 必要条件

- Python 3.9以上
- pipenv

## セットアップ

1. pipenvのインストール（まだインストールしていない場合）:
```bash
brew install pipenv
```

2. プロジェクトの依存関係のインストール:
```bash
pipenv install
```

## 実行方法

定義済みスクリプトを使用:
```bash
pipenv run solve
```

## 出力例

プログラムは以下の情報を出力します：

- 取引の最適化状態
- 最終資金と利益
- 取引手数料率
- 各取引の詳細（日付、取引量、価格、手数料）
- 取引後の現金残高とBTC残高
- 取引総額と手数料総額

## カスタマイズ

`solver.py`の以下のパラメータを調整することで、異なる条件での最適化が可能です：

- `initial_cash`: 初期資金（円）
- `TRADING_FEE_RATE`: 取引手数料率
- `coin_prices`: ビットコインの価格データ

## 注意事項

- このプログラムは過去のデータを基に最適化を行うため、将来の取引を保証するものではありません
- 実際の取引では、市場の流動性や価格変動など、追加の要因を考慮する必要があります
- これは教育目的のプログラムであり、実際の投資判断には使用しないでください 