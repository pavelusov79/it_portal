from django import template

register = template.Library()


@register.filter(name='phone_number')
def _phone_number(phone):
    """
    Format phone_number as 0 (000) 000-00-00
    """
    first = phone[0]
    second = phone[1:4]
    third = phone[4:7]
    fourth = phone[7:9]
    fifth = phone[9:11]
    return f'{first} ({second}) {third}-{fourth}-{fifth}'


@register.simple_tag
def get_favorite_id_(object, user):
    """
    object: vacancy or resume
    """
    return object.get_favorite_id(user)
