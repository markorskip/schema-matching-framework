# This file will define what a schema is ie tables with columns, columns with data types and possible example data points


from typing import List
from pydantic import BaseModel

class DataType(Enum):
    

class Column(BaseModel):
    name: str
    data_type: DataType

class Table(BaseModel):
    columns: List[Column]

class Schema(BaseModel):    
    tables: List[Table]