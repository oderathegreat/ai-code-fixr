from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

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

