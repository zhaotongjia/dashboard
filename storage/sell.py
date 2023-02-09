from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime

class Sell(Base):
    # TODO declare table name
    __tablename__ = "sell"

    id = Column(Integer, primary_key=True)
    
    # TODO create the necessary columns following the id example above
    sell_id = Column(String(250), nullable=False)
    item_name = Column(String(250), nullable=False)
    item_price = Column(Float, nullable=False)
    sell_qty = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)
    date_created = Column(String(100), nullable=False)

    def __init__(self, sell_id, item_name, item_price, sell_qty, trace_id):
        # TODO assign the parameter values to the object's properties
        self.sell_id = sell_id
        self.item_name = item_name
        self.item_price = item_price
        self.sell_qty = sell_qty
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        # TODO create a dict, and assign object properties to your dict
        dict = {}
        dict['id'] = self.id
        dict['sell_id'] = self.sell_id
        dict['item_name'] = self.item_name
        dict['item_price'] = self.item_price
        dict['sell_qty'] = self.sell_qty
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        # TODO return dict
        return dict
