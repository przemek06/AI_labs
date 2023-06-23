from data_mining import read_data, show_averages_of_data, show_distribution_of_types
from data_preparation import normalize_data, standardize_data, split_data, split_columns
from classification import train_bayes_model, train_decision_tree_model
from scores import score_the_model, show_scores

def main():
    df = read_data("glass.data")
    print("STATISTICS FOR DATA: ")
    show_averages_of_data(df)
    print()
    show_distribution_of_types(df)
    print("===================================================================")
    df_normalized = normalize_data(df)
    print("STATISTICS FOR DATA AFTER NORMALIZATION: ")
    show_averages_of_data(df_normalized)
    print()
    show_distribution_of_types(df_normalized)
    print("===================================================================")
    df_standardized = standardize_data(df)
    print("STATISTICS FOR DATA AFTER STANDARDIZATION: ")
    show_averages_of_data(df_standardized)
    print()
    show_distribution_of_types(df_standardized)
    print("===================================================================")
    print()

    print("CLASSIFICAITON MODELS' TRAINING")
    training_df, validation_df, test_df = split_data(df)
    training_df_normalized, validation_df_normalized, test_df_normalized = split_data(df_normalized)
    training_df_standardized, validation_df_standardized, test_df_standardized = split_data(df_standardized)

    # Split and train Bayes model for training data
    X_train, Y_train = split_columns(training_df)
    X_valid, Y_valid = split_columns(validation_df)
    X_test, Y_test = split_columns(test_df)
    bayes_model, bayes_parameters = train_bayes_model(X_train, Y_train, X_valid, Y_valid)

    # Split and train Bayes model for normalized training data
    X_train_normalized, Y_train_normalized = split_columns(training_df_normalized)
    X_valid_normalized, Y_valid_normalized = split_columns(validation_df_normalized)
    X_test_normalized, Y_test_normalized = split_columns(test_df_normalized)
    bayes_model_normalized, bayes_parameters_normalized = train_bayes_model(X_train_normalized, Y_train_normalized, X_valid_normalized, Y_valid_normalized)

    # Split and train Bayes model for standardized training data
    X_train_standardized, Y_train_standardized = split_columns(training_df_standardized)
    X_valid_standardized, Y_valid_standardized = split_columns(validation_df_standardized)
    X_test_standardized, Y_test_standardized = split_columns(test_df_standardized)
    bayes_model_standardized, bayes_parameters_standardized = train_bayes_model(X_train_standardized, Y_train_standardized, X_valid_standardized, Y_valid_standardized)

    print("DECISION TREE WITHOUT PREPROCESSING")
    decision_tree_model, decision_tree_parameters = train_decision_tree_model(X_train, Y_train, X_valid, Y_valid)
    print("DECISION TREE WITH NORMALIZATION")
    decision_tree_model_normalized, decision_tree_parameters_normalized = train_decision_tree_model(X_train_normalized, Y_train_normalized, X_valid_normalized, Y_valid_normalized)
    print("DECISION TREE WITH STANDARDIZATION")    
    decision_tree_model_standardized, decision_tree_parameters_standardized = train_decision_tree_model(X_train_standardized, Y_train_standardized, X_valid_standardized, Y_valid_standardized)


    print("CLASSIFICAITON MODELS' PREDICTIONS")

    # Calculate and show scores for Bayes model
    scores = score_the_model(bayes_model, X_test, Y_test)
    show_scores("Bayes (parameters: " + str(bayes_parameters) + ")", scores)

    # Calculate and show scores for normalized Bayes model
    scores_normalized = score_the_model(bayes_model_normalized, X_test_normalized, Y_test_normalized)
    show_scores("Normalized Bayes (parameters: " + str(bayes_parameters_normalized) + ")", scores_normalized)

    # Calculate and show scores for standardized Bayes model
    scores_standardized = score_the_model(bayes_model_standardized, X_test_standardized, Y_test_standardized)
    show_scores("Standardized Bayes (parameters: " + str(bayes_model_standardized) + ")", scores_standardized)

    # Calculate and show scores for Bayes model
    scores = score_the_model(decision_tree_model, X_test, Y_test)
    show_scores("Decision Tree (parameters: " + str(decision_tree_parameters) + ")", scores)

    # Calculate and show scores for normalized Decision Tree model
    scores_normalized = score_the_model(decision_tree_model_normalized, X_test_normalized, Y_test_normalized)
    show_scores("Normalized Decision Tree (parameters: " + str(decision_tree_parameters_normalized) + ")", scores_normalized)

    # Calculate and show scores for standardized Decision Tree model
    scores_standardized = score_the_model(decision_tree_model_standardized, X_test_standardized, Y_test_standardized)
    show_scores("Standardized Decision Tree (parameters: " + str(decision_tree_parameters_standardized) + ")", scores_standardized)




if __name__ == "__main__":
    main()