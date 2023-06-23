from sklearn.metrics import f1_score, accuracy_score

def score_the_model(model, X_test, Y_test):

    predictions = model.predict(X_test)

    f1 = f1_score(Y_test, predictions, average='macro')
    accuracy = accuracy_score(Y_test, predictions)
    
    return f1, accuracy

def show_scores(name, score):
    print("F1 score for " + name + ": " + str(score[0]))
    print("Accuracy for " + name + ": " + str(score[1]))