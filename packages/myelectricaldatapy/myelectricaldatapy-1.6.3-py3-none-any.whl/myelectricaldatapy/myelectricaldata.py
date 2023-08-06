"""Class for Enedis Gateway (http://www.myelectricaldata.fr)."""
from __future__ import annotations

import logging
import re
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
from typing import Any, Collection, Optional, Tuple

import pandas as pd

from .auth import TIMEOUT, EnedisAuth

_LOGGER = logging.getLogger(__name__)


class EnedisAnalytics:
    """Data analaytics."""

    local_timezone = dt.now().astimezone().tzinfo

    def __init__(self, data: Collection[Collection[str]]) -> None:
        """Initialize Dataframe."""
        self.df = pd.DataFrame(data)

    def get_data_analytics(
        self,
        convertKwh: bool = False,
        convertUTC: bool = False,
        start_date: str | None = None,
        intervals: list[Tuple[str, str]] | None = None,
        groupby: bool = False,
        freq: str = "H",
        summary: bool = False,
        cumsums: dict[str, Any] = {},
        prices: list[dict[str, Any]] | None = None,
    ) -> Any:
        """Convert datas to analyze."""
        std_cum_sum = cumsums.get("standard", {}).get("sum_value", 0)
        std_cum_sum_price = cumsums.get("standard", {}).get("sum_price", 0)
        off_cum_sum = cumsums.get("offpeak", {}).get("sum_value", 0)
        off_cum_sum_price = cumsums.get("offpeak", {}).get("sum_price", 0)

        if not self.df.empty:
            # Convert str to datetime
            self.df.date = pd.to_datetime(self.df.date, format="%Y-%m-%d %H:%M:%S")
            self.df.date = self.df.date.dt.tz_localize(self.local_timezone)

            if convertUTC:
                self.df.date = pd.to_datetime(
                    self.df.date, utc=True, format="%Y-%m-%d %H:%M:%S"
                )

            # Substract 1 minute at midnight
            # because Pandas considers midnight as the next day while
            # for Enedis it is the day before
            if "interval_length" in self.df:
                self.df.date = self.df.date.transform(self._midnightminus)

            if start_date:
                self.df = self.df[(self.df.date > f"{start_date} 23:59:59")]

            self.df.index = self.df.date

            # Add mark
            self.df["notes"] = "standard"

        if self.df.empty:
            return self.df.to_dict()

        if self.df.get("interval_length") is not None:
            self.df.interval_length = self.df.interval_length.transform(
                self._weighted_interval
            )
        else:
            self.df.interval_length = 1

        if convertKwh:
            self.df.value = (
                pd.to_numeric(self.df.value) / 1000 * self.df.interval_length
            )
        else:
            self.df.value = pd.to_numeric(self.df.value) * self.df.interval_length

        if intervals:
            self.df = self._get_data_interval(intervals)

        if groupby:
            self.df = (
                self.df.groupby(["notes", pd.Grouper(key="date", freq=freq)])["value"]
                .sum()
                .reset_index()
            )

        if prices:
            for price in prices:
                if s_date := price.get("standard", {}).get("date"):
                    self.df.loc[
                        (self.df.notes == "standard")
                        & (
                            self.df.date.dt.date
                            == pd.to_datetime(s_date, format="%Y-%m-%d").date()
                        ),
                        "price",
                    ] = self.df.value * price.get("standard", {}).get("price", 0)
                else:
                    self.df.loc[
                        (self.df.notes == "standard"), "price"
                    ] = self.df.value * price.get("standard", {}).get("price", 0)

                if s_date := price.get("offpeak", {}).get("date"):
                    self.df.loc[
                        (self.df.notes == "offpeak")
                        & (
                            self.df.date.dt.date
                            == pd.to_datetime(s_date, format="%Y-%m-%d").date()
                        ),
                        "price",
                    ] = self.df.value * price.get("offpeak", {}).get("price", 0)
                else:
                    self.df.loc[
                        (self.df.notes == "offpeak"), "price"
                    ] = self.df.value * price.get("offpeak", {}).get("price", 0)

        if summary and prices:
            self.df.loc[(self.df.notes == "standard"), "sum_value"] = (
                self.df[(self.df.notes == "standard")].value.cumsum() + std_cum_sum
            )
            self.df.loc[(self.df.notes == "offpeak"), "sum_value"] = (
                self.df[(self.df.notes == "offpeak")].value.cumsum() + off_cum_sum
            )
            self.df.loc[(self.df.notes == "standard"), "sum_price"] = (
                self.df[(self.df.notes == "standard")].price.cumsum()
                + std_cum_sum_price
            )
            self.df.loc[(self.df.notes == "offpeak"), "sum_price"] = (
                self.df[(self.df.notes == "offpeak")].price.cumsum() + off_cum_sum_price
            )

        return self.df.to_dict(orient="records")

    def _weighted_interval(self, interval: str) -> float | int:
        """Compute weighted."""
        if interval and len(rslt := re.findall("PT([0-9]{2})M", interval)) == 1:
            return int(rslt[0]) / 60
        return 1

    def _midnightminus(self, dt_date: dt) -> dt:
        """Subtracts one minute.

        to avoid taking midnight on the next day
        """
        if dt_date.time() == dt.strptime("00:00:00", "%H:%M:%S").time():
            dt_date = dt_date - timedelta(minutes=1)
            return dt_date
        return dt_date

    def _get_data_interval(self, intervalls: list[Tuple[str, str]]) -> pd.DataFrame:
        """Group date from range time."""
        for intervall in intervalls:
            # Convert str to datetime
            start = pd.to_datetime(intervall[0], format="%H:%M:%S")
            end = pd.to_datetime(intervall[1], format="%H:%M:%S")
            # Get Time
            start = start.time()
            end = self._midnightminus(end).time()
            # Mark
            self.df.loc[
                (self.df.date.dt.time >= start) & (self.df.date.dt.time < end), "notes"
            ] = "offpeak"

        return self.df

    def get_last_value(self, data: dict[str, Any], orderby: str, value: str) -> Any:
        """Return last value after order by."""
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values(by=orderby)
            if value in df.columns:
                return df[value].iloc[-1]  # pylint: disable=unsubscriptable-object


