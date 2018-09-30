from django import template
import datetime
register = template.Library()

def interval(time):
    return(time.seconds * 1000)

register.filter('interval', interval)
