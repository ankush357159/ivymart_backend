# Django Import
from datetime import datetime
import json
import environ
from django.conf import settings

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status

# razorpay
import razorpay

# Local Import
from ivymart.models import Order, ShippingAddress, Product, OrderItem
from ivymart.serializers.orderSerializers import OrderSerializer


# views start from here

env = environ.Env()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = json.loads(data["orderItems"])
    # print(data)
    # print(orderItems)

    if orderItems and len(orderItems) == 0:
        return Response(
            {"detail": "No Order Items", "status": status.HTTP_400_BAD_REQUEST}
        )
    else:
        # (1) Set up razorpay client
        amount = data["totalPrice"]
        client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.RAZOR_SECRET_KEY))

        payment = client.order.create(
            {
                "amount": int(float(amount)) * 100,
                "currency": "INR",
                "payment_capture": "1",
            }
        )

        # (2) Create Order
        order = Order.objects.create(
            user=user,
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"],
            order_id=payment["id"],
        )
        print("Order Details:",order)

        # (3) Create Shipping Address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data["address"],
            city=data["city"],
            postalCode=["postalCode"],
            state=["state"],
            country=["country"],
        )
        print("Shipping Details: ", shipping)

        # (4) Create order items

        for i in orderItems:
            # for i in range(0,len(orderItems)-1):
            product = Product.objects.get(id=i["product"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i["qty"],
                price=i["price"],
                image=product.image.url,
            )

            # (5) Update Stock

            product.countInStock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)

        data = {"payment": payment, "order": serializer.data}
        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response(
                {"detail": "Not Authorized  to view this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except:
        return Response(
            {"detail": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(id=pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response("Order was paid")


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(id=pk)
    order.isDeliver = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response("Order was Delivered")


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def startPayment(request):
    # request.data is coming from frontend
    user = request.user
    amount = request.data["amount"]
    data = request.data

    # setup razorpay client
    client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.RAZOR_SECRET_KEY))


    # create razorpay order
    payment = client.order.create(
        {"amount": int(float(amount)) * 100, "currency": "INR", "payment_capture": "1"}
    )

    # we are saving an order with isPaid=False
    order = Order.objects.create(
        user=user,
        order_id=payment["id"],
        taxPrice=data["taxPrice"],
        shippingPrice=data["shippingPrice"],
        totalPrice=data["totalPrice"],
    )

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '20 November 2020 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {"payment": payment, "order": serializer.data}
    return Response(data)


@api_view(["POST"])
def handlePaymentSuccess(request):
    res = json.loads(request.data["response"])
    print(res)

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == "razorpay_order_id":
            ord_id = res[key]
        elif key == "razorpay_payment_id":
            raz_pay_id = res[key]
        elif key == "razorpay_signature":
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_id=ord_id)

    data = {
        "razorpay_order_id": ord_id,
        "razorpay_payment_id": raz_pay_id,
        "razorpay_signature": raz_signature,
    }

    client = razorpay.Client(
        auth=("rzp_test_2ioyu4SMKC1Nvz", "PeMxgIjo29GSSXIsPYCtZaiS")
    )

    # client.payment.capture("razorpay_payment_id", )

    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({"error": "Something went wrong"})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {"message": "payment successfully received!"}

    return Response(res_data)
