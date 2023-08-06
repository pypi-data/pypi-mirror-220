from __future__ import annotations

from datetime import datetime, date
from enum import Enum

import repleno as repl

class _OrderType(Enum):
    WORK_ORDER = "Work Order"
    PURCHASE_ORDER = "Purchase Order"
    NOT_SET = "Not set"


class _Order:
    __slot__ = ["_sku", "due_date", "qty", "type"]

    def __init__(self, sku, due_date, qty, type=_OrderType.NOT_SET):
        if not isinstance(sku, repl.SKU):
            raise TypeError("sku must be of SKU type")

        self._sku = sku
        self.due_date = due_date
        self.qty = qty
        self.type = type

    def __repr__(self) -> str:
        return f"Order(sku=SKU({self._sku}), due_date={self._due_date:%Y-%m-%d}, qty={self._qty}, type={self._type})"

    def __str__(self) -> str:
        return f"{self._qty} of {self._sku} on {self._due_date:%Y-%m-%d}"

    def __eq__(self, other: _Order) -> bool:
        if isinstance(other, _Order):
            return (
                self.sku == other.sku
                and self.due_date == other.due_date
                and self.qty == other.qty
            )
        return False

    @property
    def sku(self):
        return self._sku

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if not isinstance(value, (datetime, date)):
            raise TypeError("due date must a datetime or date object.")

        self._due_date = value

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        try:
            value = float(value)
        except TypeError:
            print("order qty must be an integer or a float.")
            raise
        if value < 0:
            return ValueError(f"order qty must be a positive number.")

        self._qty = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, _OrderType):
            raise TypeError("Value must be of type OrderType.")

        self._type = value


    def to_dict(self):
        return {"location": self.sku.location, "item": self.sku.item, "due_date": self.due_date, "qty": self.qty, "order_type": self.type.value}