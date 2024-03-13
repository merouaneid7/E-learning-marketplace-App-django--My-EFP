from django import template
import math
register = template.Library()


@register.simple_tag
def discount_calculation(price,discount):
    if discount == None or discount == 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)