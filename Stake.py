import streamlit as st
import pandas as pd

# Initialize session states
if "history" not in st.session_state:
    st.session_state.history = []
if "money" not in st.session_state:
    st.session_state.money = {"A": 0.0, "B": 0.0}
if "profit" not in st.session_state:
    st.session_state.profit = {"A": 0.0, "B": 0.0}
if "bet_count" not in st.session_state:
    st.session_state.bet_count = 0
if "promo_count" not in st.session_state:
    st.session_state.promo_count = 0
if "non_promo_count" not in st.session_state:
    st.session_state.non_promo_count = 0

# Title
st.title("🎯 Bet Split Tracker")

# Split the screen into 70:30
top_container = st.container()
bottom_container = st.container()

with top_container:
    col_left, col_right = st.columns([8, 4])

    with col_left:
        st.header("Set Initial Balances 💵")
        a1, a2 = st.columns(2)
        with a1:
            initial_a = st.number_input("Initial A", min_value=0.0, step=1.0, value=st.session_state.money["A"])
        with a2:
            initial_b = st.number_input("Initial B", min_value=0.0, step=1.0, value=st.session_state.money["B"])

        if st.button("Set Initial Balances"):
            st.session_state.money["A"] = initial_a
            st.session_state.money["B"] = initial_b
            st.success(f"Balances set! A: {initial_a} | B: {initial_b}")

        st.header("Enter Bet Details 🎲")
        ba1, ba2 = st.columns(2)
        with ba1:
            bet_a = st.number_input("Bet Amount A", min_value=0.0, step=1.0, key="bet_a")
        with ba2:
            payout_a = st.number_input("Payout Amount A", min_value=0.0, step=1.0, key="payout_a")

        bb1, bb2 = st.columns(2)
        with bb1:
            bet_b = st.number_input("Bet Amount B", min_value=0.0, step=1.0, key="bet_b")
        with bb2:
            payout_b = st.number_input("Payout Amount B", min_value=0.0, step=1.0, key="payout_b")

        promo_applied = st.checkbox("Promo Applied?", value=False)

        if st.button("Submit Bet 🎯"):
            total_investment = bet_a + bet_b
            total_payout = payout_a + payout_b
            profit = total_payout - total_investment
            split_profit = profit / 2

            if st.session_state.money["A"] == 0:
                st.session_state.money["A"] = bet_a
            if st.session_state.money["B"] == 0:
                st.session_state.money["B"] = bet_b

            st.session_state.money["A"] -= bet_a
            st.session_state.money["B"] -= bet_b

            if promo_applied:
                if payout_a == 0:
                    payout_a = bet_a
                if payout_b == 0:
                    payout_b = bet_b

            st.session_state.money["A"] += payout_a
            st.session_state.money["B"] += payout_b

            st.session_state.profit["A"] += split_profit
            st.session_state.profit["B"] += split_profit

            st.session_state.history.append({
                "Bet A": bet_a, "Payout A": payout_a,
                "Bet B": bet_b, "Payout B": payout_b,
                "Promo Applied": promo_applied,
                "Total Investment": total_investment,
                "Total Payout": total_payout,
                "Profit": profit,
                "A Money After": st.session_state.money["A"],
                "B Money After": st.session_state.money["B"],
                "A Total Profit": st.session_state.profit["A"],
                "B Total Profit": st.session_state.profit["B"]
            })

            st.session_state.bet_count += 1
            if promo_applied:
                st.session_state.promo_count += 1
            else:
                st.session_state.non_promo_count += 1

    with col_right:
        st.header("Current Status 🚀")

        st.subheader("Accounts 💰")
        st.write(f"Person A: {st.session_state.money['A']:.2f}")
        st.write(f"Person B: {st.session_state.money['B']:.2f}")

        st.subheader("Profits 📈")
        st.write(f"Person A: {st.session_state.profit['A']:.2f}")
        st.write(f"Person B: {st.session_state.profit['B']:.2f}")

        st.subheader("Bets Stats 🎯")
        st.write(f"Total Bets Placed: {st.session_state.bet_count}")
        st.write(f"Promo Bets: {st.session_state.promo_count}")
        st.write(f"Non-Promo Bets: {st.session_state.non_promo_count}")

        if st.button("Reset Everything 🔄"):
            st.session_state.history = []
            st.session_state.money = {"A": 0.0, "B": 0.0}
            st.session_state.profit = {"A": 0.0, "B": 0.0}
            st.session_state.bet_count = 0
            st.session_state.promo_count = 0
            st.session_state.non_promo_count = 0
            st.success("All data reset!")

# Bottom 20% — History CSV
with bottom_container:
    st.header("History 📜")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
