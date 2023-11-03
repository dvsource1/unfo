from firebase.logic import add_entry, set_entry


class Seller:
  def __init__(self, name, phone, location):
    self.name = name
    self.phone = phone
    self.location = location
    
  def to_dict(self):
    return {
      'name': self.name,
      'phone': self.phone,
      'location': self.location
    }
  
  @classmethod
  def from_dict(cls, data):
    return Seller(data.get('name'), data.get('phone'), data.get('location'))

  def __repr__(self):
    return f"Seller: {str(self.to_dict())}"

  def __str__(self) -> str:
    return str(self.to_dict())
  
  def save(self):
    return add_entry('sellers', self.to_dict())
  
  def update(self):
    return set_entry('sellers', self.phone, self.to_dict())


class Car:
  def __init__(self, url, make, model, year, mileage, gear, fuel, engine, price, seller, timestamp, options, details):
    self.url = url
    self.make = make
    self.model = model
    self.year = year
    self.mileage = mileage
    self.gear = gear
    self.fuel = fuel
    self.engine = engine
    self.price = price
    self.seller = seller
    self.timestamp = timestamp
    self.options = options
    self.details = details
    
  def to_dict(self):
    return {
      'url': self.url,
      'make': self.make,
      'model': self.model,
      'year': self.year,
      'mileage': self.mileage,
      'gear': self.gear,
      'fuel': self.fuel,
      'engine': self.engine,
      'price': self.price,
      'seller': self.seller,
      'timestamp': self.timestamp,
      'options': self.options,
      'details': self.details
    }
    
  @classmethod
  def from_dict(cls, data):
    return Car(
      data.get('url'),
      data.get('make'),
      data.get('model'),
      data.get('year'),
      data.get('mileage'),
      data.get('gear'),
      data.get('fuel'),
      data.get('engine'),
      data.get('price'),
      data.get('seller'),
      data.get('timestamp'),
      data.get('options'),
      data.get('details')
    )
    
  def __repr__(self):
    return f"Car: {str(self.to_dict())}"
  
  def __str__(self) -> str:
    return str(self.to_dict())
  
  def save(self):
    return add_entry('cars', self.to_dict())
  
  def update(self):
    return set_entry('cars', self.url, self.to_dict())