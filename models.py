"""Database models for Affordances project."""

from django.db import models


class Participant(models.Model):
    """Class to store participant data."""

    # Identify ppt
    ip_address = models.TextField()
    key = models.TextField()  # Generated passphrase to credit ppt
    SONA_code = models.TextField(default="")  # SONA participant code
    get_args = models.TextField(default="")  # Get args issued with request
    notes = models.TextField(default="")  # Miscellaneous notes

    # Device
    ua_header = models.TextField(default="")
    screen_width = models.TextField(default="")
    screen_height = models.TextField(default="")

    # Validation
    captcha_score = models.FloatField(blank=True, null=True)

    # Experiment
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    # Demographics
    birth_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=2)
    native_english = models.BooleanField(blank=True, null=True)

    # Feedback
    post_test_purpose = models.TextField(default="")
    post_test_other = models.TextField(default="")


class Rating(models.Model):
    """Responses to likert-style rating questions."""
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )

    # Scales
    IRQ = "IRQ"
    SENSIBILITY = "SENSIBILITY"
    ENVISIONING = "ENVISIONING"
    SCALES = [
        (IRQ, "IRQ"),
        (SENSIBILITY, "Sensibility"),
        (ENVISIONING, "Envisioning")
    ]
    scale = models.CharField(
        max_length=11,
        choices=SCALES
    )

    # Item identifier
    item = models.IntegerField(blank=True, null=True)  # Item No.
    item_id = models.CharField(max_length=80)  # Unique (to scale) Item ID
    item_type = models.CharField(  # Critical/filler etc
        max_length=80, blank=True)
    version = models.CharField(  # Item version
        max_length=80, default="", blank=True)
    condition = models.CharField(  # Condition
        max_length=80, default="", blank=True)
    trial_index = models.IntegerField(blank=True, null=True)  # Index for ppt

    # Response info
    response = models.IntegerField()  # Participant response to question
    reaction_time = models.FloatField()  # RT in ms


class BinaryChoice(models.Model):
    """Responses to binary choice questions."""
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )

    # Tasks
    TASKS = [
        ("MR", "Mental Rotation")
    ]
    task = models.CharField(
        max_length=2,
        choices=TASKS
    )

    # Item identifier
    item = models.IntegerField(blank=True, null=True)  # Item No.
    item_id = models.CharField(max_length=10)  # Unique Item ID within task
    item_type = models.CharField(  # Critical/Filler etc
        max_length=80, blank=True)
    version = models.CharField(  # Item version
        max_length=10, blank=True, default="")
    condition = models.CharField(
        max_length=10, blank=True, default="")  # Condition
    trial_index = models.IntegerField(blank=True, null=True)  # Index for ppt

    # Response info
    key_press = models.CharField(  # Key pressed
        max_length=10,
        default="")
    response = models.CharField(  # Participant response to question
        max_length=10,
        default="")
    correct_response = models.CharField(  # Ground truth answer
        max_length=10,
        default="")
    is_correct = models.BooleanField()  # response == correct_response
    reaction_time = models.FloatField()  # RT in ms


class FreeResponse(models.Model):
    """Responses to free response questions."""

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )

    # Tasks
    TASKS = [
        ("AU", "Alternative Uses")
    ]
    task = models.CharField(
        max_length=2,
        choices=TASKS
    )

    # Item identifier
    item = models.IntegerField(blank=True, null=True)  # Item No.
    item_id = models.CharField(max_length=80)  # Unique (to scale) Item ID
    item_type = models.CharField(  # Critical/filler etc
        max_length=80, blank=True)
    version = models.CharField(  # Item version
        max_length=80, default="", blank=True)
    condition = models.CharField(  # Condition
        max_length=80, default="", blank=True)
    trial_index = models.IntegerField(blank=True, null=True)  # Index for ppt

    # Response info
    response = models.TextField()  # Participant response to question
    reaction_time = models.FloatField()  # RT in ms
