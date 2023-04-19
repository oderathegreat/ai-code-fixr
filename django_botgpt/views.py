from django.shortcuts import render
from django.contrib import messages
import openai


def home(request):
    lang_list = ['C++', 'Go', 'Java', 'JavaScript', 'Kotlin', 'PHP', 'Ruby', 'Rust', 'Swift', 'TypeScript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming languages":
            messages.success(request, "You forgot to pick programming langage")
            return render(request, "index.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

        openai.api_key = "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"
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

        openai.api_key = "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"
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
