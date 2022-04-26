# RockScissorPaperProject

## MileStone 1
- I have created a simple model that could do image classification tasks and download them with labels.
- This model could have 4 different outcomes: Rock, Scissor, Paper and Nothing. The model could capture significant features within the input image and use that to determine the corresponding categoriy of the image. Finally, the class with the highest probability is the output.
- When preparing the training data, I only used my left hand and tried to position my "feature" at a fixed position, which could somehow improve the accuracy of the final model as the features were very obvious and easy to learn. However, this would also lead to the result that this model is not well generalized so it couldn't give an accurate result under various conditions.
- To further improve the accuracy, I rotated my hand so lots of different features could be learnt by the model and I chose a reasonable number of samples for each class.
- The hyperparameters were set by experience where generally a 100 epoch would work for such a easy task. The batch size was chosen to be 512 and the learning rate was chosen to be 0.0001. Hopefully it was trained by Adam.
- Before downloading the model, several simple tests were done, which showed that the model was not that accurate as it couldn't output one high probability while the other 3 probabilities stay low, indicating that the model is unsure.
- The model was downloaded and could be further used easily. 
![ModelTrain](image/Model%20Training.png)
