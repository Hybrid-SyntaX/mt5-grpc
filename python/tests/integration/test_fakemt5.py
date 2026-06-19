import numpy as np
# ──────────────────────────────────────────────────────────────
#  test_fake_mt5.py
#  ---------------------------------------------
#  Tests for mt5_fake.fake_mt5.FakeMT5 – the in‑memory MT5 stub.
#  The file mirrors the style of your integration tests (see citations 1–3).
#
#  Each public method of AbstractMetaTrader5 is covered at least once.
#  For brevity some methods are param‑tested, but every branch that
#  returns a value or changes state is asserted on.
# ──────────────────────────────────────────────────────────────

import pytest
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# Imports from the fake client you built
# ------------------------------------------------------------------
from mt5_grpc.mocks.fake_mt5 import FakeMT5
from mt5_grpc.core.enums import (
    TimeFrame,
    OrderType,
    TradeAction,
    CopyTicks,
    BookType, ErrorCode, TradeReturnCode,
)
from mt5_grpc.core.types import (
    Error,
    OrderSendResult,
    OrderCheckResult,
    SymbolInfo,
    Tick,
    AccountInfo,
    TerminalInfo, TradeRequest, BookInfo,
)
from tests.util import assert_values_are_equal


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------
@pytest.fixture(scope="module")
def fake_mt5() -> FakeMT5:
    """Return a freshly initialised FakeMT5 instance."""
    mt = FakeMT5()
    # Initialise once for the whole test module – no real broker involved.
    ok = mt.initialize(path="/tmp", login=123456, server="demo_server", password="pwd")
    assert ok
    return mt


# ------------------------------------------------------------------
# 1. Connection helpers ------------------------------------------------
# ------------------------------------------------------------------
def test_login_and_shutdown(fake_mt5: FakeMT5):
    # login should succeed even though credentials are fake
    ok = fake_mt5.login(login=123456, server="demo_server", password="pwd")
    assert ok

    # shutdown must cleanly reset the state flag
    ok = fake_mt5.shutdown()
    assert ok
    # re‑initialise for the rest of the tests
    fake_mt5.initialize(path="/tmp", login=123456, server="demo_server", password="pwd")


def test_version(fake_mt5: FakeMT5):
    ver = fake_mt5.version()
    # the stub returns a namedtuple – check its fields
    assert isinstance(ver.terminal_version, int)
    assert isinstance(ver.build, int)
    assert isinstance(ver.release_date, str)


# ------------------------------------------------------------------
# 2. Account / Terminal -------------------------------------------------
# ------------------------------------------------------------------
def test_account_info(fake_mt5: FakeMT5):
    acc = fake_mt5.account_info()
    assert isinstance(acc, AccountInfo)
    # basic sanity checks – values are from the stub
    assert acc.balance == pytest.approx(10000.0)
    assert acc.equity == pytest.approx(11000.0)


def test_terminal_info(fake_mt5: FakeMT5):
    term = fake_mt5.terminal_info()
    assert isinstance(term, TerminalInfo)
    # the stub sets 'connected' to True after initialise
    assert term.connected is True
    # we ignore data_path / retransmission – they are random in the stub
    assert isinstance(term.name, str)


# ------------------------------------------------------------------
# 3. Symbols -------------------------------------------------------------
# ------------------------------------------------------------------
def test_symbols_total_and_get(fake_mt5: FakeMT5):
    total = fake_mt5.symbols_total()
    symbols = fake_mt5.symbols_get()
    # The stub pre‑populates EURUSD, GBPUSD and USDJPY
    assert total == len(symbols)
    for sym in ["EURUSD", "GBPUSD", "USDJPY"]:
        assert sym in symbols


def test_symbol_info_and_select(fake_mt5: FakeMT5):
    info = fake_mt5.symbol_info("USDJPY")
    assert isinstance(info, SymbolInfo)
    # the stub creates a SymbolInfo with name set
    assert info.name == "USDJPY"

    # selecting a symbol marks it as selected
    ok = fake_mt5.symbol_select("EURGBP")          # new symbol – will be created automatically
    assert ok
    sel_info = fake_mt5.symbol_info("EURGBP")
    assert sel_info.select is True


# ------------------------------------------------------------------
# 4. Tick & Rate helpers -------------------------------------------------
# ------------------------------------------------------------------

def test_copy_rates_from(fake_mt5:FakeMT5):
    """`copy_rates_from` returns a NumPy structured array with the expected columns."""
    rates = fake_mt5.copy_rates_from(
        symbol="EURUSD",
        timeframe=TimeFrame.TIMEFRAME_M1,
        date_from=datetime(2024, 1, 1),
        count=10
    )

    assert isinstance(rates, np.ndarray)
    # expected column names
    for name in ("time", "open", "high", "low", "close",
                 "tick_volume","real_volume", "spread"):
        assert name in rates.dtype.names

    # exactly `count` rows were generated
    assert len(rates) == 10


