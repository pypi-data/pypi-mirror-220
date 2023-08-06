import os.path
import pickle
from datetime import date, datetime
from typing import Callable, List, Union

from dateutil.relativedelta import relativedelta
from gc_integration.constants import SendUpdatesMode
from gc_integration.utils import ensure_localisation, to_localized_iso
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from tzlocal import get_localzone_name


class GoogleCalendar:
    """A wrapper class to connect with google calendar API."""

    _READ_WRITE_SCOPES = "https://www.googleapis.com/auth/calendar"

    def __init__(
        self,
        calendar: str = "primary",
        *,
        credentials: Credentials = None,
        credentials_path: str = None,
        token_path: str = None,
        save_token: bool = True,
        read_only: bool = False,
        authentication_flow_host="localhost",
        authentication_flow_port=8080,
    ):
        """Represents Google Calendar of the user.

        Specify ``credentials`` to use in requests or ``credentials_path`` and ``token_path`` to get credentials from.

        :param calendar:
                Users email address or name/id of the calendar. Default: primary calendar of the user

                If user's email or "primary" is specified, then primary calendar of the user is used.
                You don't need to specify this parameter in this case as it is a default behaviour.

                To use a different calendar you need to specify its id.
                Go to calendar's `settings and sharing` -> `Integrate calendar` -> `Calendar ID`.
        :param credentials:
                Credentials with token and refresh token.
                If specified, ``credentials_path``, ``token_path``, and ``save_token`` are ignored.
                If not specified, credentials are retrieved from "token.pickle" file (specified in ``token_path`` or
                default path) or with authentication flow using secret from "credentials.json" (specified in
                ``credentials_path`` or default path)
        :param credentials_path:
                Path to "credentials.json" file. Default: ~/.credentials
        :param token_path:
                Existing path to load the token from, or path to save the token after initial authentication flow.
                Default: "token.pickle" in the same directory as the credentials_path
        :param save_token:
                Whether to pickle token after authentication flow for future uses
        :param read_only:
                If require read only access. Default: False
        :param authentication_flow_host:
                Host to receive response during authentication flow
        :param authentication_flow_port:
                Port to receive response during authentication flow
        """

        if credentials:
            self.credentials = self._assure_refreshed(credentials)
        else:
            credentials_path = (
                credentials_path or GoogleCalendar._get_default_credentials_path()
            )
            credentials_dir, credentials_file = os.path.split(credentials_path)
            token_path = token_path or os.path.join(credentials_dir, "token.pickle")
            scopes = [self._READ_WRITE_SCOPES + (".readonly" if read_only else "")]

            self.credentials = self._get_credentials(
                token_path,
                credentials_dir,
                credentials_file,
                scopes,
                save_token,
                authentication_flow_host,
                authentication_flow_port,
            )
            self.calendar = calendar
            self.service = discovery.build(
                "calendar", "v3", credentials=self.credentials
            )

    @staticmethod
    def _assure_refreshed(credentials: Credentials):
        if not credentials.valid and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials

    @staticmethod
    def _get_credentials(
        token_path: str,
        credentials_dir: str,
        credentials_file: str,
        scopes: List[str],
        save_token: bool,
        host: str,
        port: int,
    ) -> Credentials:
        credentials = None

        if os.path.exists(token_path):
            with open(token_path, "rb") as token_file:
                credentials = pickle.load(token_file)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_path = os.path.join(credentials_dir, credentials_file)
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, scopes
                )
                credentials = flow.run_local_server(host=host, port=port)

            if save_token:
                with open(token_path, "wb") as token_file:
                    pickle.dump(credentials, token_file)

        return credentials

    @staticmethod
    def _get_default_credentials_path() -> str:
        """Checks if ".credentials" folder in home directory exists. If not, creates it.
        :return: expanded path to .credentials folder
        """
        home_dir = os.path.expanduser("~")
        credential_dir = os.path.join(home_dir, ".credentials")
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, "credentials.json")
        return credential_path

    def clear(self):
        """Deletes all the events in the calendar"""
        self.service.calendars().clear(calendarId=self.calendar).execute()

    def add_event(self, body, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Creates event in the calendar

        :param body:
                Event body.
        :param send_updates:
                Whether and how to send updates to attendees.
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/insert#optional-parameters

        :return:
                Created event object with id.
        """
        return (
            self.service.events()
            .insert(
                calendarId=self.calendar,
                body=body,
                conferenceDataVersion=1,
                sendUpdates=send_updates,
                **kwargs,
            )
            .execute()
        )

    def update_event(self, body, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Updates existing event in the calendar

        :param body:
                Event body
        :param send_updates:
                Whether and how to send updates to attendees
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/update#optional-parameters

        :return:
                Updated event object.
        """
        return (
            self.service.events()
            .update(
                calendarId=self.calendar,
                eventId=body.get("id"),
                body=body,
                conferenceDataVersion=1,
                sendUpdates=send_updates,
                **kwargs,
            )
            .execute()
        )

    def delete_event(self, event_id, send_updates=SendUpdatesMode.NONE, **kwargs):
        """Deletes an event.

        :param event_id:
                The unique event ID.
        :param send_updates:
                Whether and how to send updates to attendees
                Default is "NONE".
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/delete#optional-parameters
        """
        return (
            self.service.events()
            .delete(
                calendarId=self.calendar,
                eventId=event_id,
                sendUpdates=send_updates,
                **kwargs,
            )
            .execute()
        )

    def _list_events(
        self,
        request_method: Callable,
        time_min: Union[date, datetime],
        time_max: Union[date, datetime],
        timezone: str,
        **kwargs,
    ):
        """Lists paginated events received from request_method."""

        time_min = time_min or datetime.now()
        time_max = time_max or time_min + relativedelta(years=1)
        if not isinstance(time_min, datetime):
            time_min = datetime.combine(time_min, datetime.min.time())

        if not isinstance(time_max, datetime):
            time_max = datetime.combine(time_max, datetime.max.time())

        time_min = ensure_localisation(time_min, timezone).isoformat()
        time_max = ensure_localisation(time_max, timezone).isoformat()

        page_token = None
        while True:
            events = request_method(
                calendarId=self.calendar,
                timeMin=time_min,
                timeMax=time_max,
                pageToken=page_token,
                **kwargs,
            ).execute()
            for event_json in events["items"]:
                yield event_json
            page_token = events.get("nextPageToken")
            if not page_token:
                break

    def get_events(
        self,
        time_min=None,
        time_max=None,
        order_by=None,
        timezone=get_localzone_name(),
        single_events=False,
        query=None,
        **kwargs,
    ):
        """Lists events

        :param time_min:
                Staring date/datetime
        :param time_max:
                Ending date/datetime
        :param order_by:
                Order of the events. Possible values: "startTime", "updated". Default is unspecified stable order.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param single_events:
                Whether to expand recurring events into instances and only return single one-off events and
                instances of recurring events, but not the underlying recurring events themselves.
        :param query:
                Free text search terms to find events that match these terms in any field, except for
                extended properties.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/list#optional-parameters

        :return:
                Iterable of event objects
        """

        if not single_events and order_by == "startTime":
            raise ValueError(
                '"startTime" ordering is only available when querying single events, i.e. single_events=True'
            )
        yield from self._list_events(
            self.service.events().list,
            time_min=time_min,
            time_max=time_max,
            timezone=timezone,
            **{
                "singleEvents": single_events,
                "orderBy": order_by,
                "q": query,
                **kwargs,
            },
        )

    def get_event(self, event_id, **kwargs):
        """Returns the event with the corresponding event_id.

        :param event_id:
                The unique event ID.
        :param kwargs:
                Additional API parameters.
                See https://developers.google.com/calendar/v3/reference/events/get#optional-parameters

        :return:
                The corresponding event object or None if
                no matching ID was found.
        """
        return (
            self.service.events()
            .get(calendarId=self.calendar, eventId=event_id, **kwargs)
            .execute()
        )

    def get_free_busy(
        self,
        resource_ids: Union[str, List[str]] = None,
        *,
        time_min: Union[date, datetime] = None,
        time_max: Union[date, datetime] = None,
        timezone: str = get_localzone_name(),
        group_expansion_max: int = None,
        calendar_expansion_max: int = None,
    ):
        """Returns free/busy information for a set of calendars and/or groups.
        :param resource_ids:
                Identifier or list of identifiers of calendar(s) and/or group(s).
                Default is `default_calendar` specified in `GoogleCalendar`.
        :param time_min:
                The start of the interval for the query.
        :param time_max:
                The end of the interval for the query.
        :param timezone:
                Timezone formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich". By default,
                the computers local timezone is used if it is configured. UTC is used otherwise.
        :param group_expansion_max:
                Maximal number of calendar identifiers to be provided for a single group.
                An error is returned for a group with more members than this value.
                Maximum value is 100.
        :param calendar_expansion_max:
                Maximal number of calendars for which FreeBusy information is to be provided.
                Maximum value is 50.
        """

        time_min = time_min or datetime.now()
        time_max = time_max or time_min + relativedelta(weeks=2)

        time_min = to_localized_iso(time_min, timezone)
        time_max = to_localized_iso(time_max, timezone)

        if resource_ids is None:
            resource_ids = [self.default_calendar]
        elif not isinstance(resource_ids, (list, tuple, set)):
            resource_ids = [resource_ids]

        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": timezone,
            "groupExpansionMax": group_expansion_max,
            "calendarExpansionMax": calendar_expansion_max,
            "items": [{"id": r_id} for r_id in resource_ids],
        }

        return self.service.freebusy().query(body=body).execute()
