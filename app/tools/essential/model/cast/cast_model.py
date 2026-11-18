from pydantic import BaseModel


def cast_model[T: BaseModel](
        model: BaseModel,
        model_type: type[T],
) -> T:
    casted_model: T = model_type.model_validate(model.model_dump())
    return casted_model
