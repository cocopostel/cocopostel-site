import re,html,urllib.request
F=["https://www.theguardian.com/world/rss","https://feeds.bbci.co.uk/news/world/rss.xml","https://rss.nytimes.com/services/xml/rss/nyt/World.xml","https://www.aljazeera.com/xml/rss/all.xml","https://feeds.washingtonpost.com/rss/world"]
for u in F:
  print("==",u)
  try:d=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=20).read().decode("utf8","ignore")
  except Exception as e:print("  failed",e);continue
  for it in re.findall(r"<item>(.*?)</item>",d,re.S)[:10]:
    g=lambda t:html.unescape(re.sub(r"<!\[CDATA\[|\]\]>|<[^>]+>","",(re.search(r"<%s>(.*?)</%s>"%(t,t),it,re.S) or [None,""])[1])).strip()
    print("*",g("title"),"|",g("link"),"|",g("pubDate"),"|",g("description")[:220])
