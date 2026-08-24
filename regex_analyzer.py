import re


def analyze_text(text):
	return {
		"hashtags": re.findall(r"#\w+", text),
		"mentions": re.findall(r"@\w+", text),
		"urls": re.findall(r"https?://\S+", text),
		"emails": re.findall(
			r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
			text,
		),
	}
