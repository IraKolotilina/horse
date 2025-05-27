from sqlalchemy import Column, Integer, ForeignKey, String
from app.models.base import Base


class PlayerCurrency(Base):
    __tablename__ = "player_currency"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))
    currency_type = Column(String, nullable=False)  # real или game
    amount = Column(Integer, default=0)