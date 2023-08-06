"""
Generator for course's article's question's answer.
"""
from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .gen_base import GenBase


class ArticleQuesAnswerModel(BaseModel):
    answer: str = Field(description="Article's question's answer")


class GenAnswerToArticleQues(GenBase):
    """
    Generator class to answer article's question.
    """
    HUMAN_PROMPT = """I've developed a micro learning course about the following:
---
Course title: {course_title}
Course description: {course_description}
Article title: {article_title}
Article content: {article_content}
---
Based on the information specified above, answer the question: "{question}" with maximum length of {content_length_words} words."""

    def __init__(self, llm, verbose: bool = False):
        super().__init__(llm, verbose)

    def get_output_parser(self):
        return PydanticOutputParser(pydantic_object=ArticleQuesAnswerModel)

    def generate(self,
                 course_title: str,
                 course_description: str,
                 article_title: str,
                 article_content: str,
                 question: str,
                 content_length_words: int = 150,
                 ) -> ArticleQuesAnswerModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            article_title=article_title,
            article_content=article_content,
            question=question,
            content_length_words=content_length_words,
        )
