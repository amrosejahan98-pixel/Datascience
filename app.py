import streamlit as st
import re


def analyze_text(text):
	return {
		"hashtags": re.findall(r"#\w+", text),
		"mentions": re.findall(r"@\w+", text),
		"urls": re.findall(r"https?://\S+", text),
		"emails": re.findall(
			r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text
		),
	}


def search_tweets(keyword, limit=3):
	return [
		{
			"tweet": f"I love #{keyword}! Contact me at test@gmail.com @elon https://example.com"
		},
		{"tweet": f"Check this out #{keyword} @user http://twitter.com"},
		{"tweet": f"Email us at support@{keyword}.com for #{keyword} updates"},
	][:limit]


st.title("Twitter/X Regex Analyzer")
keyword = st.text_input("Enter a keyword", "python")

if st.button("Search Tweets"):
	if keyword:
		tweets = search_tweets(keyword)
		for item in tweets:
			st.write("### Tweet")
			st.write(item["tweet"])
			result = analyze_text(item["tweet"])
			st.write("Hashtags:", result["hashtags"])
			st.write("Mentions:", result["mentions"])
			st.write("URLs:", result["urls"])
			st.write("Emails:", result["emails"])
	else:
		st.warning("Please enter a keyword.")
