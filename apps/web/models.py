from django.conf import settings
from django.db import models

from apps.utils.models import BaseModel


class DwollaCustomer(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dwolla_customers')
    balance = models.FloatField(default=0, blank=True)
    is_active = models.BooleanField(default=True)
    customer_id = models.CharField(max_length=100, help_text="customer id from dwolla")
    status = models.CharField(max_length=100, blank=True, null=True, help_text="status of customer from dwolla")
    first_name = models.CharField(max_length=100, help_text="An individual Customer's first name. Must be less than or equal to 50 characters and contain no special characters.")
    last_name = models.CharField(max_length=100, help_text="An individual Customer's last name. Must be less than or equal to 50 characters and contain no special characters.")
    email = models.CharField(max_length=100, help_text="Customer's email address.")
    ip_address = models.CharField(max_length=100, blank=True, null=True, help_text="Customer's IP address.")
    type = models.CharField(max_length=100, default="personal", help_text="The Verified Customer type. Set to personal if creating a verified personal Customer.")
    address1 = models.CharField(max_length=100, help_text="First line of the street address of the Customer's permanent residence. Must be less than or equal to 50 characters and contain no special characters. Note: PO Boxes are not allowed.")
    address2 = models.CharField(max_length=100, blank=True, null=True, help_text="Second line of the street address of the Customer's permanent residence. Must be less than or equal to 50 characters and contain no special characters. Note: PO Boxes are not allowed.")
    city = models.CharField(max_length=100, help_text="City of Customer's permanent residence.")
    state = models.CharField(max_length=100, help_text="Two letter abbreviation of the state in which the Customer resides, e.g. CA.")
    postal_code = models.CharField(max_length=100, help_text="Postal code of Customer's permanent residence. US five-digit ZIP or ZIP + 4 code. e.g. 50314.")
    date_of_birth = models.CharField(max_length=100, help_text="Customer's date of birth in YYYY-MM-DD format. Must be between 18 to 125 years of age.")
    ssn = models.CharField(max_length=100, help_text="Last four or full 9 digits of the Customer's Social Security Number.")
    phone = models.CharField(max_length=100, blank=True, null=True, help_text="Customer's 10 digit phone number. No hyphens or other separators, e.g. 3334447777.")
    correlation_id = models.CharField(max_length=100, blank=True, null=True, help_text="A unique string value attached to a customer which can be used for traceability between Dwolla and your application. Must be less than or equal to 255 characters and contain no spaces. Acceptable characters are: a-Z, 0-9, -, ., and _. Note: Sensitive Personal Identifying Information (PII) should not be used in this field and it is recommended to use a random value for correlationId, like a UUID. Uniqueness is enforced on correlationId across Customers.")

    business_name = models.CharField(max_length=100, blank=True, null=True, help_text="Registered business name.")
    doing_business_as = models.CharField(max_length=100, blank=True, null=True, help_text="Preferred business name – also known as fictitious name, or assumed name.")
    business_type = models.CharField(max_length=100, blank=True, null=True, help_text="	Business structure. Possible values are corporation, llc, partnership.")
    business_classification = models.CharField(max_length=100, blank=True, null=True, help_text="The industry classification Id that corresponds to Customer’s business. Reference the Business Classifications section to learn how to generate this Id.")
    ein = models.CharField(max_length=100, blank=True, null=True, help_text="Employer Identification Number.")
    website = models.CharField(max_length=100, blank=True, null=True, help_text="Business’ website. e.g. https://www.domain.com")
    controller = models.CharField(max_length=1000, blank=True, null=True, help_text="A controller JSON object.")
    def __str__(self):
        return self.email

class DwollaFundingSource(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dwolla_funding_sources')
    is_active = models.BooleanField(default=True)
    funding_id =  models.CharField(max_length=100, blank=True, null=True, help_text="funding source id")
    status = models.CharField(max_length=100, blank=True, null=True, help_text="status of funding source")
    type = models.CharField(max_length=100, blank=True, null=True, help_text="type of funding source")
    bank_account_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of bank account: checking, savings, general-ledger or loan.")
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Arbitrary nickname for the funding source. Must be 50 characters or less.")
    bank_name =  models.CharField(max_length=100, blank=True, null=True, help_text="funding source id")
    fingerprint =  models.CharField(max_length=225, blank=True, null=True, help_text="funding source fingerprint")
    channels = models.CharField(max_length=300, blank=True, null=True, help_text="An array containing a list of processing channels. ACH is the default processing channel for bank transfers. Acceptable value for channels is: wire. e.g. “channels”: [ “wire” ]. A funding source (Bank Account) added using the wire channel only supports a funds transfer going to the bank account from a balance. As a result, wire as a destination funding source can only be added where the Customer account type is a Verified Customer. Note: channels is a premium feature that must be enabled on your account and is only available to select Dwolla customers.")
    def __str__(self):
        return self.name
    
class DwollaTransferSource(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dwolla_transfer_sources')
    status = models.CharField(max_length=255, blank=True, null=True)
    funding_id = models.CharField(max_length=255, blank=True, null=True)
    transfer_id = models.CharField(max_length=100, blank=True, null=True, help_text="transfer id from dwolla")
    amount = models.FloatField()
    currency = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True, help_text="deposit, withdraw")
    clearing = models.CharField(max_length=255, blank=True, null=True, help_text="A clearing JSON object that contains source and destination keys to slow down or expedite a transfer.")
    def __str__(self):
        return self.name
    
class PlaidToken(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plaid_tokens')
    link_token = models.CharField(max_length=255, blank=True, null=True)
    public_token = models.CharField(max_length=255, blank=True, null=True)
    account_id = models.CharField(max_length=255, blank=True, null=True)