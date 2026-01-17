from typing import List,Optional
from pydantic import BaseModel

class Comment(BaseModel):
    id:int
    content:str
    replies:Optional[List['Comment']]=None

Comment.model_rebuild()

comment=Comment(
    id=1,
    content="First spam",
    replies=[
        Comment(  # First person to Comment on the visual
            id=2,
            content="second spam",
            replies=[
                Comment( # reply to the person with the explain
                    id=3,
                    content="Third spam"
                ),

            
            Comment(  # Second Normal replies for the content
                id=4,
                content="Fourth spam",
                replies=[
                    Comment(
                        id=5,
                        content="Fifit Spam"
                    )
               
              ]
        )                ]
    )]
)

print(comment)