from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()


class Section(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

    def total_weight(self):
        return sum([item.weight for item in self.items.all()])


class Pack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    sections = models.ManyToManyField(Section)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)

    def total_weight(self):
        return sum([section.total_weight() for section in self.sections.all()])

    def sections_weight_percentages(self):
        return [
            (section.name, section.total_weight() / self.total_weight())
            for section in self.sections.all()
        ]


class PackType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    packs = models.ManyToManyField(Pack)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def average_pack_weight(self):
        return sum([pack.total_weight() for pack in self.packs.all()]) / len(self.packs.all())