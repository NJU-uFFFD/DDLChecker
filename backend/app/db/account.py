from db import db
from dataclasses import dataclass


@dataclass
class Account(db.Model):
    id: int