class EnedisByPDL:
    """Get data of pdl."""

    def __init__(
        self, token: str, session: Optional[Any] = None, timeout: int = TIMEOUT
    ) -> None:
        """Initialize."""
        self.auth = EnedisAuth(token, session, timeout)
        self.offpeaks: list[str] = []
        self.dt_offpeak: list[dt] = []
        self.last_access: date | None = None

    async def async_fetch_datas(
        self, service: str, pdl: str, start: dt | None = None, end: dt | None = None
    ) -> Any:
        """Retrieve date from service.

        service:    contracts, identity, contact, addresses,
                    daily_consumption_max_power,
                    daily_consumption, daily_production,
                    consumption_load_curve, production_load_curve
        """
        self.last_access = dt.now()
        path_range = ""
        if start and end:
            start_date = start.strftime("%Y-%m-%d")
            end_date = end.strftime("%Y-%m-%d")
            path_range = f"/start/{start_date}/end/{end_date}"
        path = f"{service}/{pdl}{path_range}"
        return await self.auth.request(path=path)

    async def async_valid_access(self, pdl: str) -> Any:
        """Return valid access."""
        return await self.async_fetch_datas("valid_access", pdl)

    async def async_has_access(self, pdl: str) -> bool:
        """Check valid access."""
        access = await self.async_valid_access(pdl)
        return access.get("valid", False) is True

    async def async_get_contract(self, pdl: str) -> Any:
        """Return contract information."""
        contract = {}
        contracts = await self.async_fetch_datas("contracts", pdl)
        usage_points = contracts.get("customer", {}).get("usage_points", "")
        for usage_point in usage_points:
            if usage_point.get("usage_point", {}).get("usage_point_id") == pdl:
                contract = usage_point.get("contracts", {})
                if offpeak_hours := contract.get("offpeak_hours"):
                    self.offpeaks = re.findall("(?:(\\w+)-(\\w+))+", offpeak_hours)
                    self.dt_offpeak = [
                        (  # type: ignore
                            dt.strptime(offpeak[0], "%HH%M"),
                            dt.strptime(offpeak[1], "%HH%M"),
                        )
                        for offpeak in self.offpeaks
                    ]
        return contract

    async def async_get_contracts(self, pdl: str) -> Any:
        """Return all contracts information."""
        return await self.async_fetch_datas("contracts", pdl)

    async def async_get_address(self, pdl: str) -> Any:
        """Return adress information."""
        address = {}
        addresses = await self.async_fetch_datas("addresses", pdl)
        usage_points = addresses.get("customer", {}).get("usage_points", "")
        for usage_point in usage_points:
            if usage_point.get("usage_point", {}).get("usage_point_id") == pdl:
                address = usage_point.get("usage_point")
        return address

    async def async_get_addresses(self, pdl: str) -> Any:
        """Return all adresses information."""
        return await self.async_fetch_datas("adresses", pdl)

    async def async_get_tempoday(
        self, start: dt | None = None, end: dt | None = None
    ) -> Any:
        """Return Tempo Day."""
        str_start = (
            start.strftime("%Y-%m-%d") if start else dt.now().strftime("%Y-%m-%d")
        )
        str_end = (
            end.strftime("%Y-%m-%d")
            if end
            else (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        )
        return await self.auth.request(path=f"rte/tempo/{str_start}/{str_end}")

    async def async_get_ecowatt(
        self, start: dt | None = None, end: dt | None = None
    ) -> Any:
        """Return Ecowatt information."""
        str_start = (
            start.strftime("%Y-%m-%d") if start else dt.now().strftime("%Y-%m-%d")
        )
        str_end = (
            end.strftime("%Y-%m-%d")
            if end
            else (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        )
        return await self.auth.request(path=f"rte/ecowatt/{str_start}/{str_end}")

    async def async_has_offpeak(self, pdl: str) -> bool:
        """Has offpeak hours."""
        if not self.offpeaks:
            await self.async_get_contract(pdl)
        return len(self.offpeaks) > 0

    async def async_check_offpeak(self, pdl: str, start: dt) -> bool:
        """Return offpeak status."""
        if await self.async_has_offpeak(pdl) is True:
            start_time = start.time()
            for range_time in self.offpeaks:
                starting = dt.strptime(range_time[0], "%HH%M").time()
                ending = dt.strptime(range_time[1], "%HH%M").time()
                if ending <= start_time > starting:
                    return True
        return False

    async def async_get_identity(self, pdl: str) -> Any:
        """Get identity."""
        return await self.async_fetch_datas("identity", pdl)

    async def async_get_daily_consumption(self, pdl: str, start: dt, end: dt) -> Any:
        """Get daily consumption."""
        return await self.async_fetch_datas("daily_consumption", pdl, start, end)

    async def async_get_daily_production(self, pdl: str, start: dt, end: dt) -> Any:
        """Get daily production."""
        return await self.async_fetch_datas("daily_production", pdl, start, end)

    async def async_get_details_consumption(self, pdl: str, start: dt, end: dt) -> Any:
        """Get consumption details. (max: 7 days)."""
        return await self.async_fetch_datas("consumption_load_curve", pdl, start, end)

    async def async_get_details_production(self, pdl: str, start: dt, end: dt) -> Any:
        """Get production details. (max: 7 days)."""
        return await self.async_fetch_datas("production_load_curve", pdl, start, end)

    async def async_get_max_power(self, pdl: str, start: dt, end: dt) -> Any:
        """Get consumption max power."""
        return await self.async_fetch_datas(
            "daily_consumption_max_power", pdl, start, end
        )

    async def async_close(self) -> None:
        """Close session."""
        await self.auth.async_close()
