from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Enter the text here")

    def __str__(self):
        return f"{self.fullname} - {self.born_date} - {self.born_location} - {self.description}"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE,primary_key=True)
    tags = models.ManyToManyField(Tag)
    #tags = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quote} - {self.author.fullname} - {self.tags}"
    

