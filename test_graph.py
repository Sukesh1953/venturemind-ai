from agents.supervisor import venturemind_graph

result = venturemind_graph.invoke(
    {
        "website_url": "https://www.ycombinator.com",
        "company_name": "Y Combinator"
    }
)

print("\n")
print("=" * 50)
print("RESEARCH ANALYSIS")
print("=" * 50)
print(result["research"])

print("\n")
print("=" * 50)
print("FINAL REPORT")
print("=" * 50)
print(result["report"])