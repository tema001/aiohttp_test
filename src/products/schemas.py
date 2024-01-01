from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ProductCreate:
    product_name: str
    price: str
    category_id: str

    id: UUID = field(default_factory=uuid4)
