# web-similarity-detector

##Overview
Check if your text contents(or Documents) is the copied-contents on the Web.
Put out check results that is structured by either being perfect copied or its ratio of similarities.


##Specification
1.Get the inputted text, and make some divisions from it for query.
	- Divisions is created by splitting text with “、” and “。”.
	- If the division’s length is too less, append it to the next division unless over the limit of particular length.
2.Get serps of search engine by http request with each divisions as query.
3.Check descriptions on the serps if they are include my query or similar to it.

##Usage
follow to sample.py
※You must take some interval between each requests for the Google search engine Servers.(like "time.sleep(10)" in sample.py)

