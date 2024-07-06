from django.db import models
from general.models import AuditFields


class AssetCategory(AuditFields):
    """
    Model to represent different asset categories.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Asset Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Asset(AuditFields):
    """
    Model to represent an asset entry.
    """

    category = models.ForeignKey(
        AssetCategory, on_delete=models.SET_NULL, null=True, related_name="assets"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()
    receipt_image = models.ImageField(
        upload_to="assets_receipts/", blank=True, null=True
    )

    class Meta:
        ordering = ["-purchase_date", "-created_date"]

    def __str__(self):
        return f"{self.name} - {self.value} ({self.category.name if self.category else 'No Category'})"


class Depreciation(AuditFields):
    """
    Model to represent depreciation of assets.
    """

    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="depreciations"
    )
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Depreciation: {self.value} on {self.date}"
