from .db import Base, engine
from .models import Job

print("Creating DB tables...")
Base.metadata.create_all(bind=engine)
print("Done.")

