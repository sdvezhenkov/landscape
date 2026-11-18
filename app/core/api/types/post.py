from app.tools.essential.model.camel.types.camel_model import CamelModel


class Post(CamelModel):
    id: int
    user_id: int
    title: str
