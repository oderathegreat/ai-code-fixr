from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

import openai


def home(request):
    lang_list = ['C++', 'Go', 'Java', 'JavaScript', 'Kotlin', 'PHP', 'Ruby', 'Rust', 'Swift', 'TypeScript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming languages":
            messages.success(request, "You forgot to pick programming langage")
            return render(request, "index.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

        openai.api_key = "pass-api-key here"
        openai.Model.list()

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Respond Only With Code. Fix this {lang} code: {code}",
                temperature=0,
                max_tokens=1000,
                top_p=1.0,
                frequncy_penalty=0.0,
                presence_panalty=0.0
            )
            response = (response["choices"][0]["text"]).strip()

            # save code to database
            record_data = Code(question=code, code_answer=response, language=lang, user=request.user)
            record_data.save()

            return render(request, "index.html", {'lang_list': lang_list, 'response': response, 'lang': lang})

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "index.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

    return render(request, "index.html", {'lang_list': lang_list})


def suggest(request):
    lang_list = ['C++', 'Go', 'Java', 'JavaScript', 'Kotlin', 'PHP', 'Ruby', 'Rust', 'Swift', 'TypeScript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming languages":
            messages.success(request, "You forgot to pick programming langage")
            return render(request, "suggest.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

        openai.api_key = "pass-api-key"
        openai.Model.list()

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Respond Only With Code.{code}",
                temperature=0,
                max_tokens=1000,
                top_p=1.0,
                frequncy_penalty=0.0,
                presence_panalty=0.0
            )
            response = (response["choices"][0]["text"]).strip()

            record_data = Code(question=code, code_answer=response, language=lang, user=request.user)
            record_data.save()

            return render(request, "suggest.html", {'lang_list': lang_list, 'response': response, 'lang': lang})

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "suggest.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

    return render(request, "suggest.html", {'lang_list': lang_list})


def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect('/')
        else:
            messages.success(request, "Error in Loggin In. Please try again")
            return redirect('/')

    else:
        return render(request, "index.html", {})


def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged Out")
    return redirect('/')


def registerUser(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered successfully")
            return redirect("/")

    else:
        form = SignUpForm
    return render(request, "register.html", {"form": form})


def pastquest(request):
    if request.user.is_authenticated:
        # check specifi records belonging to an individual user
        user_codes = Code.objects.filter(user_id=request.user.id)
        return render(request, "pastquest.html", {"user_code":user_codes})

    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect("/")


def  delete_past(request, Past_id):
    past = Code.objects.get(pkid=Past_id)
    past.delete()
    messages.success(request, "Data deleted Successfully")
    return redirect("pastquest")
