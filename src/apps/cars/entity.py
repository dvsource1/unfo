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


class Sell:
  def __init__(self, car, url, source, price, location, timestamp):
    self.car = car
    self.url = url
    self.source = source
    self.price = price
    self.location = location
    self.timestamp = timestamp
    
  def to_dict(self):
    return {
      'car': self.car,
      'url': self.url,
      'source': self.source,
      'price': self.price,
      'location': self.location,
      'timestamp': self.timestamp
    }
  
  @classmethod
  def from_dict(cls, data):
    return Sell(
      data.get('car'),
      data.get('url'),
      data.get('source'),
      data.get('price'),
      data.get('location'),
      data.get('timestamp')
    )
  
  def __repr__(self):
    return f"Sell: {str(self.to_dict())}"
  
  def __str__(self) -> str:
    return str(self.to_dict())
  
  def save(self):
    return add_entry('sells', self.to_dict())


class Car:
  def __init__(self, make, model, year, mileage, gear, fuel, engine, options, details):
    self.make = make
    self.model = model
    self.year = year
    self.mileage = mileage
    self.gear = gear
    self.fuel = fuel
    self.engine = engine
    self.options = options
    self.details = details
    
  def to_dict(self):
    return {
      'make': self.make,
      'model': self.model,
      'year': self.year,
      'mileage': self.mileage,
      'gear': self.gear,
      'fuel': self.fuel,
      'engine': self.engine,
      'options': self.options,
      'details': self.details
    }
    
  @classmethod
  def from_dict(cls, data):
    return Car(
      data.get('make'),
      data.get('model'),
      data.get('year'),
      data.get('mileage'),
      data.get('gear'),
      data.get('fuel'),
      data.get('engine'),
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