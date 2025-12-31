from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from BidXpert_app import forms
from datetime import datetime
from django.contrib import messages
from . models import *
from . models import Product , ProductImage
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import Categories
from .forms import ProductForm
from .forms import ContactForm
from django.contrib import messages as django_messages
from .models import Product, Bid
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Product
import json
from django.utils import timezone
import razorpay


def hello(request):
    return HttpResponse("This Is Hello Page!!!")

def dashboard(request):
    User = get_user_model()
    all_users = User.objects.all()

    total_users = User.objects.count()
    total_auctions = Product.objects.count()
    live_auctions = Product.objects.filter(current_price__isnull=False).count()
    closed_auctions = Product.objects.filter(current_price__isnull=True).count()
    total_categories = Categories.objects.count()

    # Add total ended auctions (where end date is past and product is sold)
    total_ended_auctions = Product.objects.filter(end_date__lt=timezone.now(), is_sold=True).count()

    return render(request, 'dashboard.html', {
        'total_users': total_users,
        'total_auctions': total_auctions,
        'live_auctions': live_auctions,
        'closed_auctions': closed_auctions,
        'total_categories': total_categories,
        'total_ended_auctions': total_ended_auctions,
        'all_users': all_users,
    })




# ____________________________________      Contect Us      ____________________________________________

def contact_view(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            success = True

    return render(request, 'contact-us.html', {'success': success})


def admin_messages_view(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_messages.html', {'messages': messages})

def delete_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    django_messages.success(request, "Message deleted successfully.")
    return redirect('admin_messages')

# ____________________________________      Dashboard      ____________________________________________



def index(request):
    categories = Categories.objects.all()
    return render(request, 'index.html', {'categories': categories})


def category_products(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        'products': products,
        'category': category  # You can access category.name in the template
    })

def browse_categories(request):
    categories = Categories.objects.all()
    return render(request, 'browse_categories.html', {'categories': categories})


# ____________________________________      Profile      ____________________________________________

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        aadhar_number = request.POST.get('aadhar_number')

        # Update the user object
        user.username = username
        user.email = email
        user.contact_number = contact_number
        user.address = address
        user.aadhar_number = aadhar_number

        # Handle profile image update
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        # Save the updated user
        user.save()

        # Show success message
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Use the name of your URL route

    return render(request, "profile.html", {'user': user})

# ____________________________________       Login & Register       ____________________________________________

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm  # Import your custom user form
from .models import CustomUser  # Import your custom user model

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser  # Assuming CustomUser is your custom user model

def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        aadhar_number = request.POST.get('aadhar_number')
        profile_image = request.FILES.get('profile_image')

        if password == password1:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                # Create the user and set is_staff=True to mark as admin
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    contact_number=contact_number,
                    address=address,
                    aadhar_number=aadhar_number,
                    profile_image=profile_image
                )
                user.is_staff = True  # Mark as admin
                user.save()

                # Log the admin user in after registration
                login(request, user)

                messages.success(request, "Admin registered successfully!")

                # Authenticate the user and check if they are an admin
                user = authenticate(request, username=username, password=password)
                if user is not None and user.is_staff:
                    return redirect('index')  # Redirect to the admin dashboard
                else:
                    return redirect('login')  # Redirect to the login page if not an admin
        else:
            messages.error(request, "Passwords do not match!")
    return render(request, 'register_admin.html')







def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        aadhar_number = request.POST.get('aadhar_number')
        profile_image = request.FILES.get('profile_image')

        if password == password1:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    contact_number=contact_number,
                    address=address,
                    aadhar_number=aadhar_number,
                    profile_image=profile_image
                )
                messages.success(request, "You are registered successfully!")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You logged in successfully!")

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "👋 Logged out successfully!")
    return redirect('login')

# ______________________________________________________________USER SIDE___________________________________________________________________________

def contact_us(request):
    return render(request,"contact-us.html")

