from pydantic import BaseModel, Field

COMPLAINT_ANSWER_TOPIC = "complaint_answer"
COMPLAINT_ANSWER_CONSUMER_GROUP = "complaint_answer_group"


class ComplaintAnswerEventSchema(BaseModel):
    student_telegram_user_id: int = Field(examples=[524234231])
    answer: str = Field(examples=["Попробуйте перезагрузить компьютер"])
