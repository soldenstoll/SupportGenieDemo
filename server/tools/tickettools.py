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
  title = title.strip()
  severity = severity.strip()
  summary = summary.strip()
  return {
    "ticket_id": f"T-{uuid.uuid4().hex[:6].upper()}",
    "title": title,
    "severity": severity,
    "summary": summary
  }

def print_ticket(ticket):
  '''
  Prints ticket in the format
  Ticket [id]: 
    Title: [Title] 
    Severity: [severity]
    Summary: [summary]
  '''
  res = f"Ticket {ticket['ticket_id']}:\nTitle: {ticket['title']}\nSeverity: "
  res += f"{ticket['severity']}\nSummary: {ticket['summary']}"
  return res
