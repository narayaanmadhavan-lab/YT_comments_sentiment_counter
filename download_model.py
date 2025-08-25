from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "cardiffnlp/twitter-roberta-base-sentiment"

# Downloads and caches the model/tokenizer locally
AutoModelForSequenceClassification.from_pretrained(model_name)
AutoTokenizer.from_pretrained(model_name)
