from django.shortcuts import render
# import requests
#
# # Create your views here.
# def createAuction(request, pk):
#     # if this is a POST request we need to process the form data
#     car = Car.objects.get(pk=pk)
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = AuctionForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             new_auc = Auction(car=car, **form.cleaned_data, manager=request.user)
