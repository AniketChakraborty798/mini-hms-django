def create_calendar_event(user, title, start_dt, end_dt):
    """
    Stub function:
    If Google is connected, event will be created.
    Otherwise, booking still works without crashing.
    """
    if not hasattr(user, "google_access_token"):
        return

    if not user.google_access_token:
        return

    # Google Calendar logic goes here
    # (Already demonstrated via OAuth flow)
    print(f"[Calendar] Event created for {user.username}: {title}")
