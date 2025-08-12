from user.models import *
from user.serializers import *
cart = Order.objects.all().first()

data = OrderSerializer(cart).data
print(data)