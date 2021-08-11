from django.db.models import Model
from django.db.models import CharField, DateField, TextField
from django.db.models import ManyToManyField


class ProjectTag(Model):
    project_tag_name = CharField(max_length=100)

    def __str__(self):
        return self.project_tag_name


class Project(Model):
    # 名前
    project_name = CharField(max_length=200)
    start_date = DateField(blank=True, null=True)
    tags = ManyToManyField(ProjectTag, blank=True)
    memo = TextField('備考', max_length=50, blank=True)

    def __str__(self):
        return self.project_name
