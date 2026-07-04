from tools.website_reader import read_website

text = read_website("https://www.ycombinator.com")

print(text[:1500])