from models.llm import llm


def business_analysis_agent(state):

    research = state["research"]

    prompt = f"""
You are a Venture Capital analyst.

Using ONLY this startup research:

{research}

Generate a professional investment analysis.

IMPORTANT

- Return ONLY Markdown.
- Never use ===== or ---- separators.
- Keep the response under 500 words.
- Use concise bullet points.

# Competitor Analysis

- Top Competitors
- Competitive Advantages
- Competitive Risks

# Market Analysis

- Market Type
- Market Size
- Growth Potential
- Key Trends
- Opportunities
- Challenges

# Risk Analysis

- Business Risks
- Market Risks
- Financial Risks
- Overall Risk Level

# Investment Score

Investment Score: XX/100

Team Score: XX/100

Market Score: XX/100

Competition Score: XX/100

Risk Score: XX/100

Risk Level: Low / Medium / High

Recommendation:
Invest / Consider / Avoid

Reasoning:
- 4 concise bullet points
"""

    response = llm.invoke(prompt)

    return {
        "business_analysis": response.content
    }