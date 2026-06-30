from pathlib import Path
import frontmatter
from .models import Capability
from .exceptions import (
    InvalidCapabilityError,
)

def load_capability(
    file_path: Path
) -> Capability:
    post = frontmatter.load(
        file_path
    )

    name = post.get("name")

    category = file_path.parent.name    

    capability_id = (
        f"{category}.{name}"
    )

    description = post.get(
        "description",
        ""
    )

    tools = post.get(
        "tools",
        []
    )
    if not isinstance(
        tools,
        list
    ):
        raise InvalidCapabilityError(
            f"{file_path}: tools must be a list"
        )

    model = post.get(
        "model",
        ""
    )

    prompt = post.content
    
    if not name:
        raise InvalidCapabilityError(
            f"{file_path} missing name"
    )
 
    return Capability(
    id=capability_id,
    name=name,
    category=category,
    description=description,
    tools=tools,
    model=model,
    prompt=prompt,
    source_path=file_path
)