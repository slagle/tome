from tome.artifacts.user import User

class Foo(User):
    username = "foo"
    homedir = "/home/foo"

print User.username
print("Foo is realized: %s" % Foo.is_realized())
print("Bar is realized: %s" % User.is_realized("bar"))
foo = Foo()
print("foo is realized: %s" % foo.is_realized())
Foo().realize()
print("Foo is realized: %s" % Foo().is_realized())
Foo().unrealize()
print("Foo is realized: %s" % Foo().is_realized())

