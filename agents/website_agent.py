from tools.website_reader import read_website


def website_agent(state):

    website_url = state["website_url"]

    content = read_website(website_url)

    return {
        "website_content": content
    }