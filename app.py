from flask import Flask, request, render_template
from flask.logging import create_logger
import logging


import numpy as np
import torch.nn as nn
import torch

import json
    
from string import punctuation

# pylint: disable=W0621
def tokenize_review(test_review):
    test_review = test_review.lower() # lowercase
    # get rid of punctuation
    test_text = ''.join([c for c in test_review if c not in punctuation])

    # splitting by spaces
    test_words = test_text.split()

    # tokens
    test_ints = []
    test_ints.append([vocab_to_int[word] for word in test_words])

    return test_ints

def pad_features(reviews_ints, seq_length):
    ''' Return features of review_ints, where each review is padded with 0's 
        or truncated to the input seq_length.
    '''
    
    # getting the correct rows x cols shape
    features = np.zeros((len(reviews_ints), seq_length), dtype=int)

    # for each review, I grab that review and 
    for i, row in enumerate(reviews_ints):
        features[i, -len(row):] = np.array(row)[:seq_length]
    
    return features

class SentimentRNN(nn.Module):
    """
    The RNN model that will be used to perform Sentiment analysis.
    """

    def __init__(self, vocab_size, output_size, embedding_dim, hidden_dim, n_layers, drop_prob=0.5):
        """
        Initialize the model by setting up the layers.
        """
        super(SentimentRNN, self).__init__()

        self.output_size = output_size
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim
        
        # embedding and LSTM layers
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, 
                            dropout=drop_prob, batch_first=True)
        
        # dropout layer
        self.dropout = nn.Dropout(0.3)
        
        # linear and sigmoid layers
        self.fc = nn.Linear(hidden_dim, output_size)
        self.sig = nn.Sigmoid()
        
    # pylint: disable=W0221
    def forward(self, x, hidden):
        """
        Perform a forward pass of our model on some input and hidden state.
        """
        batch_size = x.size(0)

        # embeddings and lstm_out
        embeds = self.embedding(x)
        lstm_out, hidden = self.lstm(embeds, hidden)
    
        # stack up lstm outputs
        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)
        
        # dropout and fully-connected layer
        out = self.dropout(lstm_out)
        out = self.fc(out)
        # sigmoid function
        sig_out = self.sig(out)
        
        # reshape to be batch_size first
        sig_out = sig_out.view(batch_size, -1)
        sig_out = sig_out[:, -1] # get last batch of labels
        
        # return last sigmoid output and hidden state
        return sig_out, hidden
    
    
    def init_hidden(self, batch_size):
        ''' Initializes hidden state '''
        # Create two new tensors with sizes n_layers x batch_size x hidden_dim,
        # initialized to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data
        
        if (train_on_gpu):
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda(),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_(),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_())
        
        return hidden
        
# pylint: disable=E1101
def sentiment_predict(net, test_review, sequence_length=200):
    
    net.eval()
    
    # tokenize review
    test_ints = tokenize_review(test_review)
    
    # pad tokenized sequence
    features = pad_features(test_ints, sequence_length)
    
    # convert to tensor to pass into your model
    feature_tensor = torch.from_numpy(features)
    
    batch_size = feature_tensor.size(0)
    
    # initialize hidden state
    h = net.init_hidden(batch_size)
    
    if(train_on_gpu):
        feature_tensor = feature_tensor.cuda()
    
    # get the output from the model
    output, h = net(feature_tensor.long(), h)
    
    # convert output probabilities to predicted class (0 or 1)
    pred = torch.round(output.squeeze()) 
    # printing output value, before rounding
    LOG.info('Prediction value, pre-rounding: {:.6f}'.format(output.item()))
    
    # print custom response
    if(pred.item()==1):
        return "Positive review detected!"
    else:
        return "Negative review detected."


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=['POST'])
def predict():
    """Performs an sentiment prediction
        
        input looks like:
        {
        "message":"This movie had the best acting and the dialogue was so good. I loved it."
        }
        
        result looks like:
        {
        "statusCode": "200",
        "headers":{"Content-type":"application/json"},
        "body":"{\"prediction\": \"Positive review detected!\"}
        }
        
        """
    
    # Logging the input
    json_request = request.json
    LOG.info("JSON : \n%s", json.dumps(json_request))
    # get an output prediction from the pretrained model, clf
    prediction = sentiment_predict(net, json_request['message'])
    # TO DO:  Log the output prediction value
    response = {
        "statusCode": "200",
        "headers":{"Content-type":"application/json"},
        "body":"{\"prediction\":\"" + prediction + "\"]"
        }
    LOG.info("JSON Response : \n%s", json.dumps(response))
    return response

if __name__ == "__main__":
    # load pretrained model as clf
    train_on_gpu=torch.cuda.is_available()

    with open('./model_data/vocab.json', 'r') as fp:
        vocab_to_int = json.load(fp)
			
    # Instantiate the model w/ hyperparams
    vocab_size = len(vocab_to_int)+1 # +1 for the 0 padding + our word tokens
    output_size = 1
    embedding_dim = 400
    hidden_dim = 256
    n_layers = 2

    net = SentimentRNN(vocab_size, output_size, embedding_dim, hidden_dim, n_layers)
    net.load_state_dict(torch.load('./model.dat'))

    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80


