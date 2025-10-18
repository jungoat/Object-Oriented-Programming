from __future__ import annotations
from typing import Optional, Protocol, Any

class Contact:
    all_contact: list["Contact"] = []

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contact.append(self)

    def __repr__(self) -> str:
        return(
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}"
            f")"
        )
    
c_1 = Contact("Dusty", "dusty@example.com")
c_2 = Contact("Steve", "steve@itmaybeahack.com")

class Supplier(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this were a real system we would send "
            f"'{order}' order to '{self.name}'"
        )

class Order:
    pass

c = Contact("Some Body", "some@example.net")
s = Supplier("Sup Plier", "supplier@example.net")

from pprint import pprint
pprint(c.all_contacts)

c.order("I need pliers")

class ContactList(list["Contact"]):
    def search(self, name: str) -> list["Contact"]:
        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts
    
class Contact:
    all_contacts = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return(
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}" f")"
        )
    
test_search = """
>>> Contact.all_contacts = ContactList()

>>> c1 = Contact("John A", "johna@example.net")
>>> c2 = Contact("John B", "johnb@sloop.net")
>>> c3 = Contact("Jenna C", "cutty@sark.io")
>>> [c.name for c in Contact.all_contacts.search('John')]
['John A', 'John B']
"""

class LongNameDict(dict[str, int]):
    def longest_key(self) -> Optional[str]:
        """사실상 max(self, key=len)이지만 모호하지 않다."""
        longest = None
        for key in self:
            if longest is None or len(key) > len(longest):
                longest = key
        return longest
    
articles_read = LongNameDict()
articles_read['lucy'] = 42
articles_read['c_c_phillips'] = 6
articles_read['steve'] = 7
articles_read.longest_key()

class Friend(Contact):
    def __init__(self, name: str, email: str, phone: str) -> None:
        super().__init__(name, email)
        self.phone = phone

f = Friend("Dusty", "Dusty@private.com", "555-1212")
Contact.all_contacts

class Emailable(Protocol):
    email: str

class MailSender(Emailable):
    def send_mail(self, message: str) -> None:
        print(f"Sending mail to {self.email=}")
        # 이메일 관련 로직은 여기에 추가

class EmailableContact(Contact, MailSender):
    pass

e = EmailableContact("John B", "johnb@sloop.net")
Contact.all_contacts

e.send_mail("Hello, test e-mail here")

class AddressHolder:
    def __init__(self, street: str, city: str, state: str, code: str) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.code = code

# 순진한 방식
class Friend(Contact, AddressHolder):
    def __init__(
            self,
            name: str,
            email: str,
            phone: str,
            street: str,
            city: str,
            state: str,
            code: str,
    ) -> None:
        Contact.__init__(self, name, email)
        AddressHolder.__init__(self, street, city, state, code)
        self.phone = phone

# 다중 상속
class Contact:
    all_contacts = ContactList()

    def __init__(self, /, name: str="", email: str="", **kwargs: Any) -> None:
        super().intit