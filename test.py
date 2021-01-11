from pytoolkit import classproperty

class Foo:
  @classproperty()
  def logger(cls):
    return cls.__name__

class Bar(Foo):
  pass

print(Foo.logger)
print(Bar.logger)

Foo.logger = "blub"
print(Foo.logger)
