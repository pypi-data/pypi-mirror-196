from transformers import AutoModelForCausalLM
from transformers import pipeline
from transformers import AutoTokenizer


class ruGPT3():

    def Answer(
         self, prompt, model_path, tokenizer_model,
         max_length=1024, max_new_tokens=1000,
         do_sample=True, top_k=50, top_p=0.95, num_beams=5,
         no_repeat_ngram_size=2,
         early_stopping=True, skip_special_tokens=True):

        """
Cгенерировать продолжение моделью для заданного текста
        Parameters
        ----------

        prompt: строка с текстом для генерации

        model_path: строка с путём к папке с файлами модели

        tokenizer_model:  строка с путём к папке с
файлами токенайзера для модели, может совпадать с полем model

        Для подробного разъяснения следующих параметров смотри:
        https://huggingface.co/docs/transformers/main_classes/text_generation

        max_length: целое число - максимальная длина ответа

        max_new_tokens: целое число - максимальное число новых токенов в ответе

        do_sample: булевский тип - использование или нет сэмплинга

        top_k: целое число - наибольшая вероятность
для токенов из словаря пройти через top-k фильтрацию

        top_p: нецелое число от 0 до 1 - если < 1,
то только наименьший набор токенов, с вероятностью не меньшей top_p,
будет использован для генерации

        num_beams: целое число - число "лучей" для beam_search

        no_repeat_ngram_size: целое число - если больше 0,
то ngrams данного размера будут входить всего раз

        early_stopping: булевский тип - останавливает beam_search,
если число готовых предложений хотя бы num_beams

        skip_special_tokens: булевский тип - пропуск служебных токенов

        Returns
        -------

        s1 : str
        строка - ответ от встроенного генератора

        s2 : str
        строка - ответ от встроенного генератора с дополнительными настройками:
max_new_tokens, do_sample, top_k, top_p

        s3 : str
        строка - ответ от встроенного генератора c дополнительными настройками:
        inptds,  max_length, num_beams, top_k, top_p,
no_repeat_ngram_size, early_stopping

        """
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(
                                                 tokenizer_model,
                                                 use_fast=True, Truncate=True)
        generator = pipeline("text-generation", model=model,
                             tokenizer=tokenizer, max_length=max_length)
        s1 = generator(prompt)

        inputs = tokenizer(prompt, return_tensors="pt").input_ids
        outputs = model.generate(
                                inputs, max_new_tokens=max_new_tokens,
                                do_sample=do_sample, top_k=top_k, top_p=top_p)

        s2 = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        inptds = tokenizer.encode(prompt, return_tensors='pt')
        output1 = model.generate(
                         inptds, max_length=max_length, num_beams=num_beams,
                         top_k=top_k, top_p=top_p,
                         no_repeat_ngram_size=no_repeat_ngram_size,
                         early_stopping=early_stopping)

        s3 = tokenizer.decode(
                             output1[0],
                             skip_special_tokens=skip_special_tokens)

        return s1, s2, s3
