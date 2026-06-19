# fake_mt5.py
"""
A very small in‑memory stub of the MetaTrader 5 client.

The class implements all abstract methods from
`abstracts.AbstractMetaTrader5`.  It uses the dataclasses defined in
`types.py` and the enums in `enums.py`.

Author: <your name>
"""

from __future__ import annotations

import time
import random
from datetime import datetime, timedelta
from typing import Any, List, Optional

import numpy as np

# --------------------------------------------------------------
# Imports from the user‑provided files
# --------------------------------------------------------------
from mt5_grpc.core.abstracts import AbstractMetaTrader5
from mt5_grpc.core.types import (
    SymbolInfo,
    Tick,
    TradeRequest,
    OrderSendResult,
    OrderCheckResult,
    TradePosition,
    TradeDeal,
    BookInfo,
    TerminalInfo,
    AccountInfo,
    Result,
    Version,
    Error,
)
from mt5_grpc.core.enums import (
    TimeFrame,
    CopyTicks,
    OrderTime,
    OrderTypeFilling,
    TradeAction,
    OrderType,
    BookType,
    TradeReturnCode,
    PositionType,
    PositionReason,
    OrderState,
    DealEntry,
    DealType,
    DealReason,
    AccountTradeMode,
    AccountMarginMode,
    SymbolTradeMode,
    SymbolSwapMode,
    SymbolOrderGTCMode,
    SymbolOptionMode,
    SymbolOptionRight,
    SymbolTradeExecution,
    SymbolCalcMode,
    SymbolChartMode,
    ErrorCode,
)
from mt5_grpc.util.util import log_call

def _to_structured_array(data: List[dict], dtype: List[tuple]) -> np.ndarray:
    """Fast conversion from `List[Dict]` to a NumPy structured array."""
    return np.array([tuple(row[col] for col, _ in dtype) for row in data],
                    dtype=dtype)
