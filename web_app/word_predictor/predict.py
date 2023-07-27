import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from django.http import JsonResponse
import json
import os
from django.conf import settings

tokenizer = pickle.load(open(os.path.join(settings.BASE_DIR, 'ml/tokenizer.pkl'), 'rb'))
new_model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'ml', 'bilstm_nwp'))

max_sequence_len = 40

def predict_next_word(request):
    if request.method == "POST":
        gg = json.loads(request.body)
        print(gg)
        input_text = gg.get("text", "")
        print("Starting text:", input_text)

        token_list = tokenizer.texts_to_sequences([input_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')

        predict_x = new_model.predict(token_list, verbose=0)
        predict_x = predict_x.reshape(-1)

        sorted_indices = np.argsort(predict_x)[::-1]

        # Get the top 5 values and their indices
        top_5_score = predict_x[sorted_indices[:5]]
        top_5_indices = sorted_indices[:5]

        def get_word_for_index(pred_index):
            for word, index in tokenizer.word_index.items():
                if pred_index == index:
                    return word

        top_5_words = [get_word_for_index(i) for i in top_5_indices]
        top_5_scores = [float(predict_x[i]) for i in top_5_indices]  # Convert scores to float

        # Combine words and scores into a dictionary
        predictions = [{'word': word, 'score': score} for word, score in zip(top_5_words, top_5_scores)]

        return JsonResponse({'predictions': predictions})