def about_us(request):
    return render(request,"about-us.html")

def dash(request):
    return render(request,"dash.html")

def product_list(request):
    products = Product.objects.filter(is_sold=False)
    return render(request, 'dash.html', {'products': products})

from django.utils import timezone

def declare_winner(product, highest_bid):
    current_date = timezone.now()

    if not product.end_date:
        print("No end date set for product.")
        return

    if product.end_date < current_date and not product.winner:
        if highest_bid:
            product.winner = highest_bid  # ✅ assign the Bid object
            product.is_sold = True
            product.save()
            print(f"Winner for product {product.product} is {highest_bid.user}")
        else:
            print(f"No bids placed for product {product.product}")
    else:
        print("Time for auction is not over yet or winner already declared.")




    
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Product, Bid
from django.conf import settings

@login_required
def bid_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print("price............",product.current_price)
    if product.winner:
        amount = int(product.winner.amount * 100)  # Razorpay needs amount in paise (₹100.00 = 10000)
    else:
        amount = 0
    print("amount",amount)

    # Fetch all previous bids for this product, ordered by newest first
    bids = Bid.objects.filter(product=product).select_related('user').order_by('-timestamp')
    
    # Find the highest bid (the bid with the highest amount)
    highest_bid = bids.first() if bids else None

    # Call declare_winner only if end_date exists and auction is over
    if product.end_date and timezone.now() > product.end_date:
        declare_winner(product, highest_bid)

    # Pass current time to template for comparison
    now = timezone.now()
    context = {
        "amount": amount,
        # 'payment': payment,
        'api_key': settings.RAZORPAY_KEY_ID,
        'amount_display': amount / 100,
        'product': product,
        'pd': product,
        'bids': bids,
        'highest_bid': highest_bid,
        'now': now,
    }
    return render(request, 'bid-view.html',context)



# ______________________________________________________________ADMIN SIDE___________________________________________________________________________

# ------------------------- PRODUCT CRUD --------------------------------------------------  

def product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # Set category manually
            category_id = request.POST.get("category")
            if category_id:
                try:
                    product.category = Categories.objects.get(id=category_id)
                except Categories.DoesNotExist:
                    product.category = None

            # ✅ Set end_date manually (if not handled by ModelForm)
            end_date_str = request.POST.get("end_date")
            if end_date_str:
                from datetime import datetime
                try:
                    product.end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")  # HTML datetime-local format
                except ValueError:
                    messages.error(request, "❌ Invalid date format for End Date.")
                    return redirect("product")

            product.save()

            # Save multiple images
            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            # Store dynamic fields
            product.extra_fields = {
                "date": request.POST.get("date", ""),
                "time": request.POST.get("time", ""),
                "amount": request.POST.get("amount", ""),
                "starting_price": request.POST.get("starting_price", ""),
                "end_date": end_date_str  # Store here too if needed
            }
            product.save()

            messages.success(request, "✅ Product Added Successfully!")
            return redirect("product_view")
        else:
            messages.error(request, "❌ Failed to Add Product. Please check the form.")
            print(form.errors)
    else:
        form = ProductForm()

    cate = Categories.objects.all()
    return render(request, "products.html", {"form": form, "cate": cate})




from datetime import datetime

def product_view(request):
    # Prefetch related images to reduce DB queries
    data = Product.objects.prefetch_related('images').all()

    for product in data:
        # Format time in extra_fields
        if product.extra_fields and "time" in product.extra_fields:
            try:
                product.extra_fields["time"] = datetime.strptime(
                    product.extra_fields["time"], "%H:%M"
                ).strftime("%I:%M %p")
            except ValueError:
                pass

        # Format end_date (e.g., "May 28, 2025 at 3:30 PM")
        if product.end_date:
            product.formatted_end_date = product.end_date.strftime("%b %d, %Y at %I:%M %p")
        else:
            product.formatted_end_date = "N/A"

    return render(request, 'products-view.html', {'data': data})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductImage, Categories
