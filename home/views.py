from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator
from django.db import connections, connection   
# from django.dispatch import Signal
# from django.core.signals import Signal


# Create your views here.

def project(request):
    if request.user.is_anonymous:
        return redirect("/login")
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM globalinventory")
        rows = cursor.fetchall()
    paginator = Paginator(rows, 12)  # split rows into 12 rows per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Project.html", {'page_obj': page_obj})



# def blueCard(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT COUNT(*) FROM globalinventory")
#         row_count = cursor.fetchone()[0]
#     return render(request, 'Project.html', {'row_count': row_count})


def my_stock(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM myapp_mystock")
        row_count = cursor.fetchone()[0]
    context = {'row_count': row_count}
    return render(request, 'Project.html', context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check if the user has entered correct credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("/")
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect("/login")



# def contactUs(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')

#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO contact_us (first_name, last_name, email, phone, message) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, phone, message))
#         connection.commit()

#         return HttpResponse('Form submitted successfully')
#     else:
#         return render(request, 'contactus.html')



def contactUs(request):
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        with connections['default'].cursor() as cursor:
            # Save the data to the contactus table
            cursor.execute('INSERT INTO contactus (first_name, last_name, email, phone, message) VALUES (%s, %s, %s, %s, %s)',
                            [first_name, last_name, email, phone, message])
        
        # Display a success message and redirect to the home page
        return redirect('home')
    
    # If the request method is not POST, display the contact form
    return render(request, 'contactus.html')


def myStock(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM mystock")
        rows = cursor.fetchall()
    return render(request, 'mystock.html', {'rows': rows})



def searchStock(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        if search_query is not None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM mystock WHERE name LIKE %s OR description LIKE %s", ['%' + search_query + '%', '%' + search_query + '%'])
                rows = cursor.fetchall()
                return render(request, 'mystock.html', {'rows': rows})
    return render(request, 'mystock.html')


def medicineShortage(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM globalinventory WHERE quantity <20 order by quantity asc")
        rows =  cursor.fetchall()
    return render(request, 'medshortage.html', {'rows': rows})


def searchGlobal(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        if search_query is not None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM globalinventory WHERE name LIKE %s OR description LIKE %s", ['%' + search_query + '%', '%' + search_query + '%'])
                rows = cursor.fetchall()
                return render(request, 'globalinventory.html', {'rows': rows})
    return render(request, 'globalinventory.html')


def searchHome(request):
    if request.method == 'GET':
        search_query = request.GET.get('Search_bar', None)
        if search_query is not None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM globalinventory WHERE name LIKE %s OR description LIKE %s", ['%' + search_query + '%', '%' + search_query + '%'])
                rows = cursor.fetchall()
                return render(request, 'Project.html', {'page_obj': rows})
    return render(request, 'Project.html')

def regularNeeds(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM globalinventory where quantity >80")
        rows =cursor.fetchall()
    return render(request, 'regularneeds.html', {'rows': rows})

def globalInventory(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM globalinventory")
        rows = cursor.fetchall()
    return render(request,'globalinventory.html', {'rows': rows})




def add_to_mystock(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        # check if the item already exists in mystock
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, quantity FROM mystock WHERE id = %s', [id])
            row = cursor.fetchone()
        
        if row is None:
            # insert the item into mystock with quantity 1
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO mystock (id, name, description, price, quantity) SELECT id, name, description, price, 1 FROM globalinventory WHERE id = %s', [id])
        else:
            # increment the quantity of the existing item in mystock
            with connection.cursor() as cursor:
                cursor.execute('UPDATE mystock SET quantity = quantity + 1 WHERE id = %s', [id])
        
        return redirect('/globalinventory')
        
    # if the request method is not POST, render the template
    return render(request, 'mystock.html')



def add_stock_ms(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        # check if the item already exists in mystock
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, quantity FROM mystock WHERE id = %s', [id])
            row = cursor.fetchone()
        
        if row is None:
            # insert the item into mystock with quantity 1
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO mystock (id, name, description, price, quantity) SELECT id, name, description, price, 1 FROM globalinventory WHERE id = %s', [id])
        else:
            # increment the quantity of the existing item in mystock
            with connection.cursor() as cursor:
                cursor.execute('UPDATE mystock SET quantity = quantity + 1 WHERE id = %s', [id])
        
        return redirect('/medshortage')
        
    # if the request method is not POST, render the template
    return render(request, 'mystock.html')


def remove_mystock(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        # check if the item already exists in mystock
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, quantity FROM mystock WHERE id = %s', [id])
            row = cursor.fetchone()
        
        if row is None:
            # insert the item into mystock with quantity 1
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO mystock (id, name, description, price, quantity) SELECT id, name, description, price, 1 FROM globalinventory WHERE id = %s', [id])
        else:
            # decrement the quantity of the existing item in mystock
            with connection.cursor() as cursor:
                cursor.execute('UPDATE mystock SET quantity = quantity - 1 WHERE id = %s', [id])
            
            # if the quantity becomes 0, delete the row
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM mystock WHERE id = %s AND quantity = 0', [id])
        
        return redirect('/mystock')
        
    # if the request method is not POST, render the template
    return render(request, 'mystock.html')





def logoutUserOnServerStop(sender, **kwargs):
    logout(request=None)

# # Create the Signal object
# server_stopped = Signal()

# # Connect the signal to the logoutUserOnServerStop function
# server_stopped.connect(logoutUserOnServerStop)











# from django.shortcuts import render
# from django.db import connections

# def add_to_stock(request, id):
#     with connections['your_database_alias'].cursor() as cursor:
#         # Get the item from the globalinventory table
#         cursor.execute('SELECT * FROM globalinventory WHERE id = %s', [id])
#         item = cursor.fetchone()

#         # Check if the item is already in the mystock table
#         cursor.execute('SELECT * FROM mystock WHERE id = %s', [id])
#         existing_item = cursor.fetchone()

#         if existing_item:
#             # Update the quantity if the item is already in mystock
#             new_quantity = existing_item[2] + 1
#             cursor.execute('UPDATE mystock SET quantity = %s WHERE id = %s', [new_quantity, id])
#         else:
#             # Insert the item into mystock with a quantity of 1
#             cursor.execute('INSERT INTO mystock (id, name, quantity) VALUES (%s, %s, 1)', [item[0], item[1]])

#     return render(request, 'globalinventory.html', {'message': 'Item added to mystock'})
