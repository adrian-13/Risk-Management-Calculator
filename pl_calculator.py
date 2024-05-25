def calculate_pl_with_fees(entry_price, exit_price, capital, leverage, proportion_closed, taker_fee, maker_fee, is_stop_loss=False):
    # Calculate the total value of the position
    total_position_value = capital * leverage
    
    # Calculate open fee based on total position value
    open_fee = total_position_value * taker_fee
    
    # Calculate close fee based on total position value and proportion closed
    # Use taker fee for Stop Loss close
    close_fee = total_position_value * (taker_fee if is_stop_loss else maker_fee) * proportion_closed
    
    # Calculate P/L
    price_difference = entry_price - exit_price
    percent_change = price_difference / entry_price
    leverage_gain = percent_change * leverage
    capital_gain = leverage_gain * capital
    pl = (capital_gain * proportion_closed) - open_fee - close_fee
    return round(pl, 2)

def calculate_recommended_capital(entry_price, stop_loss_price, total_capital, risk_percentage, leverage, taker_fee):
    # Calculate the amount of capital to risk (5% of total capital)
    capital_to_risk = total_capital * (risk_percentage / 100)
    
    # Calculate the price difference between entry and stop loss
    price_difference = abs(entry_price - stop_loss_price)
    
    # Calculate the percentage change for stop loss
    percent_change_sl = price_difference / entry_price
    
    # Calculate the loss per unit of capital with leverage
    leveraged_loss_per_unit = percent_change_sl * leverage
    
    # Adjust for fees
    total_taker_fee = entry_price * leverage * taker_fee * 2  # Open and close fees
    
    # Calculate the effective loss per unit of capital including fees
    effective_loss_per_unit = leveraged_loss_per_unit + (total_taker_fee / (entry_price * leverage))
    
    # Calculate the recommended capital
    recommended_capital = capital_to_risk / effective_loss_per_unit
    
    return round(recommended_capital, 2)

# Given values
entry_price = 69361
exit_price_tp1 = 69039.5
exit_price_tp2 = 68826.5
exit_price_tp3 = 68606.2
stop_loss_price = 69640
capital = 10000
leverage = 100
total_capital = 10000 # Used for recommended capital calculation
risk_percentage = 5  # We want to risk 5% of the capital.
proportion_closed_tp1 = 0.5
proportion_closed_tp2 = 0.3
proportion_closed_tp3 = 0.2
taker_fee = 0.00055  # 0.055%
maker_fee = 0.0002  # 0.02%

# Calculate P/L for each TP with fees
pl_tp1 = calculate_pl_with_fees(entry_price, exit_price_tp1, capital, leverage, proportion_closed_tp1, taker_fee, maker_fee)
pl_tp2 = calculate_pl_with_fees(entry_price, exit_price_tp2, capital, leverage, proportion_closed_tp2, taker_fee, maker_fee)
pl_tp3 = calculate_pl_with_fees(entry_price, exit_price_tp3, capital, leverage, proportion_closed_tp3, taker_fee, maker_fee)

# Calculate P/L for the remaining portion closed at Entry Price (if price hits SL at Entry Price)
# If price hits SL after TP1
remaining_after_tp1 = proportion_closed_tp2 + proportion_closed_tp3
pl_remaining_tp1 = calculate_pl_with_fees(entry_price, entry_price, capital, leverage, remaining_after_tp1, taker_fee, maker_fee)

# If price hits SL after TP2
remaining_after_tp2 = proportion_closed_tp3
pl_remaining_tp2 = calculate_pl_with_fees(entry_price, entry_price, capital, leverage, remaining_after_tp2, taker_fee, maker_fee)

# Total P/L if SL is hit after TP1
total_pl_after_tp1 = round(pl_tp1 + pl_remaining_tp1, 2)

# Total P/L if SL is hit after TP2
total_pl_after_tp2 = round(pl_tp1 + pl_tp2 + pl_remaining_tp2, 2)

# Total P/L if all TP are hit
total_pl_all_tp = round(pl_tp1 + pl_tp2 + pl_tp3, 2)

# Calculate P/L if Stop Loss is hit directly with taker fees
pl_stop_loss = calculate_pl_with_fees(entry_price, stop_loss_price, capital, leverage, 1, taker_fee, maker_fee, is_stop_loss=True)

# Calculate recommended capital to risk 5% of total capital
recommended_capital = calculate_recommended_capital(entry_price, stop_loss_price, total_capital, risk_percentage, leverage, taker_fee)

# Print the results
print("Recommended capital to risk \033[1m5%\033[0m of total capital:\033[1m", recommended_capital, "\033[0m\n")
print("Total P/L if SL is hit after TP1:\033[1m", total_pl_after_tp1,"\033[0m")
print("Total P/L if SL is hit after TP2:\033[1m", total_pl_after_tp2,"\033[0m")
print("Total P/L if all TP are hit:\033[1m", total_pl_all_tp, "\033[0m\n")
print("P/L for TP1:\033[1m", pl_tp1, "\033[0m")
print("P/L for TP2:\033[1m", pl_tp2, "\033[0m")
print("P/L for TP3:\033[1m", pl_tp3, "\033[0m\n")
print("P/L for remaining after TP1 (SL hit at entry price):\033[1m", pl_remaining_tp1, "\033[0m")
print("P/L for remaining after TP2 (SL hit at entry price):\033[1m", pl_remaining_tp2, "\033[0m\n")
print("P/L if Stop Loss is hit directly:\033[1m", pl_stop_loss, "\033[0m")
