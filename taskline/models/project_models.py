from django.db import models


class ProjectTag(models.Model):
    project_tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_tag_name


class Project(models.Model):
    # 名前
    project_name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(ProjectTag, blank=True)
    memo = models.TextField('備考', max_length=50, blank=True)

    def __str__(self):
        return self.project_name
