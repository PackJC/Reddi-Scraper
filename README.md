====================================
Reddit Scraper +Sentiment
====================================

Welcome to my project! I hope you've found everything easily. Althouht centered around Finance, this tool can be used to guage certain social and political trends.

* `Features and Updates`_
* Introduction_
* Dependencies_
* `Running the script`_
* `About the Sentiment Scoring`_


Features and Updates
------------------------------------
Many thanks to George Berry, Ewan Klein, Pierpaolo Pantone for key contributions to make VADER better.  The new updates includes capabilities regarding:

#. Refactoring for Python 3 compatibility, improved modularity, and incorporation into `[NLTK] <http://www.nltk.org/_modules/nltk/sentiment/vader.html>`_ ...many thanks to Ewan & Pierpaolo.
#. Restructuring for much improved speed/performance, reducing the time complexity from something like O(N^4) to O(N)...many thanks to George.
#. Simplified pip install and better support for vaderSentiment module and component import. (Dependency on vader_lexicon.txt file now uses automated file location discovery so you don't need to manually designate its location in the code, or copy the file into your executing code's directory.)
#. More complete demo in the ``__main__`` for ``vaderSentiment.py``. The demo has:

	* examples of typical use cases for sentiment analysis, including proper handling of sentences with:

		- typical negations (e.g., "*not* good")
		- use of contractions as negations (e.g., "*wasn't* very good")
		- conventional use of **punctuation** to signal increased sentiment intensity (e.g., "Good!!!")
		- conventional use of **word-shape** to signal emphasis (e.g., using ALL CAPS for words/phrases)
		- using **degree modifiers** to alter sentiment intensity (e.g., intensity *boosters* such as "very" and intensity *dampeners* such as "kind of")
		- understanding many **sentiment-laden slang** words (e.g., 'sux')
		- understanding many sentiment-laden **slang words as modifiers** such as 'uber' or 'friggin' or 'kinda'
		- understanding many sentiment-laden **emoticons** such as :) and :D
		- translating **utf-8 encoded emojis** such as 💘 and 💋 and 😁
		- understanding sentiment-laden **initialisms and acronyms** (for example: 'lol')

	* example  


====================================
Introduction
====================================

To do: Add Introduction

====================================
Dependencies
====================================

To do: Add Dependencies

====================================
Running the script
====================================

To do: Add How 2 Run

====================================
About the Sentiment Scoring
====================================

* The ``compound`` score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate. 
 
  It is also useful for researchers who would like to set standardized thresholds for classifying sentences as either positive, neutral, or negative.  
  Typical threshold values (used in the literature cited on this page) are:

 #. **positive sentiment**: ``compound`` score >=  0.05
 #. **neutral  sentiment**: (``compound`` score > -0.05) and (``compound`` score < 0.05)
 #. **negative sentiment**: ``compound`` score <= -0.05

* The ``pos``, ``neu``, and ``neg`` scores are ratios for proportions of text that fall in each category (so these should all add up to be 1... or close to it with float operation).  These are the most useful metrics if you want multidimensional measures of sentiment for a given sentence.
