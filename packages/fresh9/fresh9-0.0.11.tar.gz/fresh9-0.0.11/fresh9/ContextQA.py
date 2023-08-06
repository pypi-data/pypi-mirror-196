from transformers import pipeline
from transformers import AutoTokenizer
import torch
import tensorflow as tf
from transformers import TFAutoModelForQuestionAnswering




class RuRoberta():
	def Answer(self,question, context, model_path, tokenizer_model):
		"""Сгенерировать ответ моделью для заданных вопроса и контекста, с заданным токенайзером
			
			Parameters
			----------
			
			question: строка с вопросом для ответа
		 context: строка с контекстом для ответа
		 model_path: строка с путём к папке с файлами модели
		 tokenizer_model:  строка с путём к папке с файлами токенайзера для модели,
			может совпадать с полем model
				
			Returns 
			-------
			
			basic_ans['answer'] : str
				строка - ответ от встроенного генератора
		TF_ans : str
			строка - ответ от генератора от TensorFlow
		
			
		"""	
		tokenizer = AutoTokenizer.from_pretrained(tokenizer_model, use_fast=True, Truncate = True)
		inputs = tokenizer(question, context, return_tensors="pt")
		question_answerer = pipeline("question-answering", model=(model_path))
		basic_ans = question_answerer(question=question, context=context)
		
		inputs = tokenizer(question, context, return_tensors="tf")
		model = TFAutoModelForQuestionAnswering.from_pretrained(model_path, from_pt=True)
		outputs = model(**inputs)
		answer_start_index = int(tf.math.argmax(outputs.start_logits, axis=-1)[0])
		answer_end_index = int(tf.math.argmax(outputs.end_logits, axis=-1)[0])
		predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
		TF_ans = tokenizer.decode(predict_answer_tokens)
		
		return basic_ans['answer'], TF_ans