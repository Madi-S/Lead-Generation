import re


__all__ = ['linkedin_link', 'head_regex']

linkedin_link = 'https://www.linkedin.com/home'
head_regex = re.compile(
    r'(ceo|owner|manager|chief|manager)', flags=re.IGNORECASE)
