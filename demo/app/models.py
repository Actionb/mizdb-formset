from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class PhoneNumber(models.Model):
    label = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.label}: {self.number}"

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
