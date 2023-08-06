import dataclasses

from shopify_client.billing.schema.requests.discount_value import DiscountValue


@dataclasses.dataclass
class Discount:
    durationLimitInIntervals: int
    value: DiscountValue
