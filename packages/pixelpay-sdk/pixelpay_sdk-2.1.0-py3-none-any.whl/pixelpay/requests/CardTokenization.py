from nacl.encoding import Base64Encoder
from ..base.Helpers import Helpers
from ..base.RequestBehaviour import RequestBehaviour
from ..models.Billing import Billing
from ..models.Card import Card


class CardTokenization(RequestBehaviour):
    def __init__(self):
        super().__init__()

        self.number: str = None
        """Card number or PAN"""

        self.cvv2: str = None
        """Card security code"""

        self.expire_month: str = None
        """Card expire month date (MM)"""

        self.expire_year: str = None
        """Card expire year date (YYYY)"""

        self.customer: str = None
        """Tokenized customer identifier (C-* format)"""

        self.cardholder: str = None
        """Cardholder name"""

        self.address: str = None
        """Customer billing address"""

        self.country: str = None
        """Customer billing country alpha-2 code (ISO 3166-1)"""

        self.state: str = None
        """Customer billing state alpha code (ISO 3166-2)"""

        self.city: str = None
        """Customer billing city"""

        self.zip: str = None
        """Customer billing postal code"""

        self.phone: str = None
        """Customer billing phone"""

        self.email: str = None
        """Customer email"""

    def setCard(self, card: Card):
        """Associate and mapping Card model properties to transaction

        Args:
            card (Card): input Card
        """
        self.number = Helpers.cleanString(card.number)
        self.cvv2 = card.cvv2
        self.expire_month = "{:02d}".format(card.expire_month)
        self.expire_year = str(card.expire_year)
        self.cardholder = Helpers.trimValue(card.cardholder)

    def setBilling(self, billing: Billing):
        self.address = Helpers.trimValue(billing.address)
        self.country = billing.country
        self.state = billing.state
        self.city = Helpers.trimValue(billing.city)
        self.zip = billing.zip
        self.phone = billing.phone

    def setCustomerToken(self, customer: str):
        """Setup customer token

        Args:
            customer (str): Tokenized customer identifier (C-* format)
        """
        self.customer = customer

    def withEncryption(self, public_key: str) -> str:
        """Encrypt fields with sensitive data.

        Args:
            public_key (str): merchant public key

        Returns:
            str: SDK public key or None
        """
        if not public_key:
            return None

        key_pair = Helpers.getKeyPair()

        number = Helpers.encrypt(self.number, public_key, key_pair)
        cvv2 = Helpers.encrypt(self.cvv2, public_key, key_pair)
        expire_month = Helpers.encrypt(self.expire_month, public_key, key_pair)
        expire_year = Helpers.encrypt(self.expire_year, public_key, key_pair)

        if (self.number == number
            and self.cvv2 == cvv2
            and self.expire_month == expire_month
            and self.expire_year == expire_year):
            return None

        self.number = number
        self.cvv2 = cvv2
        self.expire_month = expire_month
        self.expire_year = expire_year

        return key_pair.public_key.encode(encoder=Base64Encoder).decode()
