"""
Generator for course's articles titles.
"""
from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .gen_base import GenBase


class CourseArticlesTitlesModel(BaseModel):
    titles: List[str] = Field(
        description="List of course's articles titles. All the titles are unique and sequential for the course.")


class GenCourseArticleTitles(GenBase):
    """
    Generator class for course's articles titles.
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
---
Write {articles_count} titles for the articles of the course. Each title should be maximum of {title_length_words} words."""

    def __init__(self, llm, verbose: bool = False):
        super().__init__(llm, verbose)

    def get_output_parser(self):
        return PydanticOutputParser(pydantic_object=CourseArticlesTitlesModel)

    def generate(self,
                 course_title: str,
                 course_description: str,
                 articles_count: int,
                 title_length_words: int = 8,
                 ) -> CourseArticlesTitlesModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            articles_count=articles_count,
            title_length_words=title_length_words,
        )
