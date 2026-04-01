import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Product, Warehouse, StockMovement


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['product_count'] = Product.objects.count()
    ctx['product_in_stock'] = Product.objects.filter(status='in_stock').count()
    ctx['product_low_stock'] = Product.objects.filter(status='low_stock').count()
    ctx['product_out_of_stock'] = Product.objects.filter(status='out_of_stock').count()
    ctx['product_total_unit_price'] = Product.objects.aggregate(t=Sum('unit_price'))['t'] or 0
    ctx['warehouse_count'] = Warehouse.objects.count()
    ctx['warehouse_active'] = Warehouse.objects.filter(status='active').count()
    ctx['warehouse_maintenance'] = Warehouse.objects.filter(status='maintenance').count()
    ctx['warehouse_closed'] = Warehouse.objects.filter(status='closed').count()
    ctx['warehouse_total_utilization'] = Warehouse.objects.aggregate(t=Sum('utilization'))['t'] or 0
    ctx['stockmovement_count'] = StockMovement.objects.count()
    ctx['stockmovement_in'] = StockMovement.objects.filter(movement_type='in').count()
    ctx['stockmovement_out'] = StockMovement.objects.filter(movement_type='out').count()
    ctx['stockmovement_transfer'] = StockMovement.objects.filter(movement_type='transfer').count()
    ctx['recent'] = Product.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def product_list(request):
    qs = Product.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'product_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def product_create(request):
    if request.method == 'POST':
        obj = Product()
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.category = request.POST.get('category', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.reorder_level = request.POST.get('reorder_level') or 0
        obj.unit_price = request.POST.get('unit_price') or 0
        obj.cost_price = request.POST.get('cost_price') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/products/')
    return render(request, 'product_form.html', {'editing': False})


@login_required
def product_edit(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.category = request.POST.get('category', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.reorder_level = request.POST.get('reorder_level') or 0
        obj.unit_price = request.POST.get('unit_price') or 0
        obj.cost_price = request.POST.get('cost_price') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/products/')
    return render(request, 'product_form.html', {'record': obj, 'editing': True})


@login_required
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/products/')


@login_required
def warehouse_list(request):
    qs = Warehouse.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'warehouse_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def warehouse_create(request):
    if request.method == 'POST':
        obj = Warehouse()
        obj.name = request.POST.get('name', '')
        obj.location = request.POST.get('location', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.utilization = request.POST.get('utilization') or 0
        obj.manager = request.POST.get('manager', '')
        obj.status = request.POST.get('status', '')
        obj.contact = request.POST.get('contact', '')
        obj.save()
        return redirect('/warehouses/')
    return render(request, 'warehouse_form.html', {'editing': False})


@login_required
def warehouse_edit(request, pk):
    obj = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.location = request.POST.get('location', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.utilization = request.POST.get('utilization') or 0
        obj.manager = request.POST.get('manager', '')
        obj.status = request.POST.get('status', '')
        obj.contact = request.POST.get('contact', '')
        obj.save()
        return redirect('/warehouses/')
    return render(request, 'warehouse_form.html', {'record': obj, 'editing': True})


@login_required
def warehouse_delete(request, pk):
    obj = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/warehouses/')


@login_required
def stockmovement_list(request):
    qs = StockMovement.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(product_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(movement_type=status_filter)
    return render(request, 'stockmovement_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def stockmovement_create(request):
    if request.method == 'POST':
        obj = StockMovement()
        obj.product_name = request.POST.get('product_name', '')
        obj.warehouse = request.POST.get('warehouse', '')
        obj.movement_type = request.POST.get('movement_type', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.reference = request.POST.get('reference', '')
        obj.date = request.POST.get('date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/stockmovements/')
    return render(request, 'stockmovement_form.html', {'editing': False})


@login_required
def stockmovement_edit(request, pk):
    obj = get_object_or_404(StockMovement, pk=pk)
    if request.method == 'POST':
        obj.product_name = request.POST.get('product_name', '')
        obj.warehouse = request.POST.get('warehouse', '')
        obj.movement_type = request.POST.get('movement_type', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.reference = request.POST.get('reference', '')
        obj.date = request.POST.get('date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/stockmovements/')
    return render(request, 'stockmovement_form.html', {'record': obj, 'editing': True})


@login_required
def stockmovement_delete(request, pk):
    obj = get_object_or_404(StockMovement, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/stockmovements/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['product_count'] = Product.objects.count()
    data['warehouse_count'] = Warehouse.objects.count()
    data['stockmovement_count'] = StockMovement.objects.count()
    return JsonResponse(data)
