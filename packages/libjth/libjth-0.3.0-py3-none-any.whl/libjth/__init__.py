'''J.T. Hartzfeld's Personal Library
    This is a collection of generally useful snippets and bits that make
    their way into most of my projects.
'''

from auto_all import start_all, end_all, public
try:
    from . import enums
except ImportError:
    import enums

start_all()

Priority = enums.Priority
Planets = enums.Planets

end_all()
