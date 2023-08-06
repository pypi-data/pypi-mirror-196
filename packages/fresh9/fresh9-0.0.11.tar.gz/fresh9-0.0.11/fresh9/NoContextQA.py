from transformers import pipeline
from transformers import AutoTokenizer
import torch
import tensorflow as tf
from transformers import TFAutoModelForQuestionAnswering
from transformers import T5ForConditionalGeneration, T5Tokenizer




class GenT5():
	def Answer(self,question, model_path, tokenizer_model, cuda = True):
		"""Cгенерировать ответ моделью для заданного вопроса
			Parameters
			----------
			
			question: строка с вопросом для ответа
		model_path: строка с путём к папке с файлами модели
		tokenizer_model:  строка с путём к папке с файлами токенайзера для модели,
			может совпадать с полем model
		cuda: булевский тип, вычислять ответ с использованием GPU или без (False)
				
			Returns 
			-------
			
			answer(question) : str
				строка - ответ от встроенного генератора

		
			
		"""	
		tokenizer = T5Tokenizer.from_pretrained(tokenizer_model)
		if(cuda == True):
			model = T5ForConditionalGeneration.from_pretrained(model_path).cuda();
			
		if(cuda == False):
			model = T5ForConditionalGeneration.from_pretrained(model_path)
			
		def answer(x, **kwargs):
			inputs = tokenizer(x, return_tensors='pt').to(model.device) 
			with torch.no_grad():
				hypotheses = model.generate(**inputs, **kwargs)
			return tokenizer.decode(hypotheses[0], skip_special_tokens=True)
		return answer(question)
		

	