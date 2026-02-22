# Data schema (canonical)

## Market quotes (`data/market/usd_sofr_ois_market_quotes.csv`)
Columns:
- `asof` (YYYY-MM-DD)
- `curve` (e.g. `USD-SOFR-OIS`)
- `instrument_type` (`DEPOSIT` or `OIS_SWAP`)
- `tenor` (`ON`, `1W`, `1M`, `3M`, `6M`, `9M`, `1Y`..`30Y`)
- `quote_type` (`RATE`)
- `quote` (decimal rate, e.g. 0.0525)
- `fixed_leg_freq` (empty for deposits, `1Y` for swaps)
- `fixed_leg_day_count` (e.g. `ACT/360`)
- `float_index` (e.g. `SOFR`)
- `float_leg_day_count` (e.g. `ACT/360`)
- `currency` (`USD`)

## Portfolio (`data/portfolio/usd_swap_portfolio.csv`)
Columns:
- `trade_id`, `trade_date`, `effective_date`, `maturity_date`
- `pay_receive_fixed` (`PAY` or `RECEIVE`)
- `notional` (USD)
- `fixed_rate` (decimal)
- fixed leg: `fixed_leg_freq`, `fixed_leg_day_count`
- float leg: `float_index`, `float_leg_freq`, `float_leg_day_count`, `float_spread_bps`
- curve mapping: `discount_curve`, `projection_curve` (projection currently assumed = discount in demo engine)

## Scenarios (`data/scenarios.csv`)
Columns:
- `scenario` (name)
- `parallel_bp` (parallel shift, bp)
- `short_end_bp` (additional shift applied to <=2Y, bp)
- `long_end_bp` (additional shift applied to >=10Y, bp)