from .forms import ProductForm

def productupdate(request, id):
    data = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            product = form.save(commit=False)

            # Update extra_fields
            extra_fields = product.extra_fields or {}
            extra_fields.update({
                "date": request.POST.get("date", extra_fields.get("date", "")),
                "time": request.POST.get("time", extra_fields.get("time", "")),
                "amount": request.POST.get("amount", extra_fields.get("amount", "")),
                "starting_price": request.POST.get("starting_price", extra_fields.get("starting_price", "")),
            })
            product.extra_fields = extra_fields

            # Update end_date field directly from form
            end_date_str = request.POST.get("end_date")
            if end_date_str:
                try:
                    from datetime import datetime
                    product.end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")  # datetime-local input
                except ValueError:
                    messages.error(request, "❌ Invalid end date format.")

            product.save()

            # Handle image uploads
            images = request.FILES.getlist("images")
            if images:
                for img in images:
                    ProductImage.objects.create(product=product, image=img)

            # Handle image deletions
            if 'delete_images' in request.POST:
                delete_image_ids = request.POST.getlist('delete_images')
                ProductImage.objects.filter(id__in=delete_image_ids).delete()

            messages.success(request, "✅ Product Updated Successfully!")
            return redirect("product_view")
        else:
            messages.error(request, "❌ Failed to update product.")
    else:
        form = ProductForm(instance=data)

    return render(request, "products-edit.html", {
        "form": form,
        "data": data,
        "cate": Categories.objects.all(),
    })
    
    
def productdelete(request, id):
    product = get_object_or_404(Product, id=id)
    ProductImage.objects.filter(product=product).delete()  # Delete related images
    product.delete()  # Delete the product
    messages.success(request, "🗑️ Product deleted successfully.")
    return redirect("product_view")

def delete_product_image(request, id):
    image = get_object_or_404(ProductImage, id=id)
    product_id = image.product.id
    image.delete()  # Delete the image
    return redirect('productupdate', id=product_id)

# ------------------------- CATAGORIES CRUD --------------------------------------------------  

def category(request):
    if request.method == "POST":
        form = forms.CategoryForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added Successfully")  # ✅ Success Message
            return redirect('category')  # Redirect after success
        else:
            messages.error(request, "Failed to add category. Please correct the errors.")  # ✅ Error Message
            print(form.errors)  # Debugging purposes

    else:
        form = forms.CategoryForm()

    return render(request, 'categories.html', {'form': form})  # Pass form to template

def categories_view(request):
    data = Categories.objects.all()
    return render(request,'categories-view.html',{'data':data})

def categoriesupdate(request, id):
    # Get the category to update
    category = get_object_or_404(Categories, id=id)

    if request.method == "POST":
        # Create the form instance and bind it to the POST data
        form = forms.CategoryForm(request.POST, request.FILES, instance=category)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('categories_view')  # Redirect to the categories list view
        else:
            print(form.errors)  # Debugging purposes

    else:
        # If GET request, just create the form with the existing category data
        form = forms.CategoryForm(instance=category)

    context = {
        'form': form,  # Pass the form to the template
        'category': category  # Pass the category to the template (if you need to display it explicitly)
    }
    
    return render(request, 'categories-edit.html', context)

def categoriesdelete(request,id):
    data = Categories.objects.get(id=id)
    data.delete()
    return redirect(categories_view)

# ------------------------- BIDS CRUD --------------------------------------------------  

from django.utils import timezone
from django.shortcuts import render
from .models import Product, Bid

