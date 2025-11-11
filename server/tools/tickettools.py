import uuid

def create_ticket(title, severity, summary):
  '''
  Creates and returns a ticket with the given title, severity, and summary.
  The ticket is a dict of the form
  {
    "ticket_id": id,
    "title": title,
    "severity": severity,
    "summary": summary
  }
  '''
  return {
    "ticket_id": f"T-{uuid.uuid4().hex[:6].upper()}",
    "title": title,
    "severity": severity,
    "summary": summary
  }