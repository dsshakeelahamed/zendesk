from datetime import datetime


class Ticket:
    def __init__(self, ticket_data):
        self.status = ticket_data.get("status", "")
        self.subject = ticket_data.get("subject", "")
        self.description = ticket_data.get("description", "")
        self.requester = ticket_data.get("requester_id", -1)
        self.assignee = ticket_data.get("assignee_id", -1)
        self.ticket_id = ticket_data.get("id", -1)
        try:
            created_timestamp = ticket_data.get("created_at", "")
            created_timestamp = datetime.strptime(created_timestamp, "%Y-%m-%dT%H:%M:%SZ")
            self.created = created_timestamp.strftime("%d %B %Y %H:%M%p")
        except:
            self.created = ticket_data.get("created_at", "")

    def display(self):
        print("Ticket_id : %s" % self.ticket_id)
        print("Created on : %s" % self.created)
        print("Subject : %s" % self.subject)
        print("Status : %s" % self.status)
        print("Requested By : %s" % self.requester)
        print("Assigned By : %s" % self.assignee)
