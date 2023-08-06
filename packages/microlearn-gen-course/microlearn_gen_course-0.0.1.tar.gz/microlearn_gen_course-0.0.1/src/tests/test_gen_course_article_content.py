"""
Test GenCourseArticleContent

Usage:
    pytest src/tests/test_gen_course_article_content.py -v --log-cli-level INFO
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from gen_course.gen_course_article_content import GenCourseArticleContent

from llm_factory.llm_factory import LLMFactory


load_dotenv(override=True)

logger = logging.getLogger(__name__)


def test_generate():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=256,
    )
    gen = GenCourseArticleContent(llm=llm, verbose=True)
    output = gen.generate(
        course_title="Introductory Python Course",
        course_description="Master the basics of Python programming language starting from zero knowledge.",
        article_title="Introduction to Python Programming",
    )
    logger.info(f"course's article's content: {output.content}")
    logger.info(f"course's article's questions: {output.questions}")
    assert len(output.questions) == 3
    assert len(output.content.split()) <= 150
