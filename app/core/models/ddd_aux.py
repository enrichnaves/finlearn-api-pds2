from datetime import datetime
from typing import Annotated

ImplictId = Annotated[str, "Implicitly id defined by the database"]
ImplictDateTime = Annotated[datetime, "Implicitly datetime defined by the database"]
