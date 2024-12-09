from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f"UploadedFile('{self.filename}')"