import sys

from buses import bus_locations, filter_on_field
from coprocess import recvfrom

co = filter_on_field('direction', 'North Bound', bus_locations())

recvfrom(sys.stdin, co)
