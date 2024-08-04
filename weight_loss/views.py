from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import weightlist
from .forms import weightchart
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from datetime import datetime




# HOME PAGE

def homepage(request):
    return render(request,'homepage.html')





# SIGNUP PAGE

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



# LOGIN PAGE



def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
           
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# for mark the weight

@login_required(login_url='home')
def mark_the_weight(request):
    # Get the current logged-in user
    current_user = request.user
    
    # Check if the request method is POST
    if request.method == 'POST':
        form = weightchart(request.POST)
        if form.is_valid():
            # Check if the user has already added their weight
            if weightlist.objects.filter(user=current_user, dateOfMarking =timezone.now().date()).exists():
                
                # If the user has already added the weight, show an error message
                error_message = "You have already added your weight today"
                return render(request, 'weightchart.html', {'form': form, 'error_message': error_message})
            
            # If the user has not added the weight, save the weight
            new_user = form.save(commit=False)
            new_user.user = current_user
            new_user.save()
            return redirect('listview')
    else:
        form = weightchart()
    return render(request, 'weightchart.html', {'form': form})



# LIST VIEW


def listing(request):
    product_list = weightlist.objects.all()
    paginator = Paginator(product_list,3)  # Set the number of items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'page_view.html', {'page_obj': page_obj})




# EDIT WEIGHT DATA


def edit_datas(request, id):
    product = weightlist.objects.get(pk=id)
    if request.method == 'POST':
        form = weightchart(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form =weightchart(instance=product)           
    return render(request, 'edit.html', {'form': form})





# DELETE THE DATA FROM LIST



@login_required(login_url='home')

def delete_data(request,pk):
    product=weightlist.objects.get(pk=pk)  
    if request.method == 'POST':
        product.delete()
        return redirect('listview')
    
    return render(request,'page_view.html',{'product':product})







# LOGOUT PAGE



@login_required(login_url='home')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)






# TO FIND THE WEIGHT LOSS 




def compare_weights(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        user = request.user
        
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')

        # Convert date strings to datetime objects
        date1 = datetime.strptime(date1, '%Y-%m-%d').date()
        date2 = datetime.strptime(date2, '%Y-%m-%d').date()

        # Retrieve weight entries for the selected dates and the logged-in user
        weight1 = weightlist.objects.filter(user=user, dateOfMarking=date1).first()
        weight2 = weightlist.objects.filter(user=user, dateOfMarking=date2).first()

        if not weight1 or not weight2:
            return JsonResponse({'error': 'Weight entry not found for one or both selected dates'})

        # Extract weights
        weight1_value = weight1.weight
        weight2_value = weight2.weight

        # Compare the weights
        comparison_result = 'Weight increased' if weight1_value < weight2_value else 'Weight decreased' if weight1_value > weight2_value else 'Weight unchanged'

        return JsonResponse({
            'weight1': weight1_value,
            'weight2': weight2_value,
            'date1': date1.strftime('%Y-%m-%d'),
            'date2': date2.strftime('%Y-%m-%d'),
            'comparison_result': comparison_result
        })

    return JsonResponse({'error': 'Invalid request'})