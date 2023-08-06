
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .gen_base import GenBase


class CourseMetadataModel(BaseModel):
    title: str = Field(
        description="title of the course, where the length of the title is between 2 and 4 words")
    description: str = Field(
        description="description of the course, where the length of the description is maximum of 150 words")


class GenCourseMetadata(GenBase):
    """
    Generator class for course metadata(title, description, etc.).
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
---
Rewrite the title and description for the course."""

    def __init__(self, llm, verbose: bool = False):
        super().__init__(llm, verbose)

    def get_output_parser(self):
        return PydanticOutputParser(pydantic_object=CourseMetadataModel)

    def generate(self,
                 course_title: str,
                 course_description: str,
                 ) -> CourseMetadataModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
        )
