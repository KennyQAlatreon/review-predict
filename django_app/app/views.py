from django.shortcuts import render
from model.model_prediction import *


def index(request):
  return render(request, 'app/index.html')

def review_evaluation(request):
  text_origin = request.POST.get('textarea-review')
  vectors_bag = get_vectors(text_origin)
  predictions = get_machine_prediction(vectors_bag)
  score = count_score(predictions)
  context = {'not_index': True,
             'review': text_origin,
             'score': score}
  return render(request, 'app/review_evaluation.html', context)