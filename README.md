# Urban Emoji

<img src="figures/1f5e8.png" width=20% height=20%/> <img src="figures/1f913.png" width=20% height=20%/>

<img src="figures/break_line.png" width=100% height=100%/>

## Overview

Urban Emoji uses natural language processing (nlp) and non-negative matrix factorization (nmf) to interpret slang meanings of emojis from analyzing tweets.

- [Process](#process)
- [Results](#results)
- [Business Applications](business_applications)
- [Tech Stack](#tech-stack)
- [More Projects](#more-projects)

<img src="figures/break_line.png" width=100% height=100%/>

## Process

- Using Twitter API to download tweets
- Use AWS to run the Twitter API using EC2 and automatically save the tweets to a bucket on S3
- Use a cron job to automatically download tweets every day
- Identify tweets that contain emojis
- Process the tweets and use the emojis as labels
- Vectorize the tweets using tfidf
- Use NMF and topic modeling to group the tweets and print most common words in each topic
- Print the emojis associated with the tweets in each topic
- Find topics with a large percentage of similar emojis to connects words and emojis finding 'definitions'
- Apply NMF for tweets all with similar emojis to further identify associated words to find better define their slang meanings
- Further work: Identify profiles of people who commonly use a specific emoji (think demographic information)

<img src="figures/break_line.png" width=100% height=100%/>

## Results

Below is a proof-of-concept example of the results, as you can see the crying emoji is most often affiliated with the words above for that group. The hashtags #girlposts and #femaletexts are associated with this emoji which show an indication of what type of people are commonly using this emoji.

As I add more and more tweets and use different techniques I expect to get further improve the slang definitions and also get insight on the type of people who use each emoji.

![Alt text](/figures/results_example.png "Results Example")

<img src="figures/break_line.png" width=100% height=100%/>

## Business Insight

The emoji information Urban Emoji discovers is not useful for impressing the younger generation on how hip you are but also has purpose in other Data Science projects and business applications. Below are just a few example of where this technology could be used:

#### Data Science Applications
- Use emojis as labels for text documents
- Replace emojis with a list of words that define it to improve NLP analysis of short text documents
- Improve predictive text algorithms to better recommend an appropriate emoji

#### Business Applications
- Correctly use emojis in a company's social media posts to connect with the intended audience
- Aid in better identifying what the audience of a product/company/business actually is

<img src="figures/break_line.png" width=100% height=100%/>

## Tech Stack
- Twitter’s API & Tweepy
- Python
- Pandas
- Scikit-Learn
- Unicode
- AWS, S3, & EC2
- Crontab

<img src="figures/break_line.png" width=100% height=100%/>

## More Projects
Please feel free to check out my project With New Belgium Brewery called [Seeing Taste](https://github.com/janvanzeghbroeck/Seeing-Taste)

[Linkedin](https://www.linkedin.com/in/janvanzeghbroeck/)
