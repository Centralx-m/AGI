"""
Learning Package
================

Contains learning systems for the AI agent:
- BookLearner: Learn from books and documents
- SelfTrainer: Learn from experience and feedback
"""

from .book_learner import BookLearner
from .self_trainer import SelfTrainer

__all__ = ['BookLearner', 'SelfTrainer']
