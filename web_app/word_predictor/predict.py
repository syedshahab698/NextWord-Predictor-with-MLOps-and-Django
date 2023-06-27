import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

import os
from django.conf import settings

tokenizer = pickle.load(open(os.path.join(settings.BASE_DIR, 'ml/tokenizer.pkl'), 'rb'))
new_model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'ml','bilstm_nwp'))



max_sequence_len = 40
def predict_next_word(input_text):

    next_words = 5

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([input_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    #     predicted = model.predict_classes(token_list, verbose=0)
        predict_x=new_model.predict(token_list, verbose = 0) 
        predicted=np.argmax(predict_x,axis=1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        input_text += " " + output_word
    return(input_text)

# def predict_next_word(input_text):

#     input_text = 'Data science is field of'
#     token_list = tokenizer.texts_to_sequences([input_text])[0]
#     token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
#     #     predicted = model.predict_classes(token_list, verbose=0)
#     predict_x=new_model.predict(token_list, verbose = 0) 
#     predict_x = predict_x.reshape(-1)

#     sorted_indices = np.argsort(predict_x)[::-1]

#     # Get the top 10 values and their indices
#     top_5_score = predict_x[sorted_indices[:5]]
#     top_5_indices = sorted_indices[:5]

#     def get_word_for_index(pred_index):
#         for word, index in tokenizer.word_index.items():
#             if pred_index == index:
#                 return word
        
#     top_5_words = [get_word_for_index(i) for i in top_5_indices ]
#     return top_5_words, top_5_score