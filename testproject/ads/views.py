from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return render(request, '403.html', {'message': 'Нельзя редактировать чужие объявления'}, status=403)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user == request.user:
        ad.delete()
        return redirect('ad_list')
    return render(request, '403.html', {'message': 'Нельзя удалять чужие объявления'}, status=403)

def ad_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all()

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category__iexact=category)
    if condition:
        ads = ads.filter(condition__iexact=condition)

    paginator = Paginator(ads, 10)
    page = request.GET.get('page')
    ads = paginator.get_page(page)

    return render(request, 'ads/ad_list.html', {'ads': ads})

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def create_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)

    if ad_receiver.user == request.user:
        return render(request, '403.html', {'message': 'Нельзя обмениваться с самим собой'}, status=403)

    if request.method == 'POST':
        form = ProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.save()
            return redirect('proposal_list')
    else:
        form = ProposalForm(user=request.user)

    return render(request, 'ads/proposal_form.html', {'form': form, 'ad_receiver': ad_receiver})

@login_required
def update_proposal_status(request, proposal_id, new_status):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    
    if proposal.ad_receiver.user != request.user:
        return render(request, '403.html', {'message': 'Вы не являетесь получателем предложения'}, status=403)

    if new_status in ['accepted', 'rejected']:
        proposal.status = new_status
        proposal.save()
    return redirect('proposal_list')

@login_required
def proposal_list(request):

    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')

    proposals = ExchangeProposal.objects.all().order_by('-created_at')

    if sender:
        proposals = proposals.filter(ad_sender__user=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__user=receiver)
    if status:
        proposals = proposals.filter(status__iexact=status)

    paginator = Paginator(proposals, 10)
    page = request.GET.get('page')
    proposals = paginator.get_page(page)

    return render(request, 'ads/proposal_list.html', {'proposals': proposals})