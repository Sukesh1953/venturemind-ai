from models.llm import llm


def research_agent(state):

    website_content = state["website_content"][:6000]   # Limit website content

    prompt = f"""
You are a startup research analyst.

Analyze the following website content.

Website:

{website_content}

Return ONLY Markdown.

Keep the entire response under 300 words.

## Company Overview
(2-3 sentences)

## Industry

## Products / Services
- Bullet points

## Target Customers
- Bullet points

## Business Model
(1-2 sentences)

## Growth Opportunities
- 3 bullet points

Do not explain unnecessarily.
"""

    response = llm.invoke(prompt)

    return {
        "research": response.content
    }