import string
import random
from typing import List,Callable
from abc import  ABC,abstractmethod
"""functional version of strategy"""

class SupportTicket:
    def __init__(self, customer, issue):
        self.id = generate_id()
        self.customer = customer
        self.issue = issue

def generate_id(length=8):
    # helper function for generating an id
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def fifo_ordering(list: List[SupportTicket]) -> List[SupportTicket]:
    return list.copy()


def filo_ordering_strategy(list: List[SupportTicket]) -> List[SupportTicket]:
    list_copy=list.copy()
    list_copy.reverse()
    return list_copy


def random_ordering(list: List[SupportTicket]) -> List[SupportTicket]:
    list_copy=list.copy()
    random.shuffle(list_copy)
    return list_copy


def blackhole_strategy(list:List[SupportTicket]) ->List[SupportTicket]:
    return []

class CustomerSupport:
    def __init__(self):
        self.tickets = []


    def create_ticket(self, customer, issue):
        self.tickets.append(SupportTicket(customer, issue))

    def process_tickets(self,processing_strategy_fn: Callable[[List[SupportTicket]],List[SupportTicket]]):
        ticket_list=processing_strategy_fn(self.tickets)

        # if it's empty, don't do anything
        if len(ticket_list) == 0:
            print("There are no tickets to process. Well done!")
            return
        for ticket in ticket_list:
            self.process_ticket(ticket)

    def process_ticket(self, ticket: SupportTicket):
        print("==================================")
        print(f"Processing ticket id: {ticket.id}")
        print(f"Customer: {ticket.customer}")
        print(f"Issue: {ticket.issue}")
        print("==================================")

# create the application
# random_ordering=RandomOrderingStrategy()
app = CustomerSupport()

# register a few tickets
app.create_ticket("John Smith", "My computer makes strange sounds!")
app.create_ticket("Linus Sebastian", "I can't upload any videos, please help.")
app.create_ticket("Arjan Egges", "VSCode doesn't automatically solve my bugs.")

# process the tickets
app.process_tickets(fifo_ordering)