"""Orthogonal functions base class.
"""
from abc import ABC


class OrthogonalFunctions(ABC):
    def __init__(self, T, m):
        self.T = T
        self.m = m
