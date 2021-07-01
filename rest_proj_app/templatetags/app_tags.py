from django import template
register=template.Library()
@register.filter(name="get_val")
def get_val(dic):
   total=0
   for k, v in dic.items():
       total+=v
   return total
@register.filter(name="get_item")
def get_item(dic):
    s=''
    for k in dic.keys():
        s+=k+' '
    return s
@register.filter(name="get_index")
def get_index(dic,k):
    for i  in dic.keys():
      return list(dic.keys()).index(k)
    