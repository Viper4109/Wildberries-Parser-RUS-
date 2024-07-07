from pydantic import BaseModel, Field, ValidationError, root_validator
from typing import List, Dict, Any

class Item(BaseModel):
    number: int = Field(default=0)
    id: int
    name: str
    brand: str
    product_price: str = Field(default='-')
    basic_price: str = Field(default='-')
    reviewRating: float
    volume: int

    @root_validator(pre=True)
    def assign_prices(cls, values: Dict[str, Any]):
        sizes = values.get('sizes', [])
        if sizes:
            # Устанавливаем цену из первого элемента списка sizes
            first_size = sizes[0].get('price', {})
            values['product_price'] = str(first_size.get('product', 0) / 100) + ' RUB'
            values['basic_price'] = str(first_size.get('basic', 0) / 100) + ' RUB'
        return values

class Items(BaseModel):
    products: List[Item]

    @root_validator(pre=True)
    def assign_numbers(cls, values: Dict):
        if 'products' in values:
            for index, product in enumerate(values['products'], start=1):
                product['number'] = index
        return values