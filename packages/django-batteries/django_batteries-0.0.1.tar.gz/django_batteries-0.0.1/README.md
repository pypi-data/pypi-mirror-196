# Django-batteries

This package contains useful utilities for django/drf project

## Models

Contains set of abstract models to enforce DRY principle for most common use cases

### TimeStampedModel

- `created`
- `modified`

### TimeFramedModel

- `start`
- `end`

  For time bound entities

### DescriptionModel

- `description`

### TitleModel

- `title`

### TitleDescriptionModel

- `title`
- `description`

## Fields

### Monitor field

A DateTimeField that monitors another field on the same model and sets itself to the current date/time whenever the monitored field
changes.
use it like this in your models:
class MyMode(models.Model):

    title = models.Charfield(max_length=50)
    title_changed = MonitorField(_('title changed'), monitor='title')

## Tests
