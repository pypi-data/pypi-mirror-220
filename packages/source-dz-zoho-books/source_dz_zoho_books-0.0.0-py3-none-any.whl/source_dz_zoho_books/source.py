#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple, Union

from datetime import datetime, timedelta
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources.streams import IncrementalMixin
from airbyte_cdk.sources.streams.core import StreamData
import requests
import urllib.parse
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from source_dz_zoho_books.auth import ZohoBooksAuthenticator
from .api import ZohoBooksAPI

"""
TODO: Most comments in this class are instructive and should be deleted after the source is implemented.

This file provides a stubbed example of how to use the Airbyte CDK to develop both a source connector which supports full refresh or and an
incremental syncs from an HTTP API.

The various TODOs are both implementation hints and steps - fulfilling all the TODOs should be sufficient to implement one basic and one incremental
stream from a source. This pattern is the same one used by Airbyte internally to implement connectors.

The approach here is not authoritative, and devs are free to use their own judgement.

There are additional required TODOs in the files within the integration_tests folder and the spec.yaml file.
"""


# Basic full refresh stream
class DzZohoBooksStream(HttpStream, ABC):
    """
    TODO remove this comment

    This class represents a stream output by the connector.
    This is an abstract base class meant to contain all the common functionality at the API level e.g: the API base URL, pagination strategy,
    parsing responses etc..

    Each stream should extend this class (or another abstract subclass of it) to specify behavior unique to that stream.

    Typically for REST APIs each stream corresponds to a resource in the API. For example if the API
    contains the endpoints
        - GET v1/customers
        - GET v1/employees

    then you should have three classes:
    `class DzZohoBooksStream(HttpStream, ABC)` which is the current class
    `class Customers(DzZohoBooksStream)` contains behavior to pull data for customers using v1/customers
    `class Employees(DzZohoBooksStream)` contains behavior to pull data for employees using v1/employees

    If some streams implement incremental sync, it is typical to create another class
    `class IncrementalDzZohoBooksStream((DzZohoBooksStream), ABC)` then have concrete stream implementations extend it. An example
    is provided below.

    See the reference docs for the full list of configurable options.
    """

    def __init__(self, start_date, **kwargs):
        super().__init__(**kwargs)
        self._start_date = start_date

    @property
    def url_base(self) -> str:
        return "https://www.zohoapis.in/books/"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        TODO: Override this method to define a pagination strategy. If you will not be using pagination, no action is required - just return None.

        This method should return a Mapping (e.g: dict) containing whatever information required to make paginated requests. This dict is passed
        to most other methods in this class to help you form headers, request bodies, query params, etc..

        For example, if the API accepts a 'page' parameter to determine which page of the result to return, and a response from the API contains a
        'page' number, then this method should probably return a dict {'page': response.json()['page'] + 1} to increment the page count by 1.
        The request_params method should then read the input next_page_token and set the 'page' param to next_page_token['page'].

        :param response: the most recent response from the API
        :return If there is another page in the result, a mapping (e.g: dict) containing information needed to query the next page in the response.
                If there are no more pages in the result, return None.
        """
        next_page = response.json().get("page_context")
        if not next_page:
            return None
        elif  next_page["has_more_page"] == False:
            return None
        return {"page": next_page["page"]+1}

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        return {
            "per_page": 50,
            **(next_page_token or {})
        }

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        """
        :return an iterable containing each record in the response
        """
        data = response.json().get(self.name)
        if isinstance(data, list):
            for record in data:
                yield self.transform(record=record, **kwargs)
        else:
            yield self.transform(record=data, **kwargs)

    def transform(self, record: MutableMapping[str, Any], stream_slice: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:
        return record

class IncrementalDzZohoBooksStream(DzZohoBooksStream, IncrementalMixin):
    cursor_field = "date"
    intervals = 60

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(start_date, **kwargs)
        self.start_date = start_date
        self._cursor_value = None
    
    @property
    def state(self) -> Mapping[str, Any]:
        if self._cursor_value:
            return { self.cursor_field: self._cursor_value.strftime('%Y-%m-%d') }
        else:
            return { self.cursor_field: self.start_date.strftime('%Y-%m-%d') }
        
    @state.setter
    def state(self, value: Mapping[str, Any]):
        self._cursor_value = datetime.strptime(value[self.cursor_field], '%Y-%m-%d')

    def read_records(self, *args, **kwargs) -> Iterable[Mapping[str, Any]]:
        for record in super().read_records(*args, **kwargs):
            if self._cursor_value:
                latest_record_date = datetime.strptime(record[self.cursor_field], '%Y-%m-%d')
                self._cursor_value = max(self._cursor_value, latest_record_date)
            yield record
    
    def _chunk_date_range(self, start_date: datetime) -> List[Mapping[str, Any]]:
        """
        Returns a list of each day between the start date and now.
        The return value is a list of dicts {'date': date_string}.
        """
        dates = []
        while start_date.timestamp() <= datetime.now().timestamp():
            dates.append({self.cursor_field: start_date.strftime('%Y-%m-%d')})
            start_date += timedelta(days=1)
        return dates

    def stream_slices(self, sync_mode, cursor_field: List[str] = None, stream_state: Mapping[str, Any] = None) -> Iterable[Optional[Mapping[str, Any]]]:
        start_date = datetime.strptime(stream_state[self.cursor_field], '%Y-%m-%d') if stream_state and self.cursor_field in stream_state else self.start_date
        return self._chunk_date_range(start_date)

class Contacts(DzZohoBooksStream):
    primary_key = "contact_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/contacts"

# incremental
class Estimates(IncrementalDzZohoBooksStream):
    primary_key = "estimate_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/estimates?date={str(stream_slice['date'])}"

# incremental
class Salesorders(IncrementalDzZohoBooksStream):
    primary_key = "salesorder_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/salesorders?date={str(stream_slice['date'])}"

# incremental
class Invoices(IncrementalDzZohoBooksStream):
    primary_key = "invoice_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/invoices?date={str(stream_slice['date'])}"

# incremental
class RecurringInvoices(IncrementalDzZohoBooksStream):
    primary_key = "recurring_invoice_id"
    
    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(start_date, **kwargs)
        self.cursor_field = "start_date"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/recurringinvoices?start_date={str(stream_slice['start_date'])}"

# incremental
class Creditnotes(IncrementalDzZohoBooksStream):
    primary_key = "creditnote_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/creditnotes?date={str(stream_slice['date'])}"

# incremental
class Customerpayments(IncrementalDzZohoBooksStream):
    primary_key = "payment_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/customerpayments?date={str(stream_slice['date'])}"

# incremental
class Expenses(IncrementalDzZohoBooksStream):
    primary_key = "expense_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/expenses?date={str(stream_slice['date'])}"
    
# incremental
class RecurringExpenses(IncrementalDzZohoBooksStream):
    primary_key = "recurring_expense_id"

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(start_date, **kwargs)
        self.cursor_field = "last_created_date"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/recurringexpenses?last_created_date={str(stream_slice['last_created_date'])}"

class Retainerinvoices(DzZohoBooksStream):
    primary_key = "retainerinvoice_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/retainerinvoices"

# incremental
class Purchaseorders(IncrementalDzZohoBooksStream):
    primary_key = "purchaseorder_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/purchaseorders?date={stream_slice['date']}"

# incremental
class Bills(IncrementalDzZohoBooksStream):
    primary_key = "bill_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/bills?date={stream_slice['date']}"

# incremental
class RecurringBills(IncrementalDzZohoBooksStream):
    primary_key = "recurring_bill_id"

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(start_date, **kwargs)
        self.cursor_field = "start_date"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/recurringbills?start_date={stream_slice['start_date']}"

# incremental
class VendorCredits(IncrementalDzZohoBooksStream):
    primary_key = "vendor_credit_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        if not stream_slice:
            return "v3/vendorcredits"
        else:
            return f"v3/vendorcredits?date={stream_slice['date']}"

# incremental
class Vendorpayments(IncrementalDzZohoBooksStream):
    primary_key = "payment_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        if not stream_slice:
            return "v3/vendorpayments"
        else:
            return f"v3/vendorpayments?date={stream_slice['date']}"

class Bankaccounts(DzZohoBooksStream):
    primary_key = "account_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/bankaccounts"

# incremental
class Banktransactions(DzZohoBooksStream):
    primary_key = "transaction_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        if not stream_slice:
            return "v3/banktransactions"
        else:
            return f"v3/banktransactions?date={stream_slice['date']}"

class Chartofaccounts(DzZohoBooksStream):
    primary_key = "account_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/chartofaccounts"

# incremental
class Journals(IncrementalDzZohoBooksStream):
    primary_key = "journal_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/journals?date={stream_slice['date']}"

class Basecurrencyadjustment(DzZohoBooksStream):
    primary_key = "base_currency_adjustment_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/basecurrencyadjustment"

class Projects(DzZohoBooksStream):
    primary_key = "Project_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/projects"

# incremental
class TimeEntries(IncrementalDzZohoBooksStream):
    primary_key = "time_entry_id"

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(start_date, **kwargs)
        self.cursor_field = "from_date"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return f"v3/projects/timeentries?from_date={stream_slice['from_date']}"

class Items(DzZohoBooksStream):
    primary_key = "item_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/items"
    
class Users(DzZohoBooksStream):
    primary_key = "user_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/users"

class Currencies(DzZohoBooksStream):
    primary_key = "currency_id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "v3/settings/currencies"

# Source
class SourceDzZohoBooks(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        :param config:  the user-input config object conforming to the connector's spec.yaml
        :param logger:  logger object
        :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
        """
        api = ZohoBooksAPI(config)
        return api.check_connection()

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        auth = ZohoBooksAuthenticator(
            token_refresh_endpoint="https://accounts.zoho.in/oauth/v2/token",
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            refresh_token=config["refresh_token"]
        )

        start_date = datetime.strptime(config["start_date"], '%Y-%m-%dT%H:%M:%S%z')    
        init_params = {
            "authenticator": auth,
            "start_date": start_date
        }

        return [
            Contacts(**init_params),
            Estimates(**init_params),
            Salesorders(**init_params),
            Invoices(**init_params),
            RecurringInvoices(**init_params),
            Creditnotes(**init_params),
            Customerpayments(**init_params),
            Expenses(**init_params),
            RecurringExpenses(**init_params),
            Retainerinvoices(**init_params),
            Purchaseorders(**init_params),
            Bills(**init_params),
            RecurringBills(**init_params),
            VendorCredits(**init_params),
            Vendorpayments(**init_params),
            Bankaccounts(**init_params),
            Banktransactions(**init_params),
            Chartofaccounts(**init_params),
            Journals(**init_params),
            # Basecurrencyadjustment(**init_params),
            Projects(**init_params),
            TimeEntries(**init_params),
            Items(**init_params),
            Users(**init_params),
            Currencies(**init_params)
        ]

