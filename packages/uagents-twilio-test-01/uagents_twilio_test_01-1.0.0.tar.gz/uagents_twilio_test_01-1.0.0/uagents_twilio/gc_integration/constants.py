class SendUpdatesMode:
    """Possible values of the mode for sending updates or invitations to attendees.

    * ALL - Send updates to all participants. This is the default value.
    * EXTERNAL_ONLY - Send updates only to attendees not using google calendar.
    * NONE - Do not send updates.
    """

    ALL = "all"
    EXTERNAL_ONLY = "externalOnly"
    NONE = "none"


class Visibility:
    """Possible values of the event visibility.

    * DEFAULT - Uses the default visibility for events on the calendar. This is the default value.
    * PUBLIC - The event is public and event details are visible to all readers of the calendar.
    * PRIVATE - The event is private and only event attendees may view event details.
    """

    DEFAULT = "default"
    PUBLIC = "public"
    PRIVATE = "private"


class Transparency:
    """Possible values of the event transparency.

    * OPAQUE - Default value. The event does block time on the calendar.
               This is equivalent to setting 'Show me as' to 'Busy' in the Calendar UI.
    * TRANSPARENT - The event does not block time on the calendar.
                    This is equivalent to setting 'Show me as' to 'Available' in the Calendar UI.
    """

    OPAQUE = "opaque"
    TRANSPARENT = "transparent"


class ResponseStatus:
    """Possible values for attendee's response status

    * NEEDS_ACTION - The attendee has not responded to the invitation.
    * DECLINED - The attendee has declined the invitation.
    * TENTATIVE - The attendee has tentatively accepted the invitation.
    * ACCEPTED - The attendee has accepted the invitation.
    """

    NEEDS_ACTION = "needsAction"
    DECLINED = "declined"
    TENTATIVE = "tentative"
    ACCEPTED = "accepted"
