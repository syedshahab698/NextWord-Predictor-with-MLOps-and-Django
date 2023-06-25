from django.shortcuts import render
from .models import InputText
from .predict import predict_next_word

def home(request):
    return render(request, 'index.html')


def word_pred(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        predicted_word = predict_next_word(input_text)
        InputText.objects.create(text=input_text)
    else:
        predicted_word = ''

    return render(request, 'word_prediction_tool.html', {'predicted_word': predicted_word})


# def word_pred(request):
#     return render(request, 'word_prediction_tool.html')

# def word_pred(request):
#     return render(request, 'word_prediction_tool.html')
