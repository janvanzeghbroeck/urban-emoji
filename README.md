# Urban Emoji

<img src="figures/1f913.png" width=100% height=100%/>

<img src="figures/break_line.png" width=100% height=100%/>

Urban Emoji uses natural language processing (nlp) and non-negative matrix factorization (nmf) to interpret slang meanings of emojis from analyzing tweets.

<img src="figures/break_line.png" width=100% height=100%/>

## Process

- Using Twitter API to download tweets
- Identify tweets that contain emojis
- Process the tweets and use the emojis as labels
- Vectorize the tweets using tfidf
- Use NMF and topic modeling to group the tweets and print most common words in each topic
- Print the emojis associated with the tweets in each topic
- Find topics with a large percentage of similar emojis to connects words and emojis
- Currently applying NMF for tweets all with similar emojis to further identify associated words to find their slang definitions

<img src="figures/break_line.png" width=100% height=100%/>

## Results

Below is a proof of concept example of the results, as you can see the crying emoji is most often affiliated with the words above for that group. As I add more and more tweets and use different techniques I expect to get further improve the slang definitions for many emojis.

![Alt text](/figures/results_example.png "Results Example")

<img src="figures/break_line.png" width=100% height=100%/>

## Tech Stack
Twitter’s API, Python, Pandas, Scikit-Learn, Unicode

<img src="figures/break_line.png" width=100% height=100%/>

## Other Projects
Please feel free to check out my project With New Belgium Brewery called [Seeing Taste](https://github.com/janvanzeghbroeck/Seeing-Taste)

[Linkedin](https://www.linkedin.com/in/janvanzeghbroeck/)
