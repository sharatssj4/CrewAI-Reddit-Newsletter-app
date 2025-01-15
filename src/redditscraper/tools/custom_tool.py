from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import praw as pr
import os

class MyCustomTool(BaseTool):
    name: str = "Reddit Scraper"
    description: str = (
        "Scrape reddit content based on the topic"
    )


    def _run(self, max_comments_per_post: int = 2) -> str:
        # Implementation goes here
        """Useful to scrape a reddit content"""
        reddit = pr.Reddit(
            client_id=os.environ["client_id"],
            client_secret=os.environ["client_secret"],
            user_agent="user-agent",
        )
        subreddit = reddit.subreddit("Science")
        scraped_data = []

        for post in subreddit.hot(limit=2):
            post_data = {"title": post.title, "url": post.url, "comments": []}

            try:
                post.comments.replace_more(limit=0)  # Load top-level comments only
                comments = post.comments.list()
                if max_comments_per_post is not None:
                    comments = comments[:7]

                for comment in comments:
                    post_data["comments"].append(comment.body)

                scraped_data.append(post_data)

            except praw.exceptions.APIException as e:
                print(f"API Exception: {e}")
                time.sleep(60)  # Sleep for 1 minute before retrying

        return scraped_data