def test_copy_rates_from_pos(fake_mt5:FakeMT5):
    """`copy_rates_from_pos` behaves like `copy_rates_from`, but uses a start position."""
    rates = fake_mt5.copy_rates_from_pos(
        symbol="EURUSD",
        timeframe=TimeFrame.TIMEFRAME_M1,
        start_pos=0,
        count=10
    )

    assert isinstance(rates, np.ndarray)
    for name in ("time", "open", "high", "low", "close",
                 "tick_volume","real_volume", "spread"):
        assert name in rates.dtype.names

    assert len(rates) == 10


def test_copy_rates_range(fake_mt5:FakeMT5):
    """`copy_rates_range` returns a (potentially longer) array with the same columns."""
    from_time = datetime(2024, 2, 1) - timedelta(days=1)
    to_time   = datetime(2024, 2, 1)

    rates = fake_mt5.copy_rates_range(
        symbol="EURUSD",
        timeframe=TimeFrame.TIMEFRAME_M1,
        date_from=from_time,
        date_to=to_time
    )

    assert isinstance(rates, np.ndarray)
    for name in ("time", "open", "high", "low", "close",
                 "tick_volume","real_volume", "spread"):
        assert name in rates.dtype.names

    # the stub limits the output to 1000 bars; just ensure it doesn't exceed that
    assert len(rates) <= 1000


def test_copy_ticks_from(fake_mt5: FakeMT5):
    """`copy_ticks_from` returns a structured array of tick data."""
    ticks = fake_mt5.copy_ticks_from(
        symbol="USDJPY",
        date_from=datetime(2025, 5, 14) - timedelta(hours=1),
        count=3,
        flags=CopyTicks.COPY_TICKS_ALL
    )

    assert isinstance(ticks, np.ndarray)
    for name in ("time", "bid", "ask", "last", "volume", "flags"):
        assert name in ticks.dtype.names

    assert len(ticks) == 3


def test_copy_ticks_range(fake_mt5: FakeMT5):
    """`copy_ticks_range` returns a (potentially long) tick array."""
    ticks = fake_mt5.copy_ticks_range(
        symbol="EURUSD",
        date_from=datetime(2024, 1, 1),
        date_to=datetime(2024, 1, 2),
        flags=CopyTicks.COPY_TICKS_ALL
    )

    assert isinstance(ticks, np.ndarray)
    for name in ("time", "bid", "ask", "last", "volume", "flags"):
        assert name in ticks.dtype.names

    # the stub caps the output at 1000 ticks
    assert len(ticks) <= 1000


# ------------------------------------------------------------------
# 5. Orders / Positions / Deals ------------------------------------------
# ------------------------------------------------------------------
def test_order_send_deal(fake_mt5: FakeMT5):
    """Test a normal market buy order."""
    req = TradeRequest(
        action=TradeAction.TRADE_ACTION_DEAL,
        symbol="EURUSD",
        volume=0.01,
        price=1.1005,          # explicit price – not needed for market orders
        type=OrderType.ORDER_TYPE_BUY,
    )
    res = fake_mt5.order_send(req)

    # ① Return type must be OrderSendResult
    assert isinstance(res, OrderSendResult)

    # ② Success code
    assert res.retcode == TradeReturnCode.TRADE_RETCODE_DONE

    # ③ Orders counter increased
    assert fake_mt5.orders_total() >= 1

    # ④ A position was created for a DEAL action
    assert any(p.symbol == "EURUSD" for p in fake_mt5.positions_get())


def test_order_check_deal(fake_mt5: FakeMT5):
    """Verify the order‑check logic."""
    # Build a request dictionary – the real MT5 client accepts this form.
    # Our fake implementation expects a TradeRequest, so we convert it.
    req_dict = {
        "action": TradeAction.TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 0.01,
        "type": OrderType.ORDER_TYPE_BUY,
        "price": 1.1005,
        "sl": 0.0,
        "tp": 0.0,
        "deviation": 10,
        "magic": 123456,
        "comment": "test order check",
    }

    # Convert dict → TradeRequest (your FakeMT5 implementation accepts it)
    req = TradeRequest(**req_dict)

    res = fake_mt5.order_check(req)

    # ① Return type
    assert isinstance(res, OrderCheckResult)

    # ② Success code
    assert res.retcode == TradeReturnCode.TRADE_RETCODE_DONE

    # ③ The returned balance/equity/margin values are *numbers* (stub uses constants)
    assert isinstance(res.balance, float)
    assert isinstance(res.equity, float)
    assert isinstance(res.margin, float)

    # ④ The request inside the result is identical to what we sent
    assert_values_are_equal(
        req,
        res.request,
        exclude=['price']   # the stub may adjust the price internally
    )


