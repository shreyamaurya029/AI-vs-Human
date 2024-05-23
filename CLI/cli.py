import torch
import json
import os
from transformers import BertTokenizer, BertConfig, BertForSequenceClassification
from tqdm import tqdm
import click

# Assuming the model and tokenizer are loaded globally
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Load the model configuration and model from a .pth file
config = BertConfig.from_pretrained('bert-base-uncased')
BertModel = BertForSequenceClassification(config)
model = BertModel.from_pretrained("yadagiriannepaka/BERT_MODELGYANDEEP.pth")  #this is fetching from external directoory
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


class TextDetector:
    def get_score(self, text):
        # Encode the text to BERT's format
        inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True,
                           padding=True)  # our tokenizing logic may be different
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Get prediction
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)  # how to find this probability

        # Assuming we are interested in the probability of the first class
        return probabilities[0, 1].item()


detector = TextDetector()


def comparative_score(score1, score2, epsilon=1e-3):
    """
    Return a single score in [0, 1] based on the comparison of two [0, 1] input scores.

    :param score1: first score
    :param score2: second score
    :param epsilon: non-answer (output score = 0.5) epsilon threshold
    :return: [0, 0.5) if score1 > score2 + eps; (0.5, 1] if score2 > score1 + eps; 0.5 otherwise
    """
    if score1 > score2 + epsilon:
        return (1.0 - min(max(score2, 0.0), 1.0)) / 2.0 + 0.5
    if score2 > score1 + epsilon:
        return min(max(score1, 0.0), 1.0) / 2.0
    return 0.5


@click.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_directory', type=click.Path(file_okay=False, exists=True))
def process_input(input_file, output_directory):
    with open(os.path.join(output_directory, 'results.jsonl'), 'w') as out:
        for line in tqdm(input_file, desc='Predicting pairs', unit=' pairs'):
            j = json.loads(line)
            t1 = j['text1']
            t2 = j['text2']

            score1 = detector.get_score(t1)
            score2 = detector.get_score(t2)

            json.dump({'id': j['id'], 'is_human': float(comparative_score(score1, score2))}, out)
            out.write('\n')
            out.flush()


if __name__ == "__main__":
    process_input()