# --------------------------------------------------------------
# Fake MT5 implementation
# --------------------------------------------------------------
class FakeMT5(AbstractMetaTrader5):
    """
    A simple, in‑memory mock of the MetaTrader 5 client.
    All data is stored locally – no real broker connection takes place.

    The class is intentionally lightweight; it only implements a few
    useful behaviours so that you can write unit tests or run demos
    without having MT5 installed.
    """

    @log_call
    def __init__(self) -> None:
        # Connection state -------------------------------------------------
        self._initialized: bool = False

        # Symbol information -----------------------------------------------
        self._symbols: dict[str, SymbolInfo] = {}

        # Orders / positions / deals ---------------------------------------
        self._orders: list[OrderSendResult] = []
        self._positions: list[TradePosition] = []
        self._deals: list[TradeDeal] = []

        # Market book ------------------------------------------------------
        self._market_book: dict[str, BookInfo] = {}

        # ID counters --------------------------------------------------------
        self._next_order_id: int = 1
        self._next_ticket_id: int = 1000
        self._next_deal_id: int = 2000

        # Last error (used by `last_error()`)
        self._last_error: Error = Error(ErrorCode.RES_S_OK, "Success")

        self._path = ''
        self._server = ''
        self._login = -1
        self._password = ''

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _new_order_id(self) -> int:
        oid = self._next_order_id
        self._next_order_id += 1
        return oid

    def _new_ticket_id(self) -> int:
        tid = self._next_ticket_id
        self._next_ticket_id += 1
        return tid

    def _new_deal_id(self) -> int:
        did = self._next_deal_id
        self._next_deal_id += 1
        return did

    # ------------------------------------------------------------------
    # Connection & account methods
    # ------------------------------------------------------------------
    @log_call
    def initialize(self, path: str, server: str, login: Any, password: str) -> bool:
        """Pretend to connect to the broker."""
        self._initialized = True
        self._path = path
        self._server = server
        self._login = login
        self._password = password

        # Create a few demo symbols if none exist yet
        for sym in ("EURUSD", "GBPUSD", "USDJPY"):
            self._symbols.setdefault(sym, SymbolInfo(name=sym,trade_mode=SymbolTradeMode.SYMBOL_TRADE_MODE_FULL))

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return True

    @log_call
    def login(self, server: str, login: Any, password: str) -> bool:
        """Pretend to log in (no real authentication)."""
        self._server = server
        self._login = login
        self._password = password
        self._initialized = True
        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return True

    @log_call
    def shutdown(self) -> bool:
        """Pretend to disconnect."""
        self._initialized = False
        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return True

    @log_call
    def version(self) -> Version:
        """Return a dummy terminal version."""
        return Version(terminal_version=123456, build=1, release_date="2023-01-01")

    @log_call
    def account_info(self) -> AccountInfo:
        """Return some made‑up account details."""
        return AccountInfo(
            balance=10000.0,
            equity=11000.0,
            margin=2000.0,
            server=self._server or "",
            trade_allowed=True,
            name=f"FakeAccount{self._login}",
            login=int(self._login) if isinstance(self._login, (int, str)) and str(self._login).isdigit() else 123456,
        )

    @log_call
    def terminal_info(self) -> TerminalInfo:
        """Return some dummy terminal info."""
        return TerminalInfo(
            build=1,
            connected=self._initialized,
            path=self._path or "",
            name="FakeTerminal",
            maxbars=1000,
            trade_allowed=True,
        )

    # ------------------------------------------------------------------
    # Symbol related methods
    # ------------------------------------------------------------------
    @log_call
    def symbols_get(self, group: Optional[str] = None) -> List[SymbolInfo]:
        return list(self._symbols.values())

    @log_call
    def symbols_total(self) -> int:
        return len(self._symbols)

    @log_call
    def symbol_select(self, symbol: str) -> bool:
        if symbol not in self._symbols:
            self._symbols[symbol] = SymbolInfo(name=symbol)
        self._symbols[symbol].select = True
        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return True

    @log_call
    def symbol_info(self, symbol: str) -> Optional[SymbolInfo]:
        return self._symbols.get(symbol)

    @log_call
    def symbol_info_tick(self, symbol: str) -> Tick:
        now_ts = int(time.time())
        tick = Tick(
            time=now_ts,
            bid=1.1000 + random.random() * 0.001,
            ask=1.1005 + random.random() * 0.001,
            last=1.1002 + random.random() * 0.001,
            volume=int(random.random() * 1000),
            flags=random.randint(1, 7),
        )
        return tick

    # ------------------------------------------------------------------
    # Rate retrieval methods
    # ------------------------------------------------------------------
    @log_call
    def copy_rates_range(
            self,
            symbol: str,
            timeframe: TimeFrame,
            date_from: datetime,
            date_to: datetime,
    ) -> Optional[np.ndarray]:
        """Return a column‑wise NumPy array of bars."""
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return None

        start_ts = int(date_from.timestamp())
        end_ts = int(date_to.timestamp())
        diff_sec = max(1, end_ts - start_ts)

        # 10 bars per minute – dummy generator
        num_bars = min(1000, diff_sec // 60) or 1

        rates: List[dict] = []
        for i in range(num_bars):
            ts = start_ts + i * 60
            open_price = 1.1000 + i * 0.0001
            high = open_price + 0.0002
            low = open_price - 0.0002
            close = open_price + 0.0001

            rates.append({
                "time": ts,
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "tick_volume": 1000 + i * 10,
                "real_volume": 1000 + i * 10,
                "spread": 1
            })

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")

        # --- columnar dtype -------------------------------------------------
        dtype = [
            ("time", "i8"),
            ("open", "f8"),
            ("high", "f8"),
            ("low", "f8"),
            ("close", "f8"),
            ("tick_volume", "f8"),
            ("real_volume", "f8"),
            ("spread", "i4")
        ]

        return _to_structured_array(rates, dtype)

    @log_call
    def copy_rates_from(
            self,
            symbol: str,
            timeframe: TimeFrame,
            date_from: datetime,
            count: int
    ) -> Optional[np.ndarray]:
        """Return a column‑wise NumPy array of the *last* `count` bars."""
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return None

        start_ts = int(date_from.timestamp())
        rates: List[dict] = []

        for i in range(count):
            ts = start_ts + i * 60
            open_price = 1.1000 + i * 0.0001
            high = open_price + 0.0002
            low = open_price - 0.0002
            close = open_price + 0.0001

            rates.append({
                "time": ts,
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "tick_volume": 1000 + i * 10,
                "real_volume": 1000 + i * 10,
                "spread": 1
            })

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")

        dtype = [
            ("time", "i8"),
            ("open", "f8"),
            ("high", "f8"),
            ("low", "f8"),
            ("close", "f8"),
            ("tick_volume", "f8"),
            ("real_volume", "f8"),
            ("spread", "i4")
        ]

        return _to_structured_array(rates, dtype)

    @log_call
    def copy_rates_from_pos(
            self,
            symbol: str,
            timeframe: TimeFrame,
            start_pos: int,
            count: int
    ) -> Optional[np.ndarray]:
        """Return a column‑wise NumPy array starting from `start_pos`."""
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return None

        rates: List[dict] = []

        for i in range(count):
            pos = start_pos + i
            ts = 1609459200 + pos * 60  # Jan 1 2021 UTC base
            open_price = 1.1000 + pos * 0.0001
            high = open_price + 0.0002
            low = open_price - 0.0002
            close = open_price + 0.0001

            rates.append({
                "time": ts,
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "tick_volume": 1000 + pos * 10,
                "real_volume": 1000 + pos * 10,
                "spread": 1
            })

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")

        dtype = [
            ("time", "i8"),
            ("open", "f8"),
            ("high", "f8"),
            ("low", "f8"),
            ("close", "f8"),
            ("tick_volume", "f8"),
            ("real_volume", "f8"),
            ("spread", "i4")
        ]

        return _to_structured_array(rates, dtype)
    # ------------------------------------------------------------------
    # Tick retrieval methods
    # ------------------------------------------------------------------

    # --------------------------------------------------------------------
    # Ticks (columnar / structured array)
    # --------------------------------------------------------------------

    @log_call
    def copy_ticks_from(
            self,
            symbol: str,
            date_from: Any,
            count: int,
            flags: CopyTicks
    ) -> Optional[np.ndarray]:
        """Return ticks as a NumPy structured array."""
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return None

        start_ts = int(date_from.timestamp() if isinstance(date_from, datetime) else date_from)
        ticks: List[Tick] = []

        for i in range(min(count, 100)):
            ts = start_ts + i
            tick = Tick(
                time=ts,
                bid=1.1000 + i * 0.00001,
                ask=1.1005 + i * 0.00001,
                last=1.1002 + i * 0.00001,
                volume=int(100 + i),
                time_msc=0,  # placeholder
                flags=random.randint(1, 7),
                volume_real=0.0
            )
            ticks.append(tick)

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")

        dtype = [
            ("time", "i8"),
            ("bid", "f8"),
            ("ask", "f8"),
            ("last", "f8"),
            ("volume", "i4"),
            ("flags", "i4")
        ]

        return _to_structured_array([t.__dict__ for t in ticks], dtype)

    @log_call
    def copy_ticks_range(
            self,
            symbol: str,
            date_from: datetime,
            date_to: datetime,
            flags: CopyTicks
    ) -> Optional[np.ndarray]:
        """Return a column‑wise NumPy array of ticks between two timestamps."""
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return None

        start_ts = int(date_from.timestamp())
        end_ts = int(date_to.timestamp())
        num_ticks = min(1000, end_ts - start_ts)

        ticks: List[Tick] = []

        for i in range(num_ticks):
            ts = start_ts + i
            tick = Tick(
                time=ts,
                bid=1.1000 + i * 0.00001,
                ask=1.1005 + i * 0.00001,
                last=1.1002 + i * 0.00001,
                volume=int(100 + i),
                time_msc=0,
                flags=random.randint(1, 7),
                volume_real=0.0
            )
            ticks.append(tick)

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")

        dtype = [
            ("time", "i8"),
            ("bid", "f8"),
            ("ask", "f8"),
            ("last", "f8"),
            ("volume", "i4"),
            ("flags", "i4")
        ]

        return _to_structured_array([t.__dict__ for t in ticks], dtype)

    # ------------------------------------------------------------------
    # Order / position / deal methods
    # ------------------------------------------------------------------
    @log_call
    def order_send(self, trade_request: TradeRequest | dict) -> Optional[OrderSendResult]:
        if not self._initialized:
            self._last_error = Error(ErrorCode.RES_E_AUTH_FAILED, "Not initialized")
            return None

        if isinstance(trade_request, dict):
            trade_request = TradeRequest(**trade_request)

        if trade_request.symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {trade_request.symbol} not found")
            return None

        order_id = self._new_order_id()
        ticket_id = self._new_ticket_id()

        # Simulate a successful execution
        result = OrderSendResult(
            ask=1.1005,
            bid=1.1000,
            comment="",
            deal=ticket_id,
            order=ticket_id,
            price=trade_request.price or 1.1002,
            request=trade_request,
            request_id=order_id,
            retcode=TradeReturnCode.TRADE_RETCODE_DONE,
            volume=trade_request.volume,
        )
        self._orders.append(result)

        # Create a position if the action is TRADE_ACTION_DEAL
        if trade_request.action == TradeAction.TRADE_ACTION_DEAL:
            pos_type = (
                PositionType.POSITION_TYPE_BUY
                if trade_request.type in (OrderType.ORDER_TYPE_BUY, OrderType.ORDER_TYPE_BUY_LIMIT, OrderType.ORDER_TYPE_BUY_STOP)
                else PositionType.POSITION_TYPE_SELL
            )
            position_ticket = ticket_id #self._new_ticket_id()
            position = TradePosition(
                ticket=position_ticket,
                symbol=trade_request.symbol,
                type=pos_type,
                magic=trade_request.magic,
                identifier=position_ticket,
                volume=trade_request.volume,
                price_open=result.price,
                sl=trade_request.sl or 0.0,
                tp=trade_request.tp or 0.0,
            )
            self._positions.append(position)

            # Deal record
            deal = TradeDeal(
                ticket=ticket_id,
                symbol=trade_request.symbol,
                type=DealType.DEAL_TYPE_BUY if pos_type == PositionType.POSITION_TYPE_BUY else DealType.DEAL_TYPE_SELL,
                entry=DealEntry.DEAL_ENTRY_IN,
                volume=trade_request.volume,
                price=result.price,
            )
            self._deals.append(deal)

        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return result

    @log_call
    def order_check(self, trade_request: TradeRequest) -> Optional[OrderCheckResult]:
        if not self._initialized:
            self._last_error = Error(ErrorCode.RES_E_AUTH_FAILED, "Not initialized")
            return None
        if isinstance(trade_request, dict):
            trade_request = TradeRequest(**trade_request)
        # Return dummy values – real MT5 would calculate margin/profit etc.
        result = OrderCheckResult(
            retcode=TradeReturnCode.TRADE_RETCODE_DONE,
            balance=10000.0,
            equity=11000.0,
            profit=0.0,
            margin=2000.0,
            margin_free=8000.0,
            margin_level=55.0,
            comment="",
            request=trade_request,
        )
        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return result

    @log_call
    def order_calc_profit(
        self, action: TradeAction, symbol: str, volume: float, price_open: float, price_close: float
    ) -> float:
        """Very naive profit calculation."""
        return (price_close - price_open) * volume

    @log_call
    def order_calc_margin(self, action: TradeAction, symbol: str, volume: float, price: float) -> float:
        """Simplified margin – 10 % of notional value."""
        return volume * price * 0.1

    @log_call
    def orders_total(self) -> int:
        return len(self._orders)

    @log_call
    def orders_get(self, symbol: Optional[str] = None, ticket: Optional[int] = None, group: Optional[Any] = None):
        result = []
        for order in self._orders:
            if symbol is not None and order.request.symbol != symbol:
                continue
            if ticket is not None and order.order != ticket:
                continue
            result.append(order)
        return result

    @log_call
    def positions_total(self) -> int:
        return len(self._positions)

    @log_call
    def positions_get(
        self,
        symbol: Optional[str] = None,
        ticket: Optional[int] = None,
        group: Optional[Any] = None,
    ):
        result = self._positions
        if ticket is not None:
            result =  filter(lambda pos: pos.ticket == ticket, self._positions)
        if symbol is not None:
            result= filter(lambda pos: pos.symbol == symbol, self._positions)
        if group is not None:
            result= filter(lambda pos: pos.group == group, self._positions)

        return list(result)
        # result = []
        # for pos in self._positions:
        #     if symbol is not None and pos.symbol != symbol:
        #         continue
        #     if ticket is not None and pos.ticket != ticket:
        #         continue
        #     result.append(pos)
        # return result

    # ------------------------------------------------------------------
    # History methods (they just proxy to the current lists)
    # ------------------------------------------------------------------
    @log_call
    def history_orders_total(self, date_from: Any, date_to: Any) -> int:
        return len(self._orders)

    @log_call
    def history_orders_get(
        self,
        date_from: Optional[Any] = None,
        date_to: Optional[Any] = None,
        group: Optional[Any] = None,
        position: Optional[int] = None,
        ticket: Optional[int] = None,
    ):
        return self.orders_get(symbol=group, ticket=ticket)

    @log_call
    def history_deals_total(self, date_from: Any, date_to: Any) -> int:
        return len(self._deals)

    @log_call
    def history_deals_get(
        self,
        date_from: Optional[Any] = None,
        date_to: Optional[Any] = None,
        group: Optional[Any] = None,
        position: Optional[int] = None,
        ticket: Optional[int] = None,
    ):
        result = []
        for deal in self._deals:
            if ticket is not None and deal.ticket != ticket:
                continue
            result.append(deal)
        return result

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------
    @log_call
    def last_error(self) -> Error:
        return self._last_error

    # ------------------------------------------------------------------
    # Market book methods
    # ------------------------------------------------------------------
    @log_call
    def market_book_add(self, symbol: str) -> bool:
        if symbol not in self._symbols:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return False
        book = BookInfo(price=1.1005, type=BookType.BOOK_TYPE_SELL, volume=1000.0, volume_dbl=2000.0)
        self._market_book[symbol] = book
        self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return True

    @log_call
    def market_book_release(self, symbol: str) -> bool:
        if symbol in self._market_book:
            del self._market_book[symbol]
            self._last_error = Error(ErrorCode.RES_S_OK, "Success")
            return True
        else:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
            return False

    @log_call
    def market_book_get(self, symbol: str) -> Optional[BookInfo]:
        book = self._market_book.get(symbol)
        if book is None:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, f"Symbol {symbol} not found")
        else:
            self._last_error = Error(ErrorCode.RES_S_OK, "Success")
        return book

    # ------------------------------------------------------------------
    # Convenience wrappers that mirror the real MT5 API
    # ------------------------------------------------------------------
    @log_call
    def Close(self, symbol: str, *, comment: Optional[str] = None, ticket: Optional[int] = None) -> bool:
        """Close an open position."""
        pos_to_close = None
        if ticket is not None:
            for p in self._positions:
                if p.ticket == ticket:
                    pos_to_close = p
                    break
        else:
            for p in self._positions:
                if p.symbol == symbol:
                    pos_to_close = p
                    break

        if pos_to_close:
            self._positions.remove(pos_to_close)
            self._last_error = Error(ErrorCode.RES_S_OK, "Success")
            return True
        else:
            self._last_error = Error(ErrorCode.RES_E_NOT_FOUND, "Position not found")
            return False

    @log_call
    def Buy(self, symbol: str, volume: float, price: Optional[float] = None, *, comment: Optional[str] = None, ticket: Optional[int] = None):
        """Send a market buy order."""
        req = TradeRequest(
            action=TradeAction.TRADE_ACTION_DEAL,
            symbol=symbol,
            volume=volume,
            comment=comment,
            price=price or 1.1002,
            type=OrderType.ORDER_TYPE_BUY,
        )
        return self.order_send(req)

    @log_call
    def Sell(self, symbol: str, volume: float, price: Optional[float] = None, *, comment: Optional[str] = None, ticket: Optional[int] = None):
        """Send a market sell order."""
        req = TradeRequest(
            action=TradeAction.TRADE_ACTION_DEAL,
            symbol=symbol,
            volume=volume,
            comment=comment,
            price=price or 1.1002,
            type=OrderType.ORDER_TYPE_SELL,
        )
        return self.order_send(req)
