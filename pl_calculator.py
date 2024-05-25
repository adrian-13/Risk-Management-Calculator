import streamlit as st

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

st.title("Risk Management Calculator")

st.header("Calculate Profit/Loss and Recommended Capital")

total_capital = st.number_input("Total Capital - _The total amount of capital available for trading._ ", value=100000.0, format="%.2f")
capital = st.number_input("Capital - _The amount of money you are investing in this position._", value=10000.0, format="%.2f")
leverage = st.number_input("Leverage", value=10)
risk_percentage = st.number_input("Risk Percentage - _The percentage of your total trading capital that you are willing to risk on this trade._", value=5.0, format="%.1f")
taker_fee = st.number_input("Taker Fee (%)", value=0.055, format="%.3f") / 100
maker_fee = st.number_input("Maker Fee (%)", value=0.02, format="%.3f") / 100
entry_price = st.number_input("Entry Price ($)", value=69361.0, format="%.2f")
exit_price_tp1 = st.number_input("Exit Price TP1 ($)", value=69039.0, format="%.2f")
exit_price_tp2 = st.number_input("Exit Price TP2 ($)", value=68826.0, format="%.2f")
exit_price_tp3 = st.number_input("Exit Price TP3 ($)", value=68606.0, format="%.2f")
stop_loss_price = st.number_input("Stop Loss Price ($)", value=69500.0, format="%.2f")
proportion_closed_tp1 = st.number_input("Proportion Closed TP1 (%)", value=50) / 100
proportion_closed_tp2 = st.number_input("Proportion Closed TP2 (%)", value=30) / 100
proportion_closed_tp3 = st.number_input("Proportion Closed TP3 (%)", value=20) / 100

if st.button("Calculate"):
    pl_tp1 = calculate_pl_with_fees(entry_price, exit_price_tp1, capital, leverage, proportion_closed_tp1, taker_fee, maker_fee)
    pl_tp2 = calculate_pl_with_fees(entry_price, exit_price_tp2, capital, leverage, proportion_closed_tp2, taker_fee, maker_fee)
    pl_tp3 = calculate_pl_with_fees(entry_price, exit_price_tp3, capital, leverage, proportion_closed_tp3, taker_fee, maker_fee)
    remaining_after_tp1 = proportion_closed_tp2 + proportion_closed_tp3
    pl_remaining_tp1 = calculate_pl_with_fees(entry_price, entry_price, capital, leverage, remaining_after_tp1, taker_fee, maker_fee)
    remaining_after_tp2 = proportion_closed_tp3
    pl_remaining_tp2 = calculate_pl_with_fees(entry_price, entry_price, capital, leverage, remaining_after_tp2, taker_fee, maker_fee)
    total_pl_after_tp1 = round(pl_tp1 + pl_remaining_tp1, 2)
    total_pl_after_tp2 = round(pl_tp1 + pl_tp2 + pl_remaining_tp2, 2)
    total_pl_all_tp = round(pl_tp1 + pl_tp2 + pl_tp3, 2)
    pl_stop_loss = calculate_pl_with_fees(entry_price, stop_loss_price, capital, leverage, 1, taker_fee, maker_fee, is_stop_loss=True)
    recommended_capital = calculate_recommended_capital(entry_price, stop_loss_price, total_capital, risk_percentage, leverage, taker_fee)
    
    st.write("")
    st.write(f"**Recommended capital to risk 5% of total capital:** {recommended_capital}")
    st.write("")
    st.write(f"**Total P/L if SL is hit after TP1:** {total_pl_after_tp1}")
    st.write(f"**Total P/L if SL is hit after TP2:** {total_pl_after_tp2}")
    st.write(f"**Total P/L if all TP are hit:** {total_pl_all_tp}")
    st.write("")
    st.write(f"**P/L for TP1:** {pl_tp1}")
    st.write(f"**P/L for TP2:** {pl_tp2}")
    st.write(f"**P/L for TP3:** {pl_tp3}")
    st.write("")
    st.write(f"**P/L for remaining after TP1 (SL hit at entry price):** {pl_remaining_tp1}")
    st.write(f"**P/L for remaining after TP2 (SL hit at entry price):** {pl_remaining_tp2}")
    st.write(f"**P/L if Stop Loss is hit directly:** {pl_stop_loss}")
    

