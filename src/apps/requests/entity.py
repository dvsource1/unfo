from firebase.logic import add_entry, set_entry


class Request:
  def __init__(self, name, base, is_paginate=False, is_active=True):
    self.name = name
    self.base = base
    self.is_paginate = is_paginate
    self.is_active = is_active

  def to_dict(self) -> dict:
    return {
      'name': self.name,
      'base': self.base,
      'is_paginate': self.is_paginate,
      'is_active': self.is_active
    }

  @staticmethod
  def from_dict(data) -> 'Request':
    return Request(data.get('name'), data.get('base'), data.get('is_paginate'), data.get('is_active'))
  
  def __repr__(self) -> str:
    return f"Request: {str(self.to_dict())}"
  
  def __str__(self) -> str:
    return str(self.to_dict())


class Source:
  def __init__(self, key, name, host, requests, is_active=True):
    self.key = key
    self.name = name
    self.host = host
    self.is_active = is_active
    self.requests = [Request.from_dict(request) for request in (requests or [])]
  
  def to_dict(self) -> dict:
    return {
      'key': self.key,
      'name': self.name,
      'host': self.host,
      'is_active': self.is_active,
      'requests': self.requests
    }
  
  @staticmethod
  def from_dict(data) -> 'Source':
    return Source(data.get('key'), data.get('name'), data.get('host'), data.get('requests'), data.get('is_active'))
  
  def __repr__(self) -> str:
    return f"Source: {str(self.to_dict())}"
    
  def __str__(self) -> str:
    return str(self.to_dict())
  
  def save(self):
    return add_entry('sources', self.to_dict())
  
  def update(self):
    return set_entry('sources', self.key, self.to_dict())