def bids(request):
    
    search_query = request.GET.get('search', '')
    
    if search_query:
        products = Product.objects.filter(product__icontains=search_query)
    else:
        products = Product.objects.all()
    
    products_with_bids = []
    now = timezone.now()

    for product in products:
        bids_qs = Bid.objects.filter(product=product, is_deleted=False).select_related('user').order_by('-amount', '-timestamp')
        highest_bid = bids_qs.first() if bids_qs.exists() else None

        products_with_bids.append({
            'product': product,
            'bids': bids_qs,
            'highest_bid': highest_bid,
        })

    return render(request, 'bids.html', {
        'products_with_bids': products_with_bids,
        'now': now,
    })




# ------------------------- USERS CRUD --------------------------------------------------  

def users(request):
    all_users = CustomUser.objects.filter(is_superuser=False)  # Fetch all registered users
    print(all_users)
    return render(request, 'users.html', {'users': all_users})


# ------------------------- Bids CRUD -------------------------------------------------- 

@csrf_protect
@require_POST
@login_required
def place_bid_ajax(request, product_id):
    try:
        data = json.loads(request.body)
        bid_amount = float(data.get("bid_amount"))
        product = get_object_or_404(Product, pk=product_id)

        current_price = float(product.current_price or product.starting_price)

        if bid_amount <= current_price:
            return JsonResponse({'success': False, 'error': 'Bid must be higher than current price.'})

        # Save the bid
        Bid.objects.create(product=product, user=request.user, amount=bid_amount)
        product.current_price = bid_amount
        product.save()

        return JsonResponse({'success': True, 'new_price': bid_amount})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Bid

@login_required
def user_bids_view(request):
    bids = Bid.objects.filter(user=request.user).select_related('product').order_by('-timestamp')
    current_time = timezone.now()

    # Attach status to each bid
    for bid in bids:
        product = bid.product
        highest_bid = product.bid_set.order_by('-amount').first()

        if product.end_date and product.end_date < current_time:
            if product.winner and product.winner == highest_bid:
                if highest_bid.user == request.user:
                    bid.status = "Winner"
                else:
                    bid.status = "Lost"
            else:
                bid.status = "Ended"
        else:
            bid.status = "Pending"

    return render(request, 'user_bids.html', {'bids': bids})


# ------------------------- PAYMENT -------------------------------------------------- 


import razorpay
from django.conf import settings
from django.shortcuts import render
from .models import Product  # import your Product model
from django.shortcuts import get_object_or_404

RAZORPAY_KEY_ID = "rzp_test_WzJxp1mLRafTnC"
RAZORPAY_KEY_SECRET = "nLWMbfmcNBodcmApXRPEOxIv"

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    amount = int(product.price * 100)  # Razorpay needs amount in paise (₹100.00 = 10000)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
        "receipt": f"order_rcptid_{product.id}"
    })

    context = {
        "amount": amount,
        'payment': payment,
        'api_key': settings.RAZORPAY_KEY_ID,
        'amount_display': amount / 100,
        'product': product,
    }

    return render(request, 'pay.html', context)


# ------------------------- END AUCTION --------------------------------------------------

from django.utils import timezone
from django.shortcuts import render
from .models import Product, Bid

def ended_auctions_view(request):
    now = timezone.now()

    # ✅ Only include auctions that ended AND have a declared winner
    ended_products = Product.objects.filter(
        end_date__lt=now,
        winner__isnull=False
    ).order_by('-end_date')

    # Preload bids for optimization
    product_ids = ended_products.values_list('id', flat=True)
    all_bids = Bid.objects.filter(product_id__in=product_ids).select_related('user', 'product')

    # Group bids by product
    bid_map = {}
    for bid in all_bids:
        bid_map.setdefault(bid.product_id, []).append(bid)

    products_with_bids = []
    for product in ended_products:
        bids = sorted(bid_map.get(product.id, []), key=lambda b: b.amount, reverse=True)
        highest_bid = bids[0] if bids else None

        products_with_bids.append({
            'product': product,
            'bids': bids,
            'highest_bid': highest_bid,
        })

    return render(request, 'ended_auctions.html', {
        'products_with_bids': products_with_bids,
        'now': now
    })

 