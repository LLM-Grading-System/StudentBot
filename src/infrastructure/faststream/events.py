from pydantic import BaseModel, Field

COMPLAINT_ANSWER_TOPIC = "complaint_answer"
COMPLAINT_ANSWER_CONSUMER_GROUP = "complaint_answer_group"


class ComplaintAnswerEventSchema(BaseModel):
    student_telegram_user_id: int = Field(examples=[524234231])
    answer: str = Field(examples=["Попробуйте перезагрузить компьютер"])


COMMENT_CREATED_TOPIC = "comment_created"
COMMENT_CREATED_CONSUMER_GROUP = "comment_created_group"


class CommentCreatedEventSchema(BaseModel):
    username: str = Field(examples=["octocat"])
    pull_request_link: str = Field(examples=["/pull_request/1"])
