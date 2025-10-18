from __future__ import annotations
from typing import Optional, Protocol, Any

class ContactList(list["Contact"]):
    def search(self, name: str) -> list["Contact"]:
        """All contacts with search name in name."""
        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts
    
class Contact:
    all_contacts = ContactList()

    def __init__(self, /, name: str = "", email: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.all_contacts.append(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"{self.name!r}, {self.email!r}" f")"
    
class AddressHolder:
    def __init__(
            self,
            /,
            street: str = "",
            city: str = "",
            state: str = "",
            code: str ="",
            **kwargs: Any,
            ) -> None:
        super().__init__(**kwargs)
        self.street = street
        self.city = city
        self.state = state
        self.code = code

class Friend(Contact, AddressHolder):
    def __init__(self, /, phone: str="", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.phone =