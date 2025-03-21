import bcrypt
from django.shortcuts import render,redirect
from django.contrib import messages
from Sav_Vintage_app.models import Cars,User,Purchases
# Create your views here.
def index(request):
    if 'userid' not in request.session:
        return redirect('login')
    userid=request.session.get('userid')
    user=User.objects.get(id=userid)
    cars=Cars.objects.all()
    context={
        'cars':cars,
        'username':user.first_name
    }
    return render(request,"index.html",context)

def viewOrders(request):
    if 'userid' not in request.session:
        return redirect('login')
    userid=request.session.get('userid')
    user=User.objects.get(id=userid)
    purchases=Purchases.objects.filter(buyer=user)
    context={
        'username':user.first_name,
        'purchases':purchases
    }
    return render(request,"orders.html",context)
def register(request):

    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        first_name=request.POST ['first_name']
        last_name=request.POST ['last_name']
        email=request.POST['email']
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
       
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
            return render(request,"register.html")
        else:
            user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)
            request.session['userid'] = user.id
        return redirect('success')


    return render(request,"register.html")
    
def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(),user.password.encode()):
                request.session['userid']=user.id
                request.session['first_name']=user.first_name
                return redirect('success')
            else:
                messages.error(request,"Try Again, The Password and Email doesn't match")
        except User.DoesNotExist:

            messages.error(request,"This Email is not assigned in our database")
    return render(request,"login.html")

def success(request):
    if 'userid' not in request.session:
        return redirect('login')

    userid = int(request.session.get('userid'))  # Ensure it's an integer
    user = User.objects.get(id=userid)  # Now define user first
    seller_cars = Cars.objects.filter(seller=user)  # Get all cars listed by the logged-in user
    all_cars = Cars.objects.all()  # Get all cars for displaying
    context = {
        'username': user.first_name,
        'userid': userid,
        'cars': all_cars,  # Pass all cars for display
        'seller_cars': seller_cars  # Pass only the logged-in user's cars
    }

    return render(request, "index.html", context)
def addCar(request):
    if 'userid' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        errors=Cars.objects.validator(request.POST)
        model = request.POST.get('model')
        maker=request.POST.get('maker')
        year = request.POST.get('year')
        price = request.POST.get('price')
        desc=request.POST.get('desc')
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
            return render(request,"addCar.html")
        else:
        #create an object
            userid=request.session.get('userid')
            seller=User.objects.get(id=userid)
            Cars.objects.create(model=model,maker=maker,year=year,price=price,desc=desc,seller=seller)
            return redirect('success')
    return render(request,"addCar.html")

def makePurchase(request,car_id):
    userid=request.session.get('userid')
    car=Cars.objects.get(id=car_id)
    buyer=User.objects.get(id=userid)
    
    if car.is_available:
        if request.method=="POST":
            purchase=Purchases.objects.create(car=car,buyer=buyer,price=car.price)
            car.is_available=False
            car.save()
            context={
                'purchases':purchase,
            }
        return redirect('viewOrders')
    return render(request,"viewOrders.html")

def details(request,id):
    car=Cars.objects.get(id=id)
    context={
        'car':car
    }
    return render(request,"carDetails.html",context)
def update(request,id):
    car=Cars.objects.get(id=id)
    if request.method=="POST":
        car.model=request.POST.get("model",car.model)
        car.maker=request.POST.get("maker",car.maker)
        car.year=request.POST.get("year",car.year)
        car.desc=request.POST.get("desc",car.desc)
        car.save()
        return redirect('details',id)
    context={
        'car':car
    }
    return render(request,"updateCar.html",context)
def cancelOrder(request,id):
    order=Purchases.objects.get(id=id)
    order.car.is_available=True
    order.car.save()
    order.delete()
    return redirect('success')
def cancelAdd(request):
    return redirect('success')

def deleteCar(request,id):
    car=Cars.objects.get(id=id)
    car.delete()
    return redirect('success')

def logout(request):
    request.session.flush() 
    return redirect('login')