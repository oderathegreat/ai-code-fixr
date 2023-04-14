from django.shortcuts import render, redirect
from django.contrib import messages
import openai


def home(request):
    # api-key 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
    lang_list = ['C++', 'Go', 'Java', 'JavaScript', 'Kotlin', 'PHP', 'Ruby', 'Rust', 'Swift', 'TypeScript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming languages":
            messages.success(request, "You forgot to pick programming langage")
            return render(request, "index.html", {'lang_list': lang_list, 'code': code, 'lang': lang})

        openai.api_key = "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"
        openai.Model.list()

        #make a request to api
        try:

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Respond Only With Code. Fix this {lang} code: {code}",
                temperature=0,
                max_tokens = 1000,
                top_p = 1.0,
                frequncy_penalty = 0.0,
                presence_panalty = 0.0

            )
        except Exception as e:



    # print(sorted(lang_list))
    return render(request, "index.html", {'lang_list': lang_list})
