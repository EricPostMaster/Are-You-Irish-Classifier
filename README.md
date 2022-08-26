# Measuring "Irish-ness" with the Murphy Index :shamrock:

## :bulb: The Idea:
Spam detection can be tricky business! Spammy emails or text messages generally have plenty of words to work with, but what if we only have a couple of words to work with? What if we want to detect whether an account is spammy just by its name?

## :gear: The Method:
Turns out, this is just the sort of thing the Naive Bayes algorithm is good at. We can divide the name(s) into ngram tokens and use those tokens to calculate a probability that a name is spam. For instance, if my name is Eric and I am using 3-grams, then the document would become `Eri ric`. Ngram length is one of the hyperparameters I tuned during model development, which you can review in more detail in [this Jupyter notebook](https://github.com/EricPostMaster/Are-You-Irish-Classifier/blob/main/model_development.ipynb).

Based on the excellent work of David Mandell Freeman shared in [this paper](https://dl.acm.org/doi/abs/10.1145/2517312.2517314).

By comparing average log predicted probabilities of name ngrams being Irish to the "benchmark" Irish surname "Murphy", we can create a tongue-in-cheek "Irish-ness" score just in time for St. Patrick's Day!

For example, if the average log predicted probability of the name "Murphy" is -6.58, and the average log predicted probability of "Bailey" is -7.762, then the Murphy Index would be (-6.58/-7.762)\*-100 =  84.77. A bonnie lovely Murphy score, I'd say! :)

## :iphone: The App:
The app is easy to use: just drop your surname (or your friend's surname!) in the text box, press Enter, and get your Murphy score.

As a bonus, you can see your score stacks up against others who have used the app before you. I thought users would enjoy seeing how their Murphy indices compare to others, so I connected to the Google Sheets API and store each score produced by the model and present the results below the score results. I've gotten a lot of great feedback on it!

<img src="https://github.com/EricPostMaster/Are-You-Irish-Classifier/blob/main/images/murphy_index2.gif" width="400px">

Try it out yourself [here](https://ericpostmaster-are-you-irish-classifier-main-z64nlv.streamlitapp.com/)!

I'd love to hear what you think! Feel free to [message me on LinkedIn](https://www.linkedin.com/in/ericsims2/) or submit an issue or pull request here.