def test_orders_and_positions_filter(fake_mt5: FakeMT5):
    # create two orders with different symbols
    req_a = TradeRequest(action=TradeAction.TRADE_ACTION_DEAL, symbol="EURUSD", volume=0.01)
    req_b = TradeRequest(action=TradeAction.TRADE_ACTION_DEAL, symbol="GBPUSD", volume=0.02)

    fake_mt5.order_send(req_a)
    fake_mt5.order_send(req_b)

    # total orders should be at least 2
    assert fake_mt5.orders_total() >= 2

    # filter by symbol
    eur_orders = fake_mt5.orders_get(symbol="EURUSD")
    assert all(o.request.symbol == "EURUSD" for o in eur_orders)

    # filter by ticket (the order id returned)
    ticket_id = eur_orders[0].order if eur_orders else None
    if ticket_id is not None:
        specific = fake_mt5.orders_get(ticket=ticket_id)
        assert len(specific) == 1
        assert specific[0].order == ticket_id


def test_history_orders_and_deals(fake_mt5: FakeMT5):
    # history mirrors current lists in the stub
    h_total = fake_mt5.history_orders_total(datetime.now(), datetime.now())
    assert h_total == fake_mt5.orders_total()

    h_list = fake_mt5.history_orders_get()
    assert len(h_list) == fake_mt5.orders_total()

    d_total = fake_mt5.history_deals_total(datetime.now(), datetime.now())
    assert d_total == len(fake_mt5._deals)

    d_list = fake_mt5.history_deals_get()
    assert len(d_list) == d_total


# ------------------------------------------------------------------
# 6. Market book --------------------------------------------------------
# ------------------------------------------------------------------
def test_market_book_add_release_and_get(fake_mt5: FakeMT5):
    symbol = "EURGBP"

    # add a book – should succeed
    ok = fake_mt5.market_book_add(symbol)
    assert ok

    book = fake_mt5.market_book_get(symbol)
    assert isinstance(book, BookInfo)
    assert book.type == BookType.BOOK_TYPE_SELL

    # release removes it
    ok = fake_mt5.market_book_release(symbol)
    assert ok
    assert fake_mt5.market_book_get(symbol) is None


# ------------------------------------------------------------------
# 7. Convenience wrappers (Close / Buy / Sell) ---------------------------
# ------------------------------------------------------------------
def test_close_buy_sell(fake_mt5: FakeMT5):
    # open a position first
    req = TradeRequest(
        action=TradeAction.TRADE_ACTION_DEAL,
        symbol="USDJPY",
        volume=0.01,
        type=OrderType.ORDER_TYPE_BUY,
    )
    order_res = fake_mt5.order_send(req)
    assert order_res is not None

    # now close it
    closed = fake_mt5.Close(symbol="USDJPY")
    assert closed is True
    # position count should drop to zero (or at least not increase)
    assert all(p.symbol != "USDJPY" for p in fake_mt5.positions_get())


def test_buy_and_sell(fake_mt5: FakeMT5):
    buy_res = fake_mt5.Buy(symbol="EURUSD", volume=0.01, price=1.1002)
    assert isinstance(buy_res, OrderSendResult)

    sell_res = fake_mt5.Sell(symbol="GBPUSD", volume=0.02, price=1.3005)
    assert isinstance(sell_res, OrderSendResult)


# ------------------------------------------------------------------
# 8. Error handling -------------------------------------------------------
# ------------------------------------------------------------------
def test_error_handling_on_unknown_symbol(fake_mt5: FakeMT5):
    # Ask the stub to copy rates for a symbol that doesn't exist
    res = fake_mt5.copy_rates_from(symbol="NOT_A_SYMBOL", timeframe=TimeFrame.TIMEFRAME_M1, date_from=datetime.now(), count=10)
    assert res is None

    err = fake_mt5.last_error()
    assert isinstance(err, Error)
    # the error code should not be RES_S_OK
    assert err.code != ErrorCode.RES_S_OK


# ------------------------------------------------------------------
# 9. Miscellaneous helpers -----------------------------------------------
# ------------------------------------------------------------------
def test_order_calc__margin(fake_mt5: FakeMT5):
    margin = fake_mt5.order_calc_margin(TradeAction.TRADE_ACTION_DEAL, "EURUSD", 0.01, 1.1025)
    # stub uses 10 % of notional value
    assert margin == pytest.approx(0.01 * 1.1025 * 0.1)

def test_order_calc_profit(fake_mt5: FakeMT5):
    res = fake_mt5.order_calc_profit(
        action=TradeAction.TRADE_ACTION_DEAL,
        symbol="EURUSD",
        volume=1.0,
        price_open=1.2000,
        price_close=1.2500
    )
    assert res == pytest.approx((1.25 - 1.20) * 1.0)
# ------------------------------------------------------------------
# End of test file -------------------------------------------------------
