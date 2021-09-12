# Metrics

This document contains information on metrics and scores used in Varangian.

## Augmented Static Analysis

**Sample:** One instance of a static analyzer output. Often called an error or a warning.

**Augmented Static Analyzer (*AugSA*):** An AI model or an ensemble of models trained on thousands of labelled samples to predict whether a sample is actually a bug.

**Positive/Negative Prediction:** AugSA predicts positive if it considers sample to contain a bug. It predicts negative if it considers a sample to not contain a bug.

**True Positive (*TP*):** A sample that is predicted to be a bug and is actually a bug.

**False Positive (*FP*):** A sample that is predicted to be a bug and is actually not a bug.

**Model Confidence Score:** The likelihood of a sample being a bug according to AugSA.

**Prediction Threshold:** The threshold indicates the confidence score beyond which the prediction changes.
Example: If the threshold is 0.5, a confidence score of 0.51 would mean the model is predicting positive and confidence score of 0.49 would mean the model is predicting negative.


## Varangian Issue

**Rank:** Ranking of bugs based on model confidence. The model confidence is calculated during an Augmented Static Analysis run over a commit. Rank 1 indicates model has the most confidence that the bug is a True Positive, compared to other bugs.

**Developer Experience:** The number of FPs a developer has to analyze before finding a TP. This is calculated as the ratio of FP to TP (FP/TP) during AugSA testing.
Example: The ideal score is 0 which means every bug the developer analyzes is a TP. A score of 3.0 would mean that the developer has to go through 3 FPs before finding a TP.

**Bug Likelihood:** Likelihood that a bug is a TP. This is graded as High, Medium and Low.

**Bug Likelihood - High:** Developer experience of less than 1 (0 <= FP/TP < 0.5). Almost every bug that the developer analyzes is a TP or in the worst case, every alternate bug is a TP.

**Bug Likelihood - Medium:** Developer experience of 1 to 2 (0.5 <= FP/TP < 2). Every alternate bug is a TP or in the worst case, every third bug is a TP.

**Bug Likelihood - Low:** Developer experience of 1 to 2 (2 <= FP/TP <= 3). In the best case, every third bug is a TP.
