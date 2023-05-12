# Generated by Django 3.1.3 on 2020-12-09 10:30

import django.db.models.deletion
from django.db import migrations, models


def create_through_product_relations(apps, schema_editor):
    AssignedProductAttribute = apps.get_model("attribute", "AssignedProductAttribute")
    AssignedProductAttributeValue = apps.get_model(
        "attribute", "AssignedProductAttributeValue"
    )
    for assignment in AssignedProductAttribute.objects.iterator():
        instances = [
            AssignedProductAttributeValue(value=value, assignment=assignment)
            for value in assignment.values.all()
        ]
        AssignedProductAttributeValue.objects.bulk_create(instances)


def create_through_variant_relations(apps, schema_editor):
    AssignedVariantAttribute = apps.get_model("attribute", "AssignedVariantAttribute")
    AssignedVariantAttributeValue = apps.get_model(
        "attribute", "AssignedVariantAttributeValue"
    )
    for assignment in AssignedVariantAttribute.objects.iterator():
        instances = [
            AssignedVariantAttributeValue(value=value, assignment=assignment)
            for value in assignment.values.all()
        ]
        AssignedVariantAttributeValue.objects.bulk_create(instances)


def create_through_page_relations(apps, schema_editor):
    AssignedPageAttribute = apps.get_model("attribute", "AssignedPageAttribute")
    AssignedPageAttributeValue = apps.get_model(
        "attribute", "AssignedPageAttributeValue"
    )
    for assignment in AssignedPageAttribute.objects.iterator():
        instances = [
            AssignedPageAttributeValue(value=value, assignment=assignment)
            for value in assignment.values.all()
        ]
        AssignedPageAttributeValue.objects.bulk_create(instances)


class Migration(migrations.Migration):

    dependencies = [
        ("attribute", "0004_auto_20201204_1325"),
    ]

    operations = [
        # create new through models
        migrations.CreateModel(
            name="AssignedProductAttributeValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(db_index=True, editable=False, null=True),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="productvalueassignment",
                        to="attribute.assignedproductattribute",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="productvalueassignment",
                        to="attribute.attributevalue",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order", "pk"),
                "unique_together": {("value", "assignment")},
            },
        ),
        migrations.CreateModel(
            name="AssignedVariantAttributeValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(db_index=True, editable=False, null=True),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variantvalueassignment",
                        to="attribute.assignedvariantattribute",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variantvalueassignment",
                        to="attribute.attributevalue",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order", "pk"),
                "unique_together": {("value", "assignment")},
            },
        ),
        migrations.CreateModel(
            name="AssignedPageAttributeValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(db_index=True, editable=False, null=True),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pagevalueassignment",
                        to="attribute.assignedpageattribute",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pagevalueassignment",
                        to="attribute.attributevalue",
                    ),
                ),
            ],
            options={
                "ordering": ("sort_order", "pk"),
                "unique_together": {("value", "assignment")},
            },
        ),
        # migrate existing data to through model
        migrations.RunPython(
            create_through_product_relations, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            create_through_variant_relations, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            create_through_page_relations, reverse_code=migrations.RunPython.noop
        ),
        # remove current `values` relations
        migrations.RemoveField(
            model_name="assignedproductattribute",
            name="values",
        ),
        migrations.RemoveField(
            model_name="assignedvariantattribute",
            name="values",
        ),
        migrations.RemoveField(
            model_name="assignedpageattribute",
            name="values",
        ),
        # create new values relations with use of through models
        migrations.AddField(
            model_name="assignedproductattribute",
            name="values",
            field=models.ManyToManyField(
                blank=True,
                related_name="productassignments",
                through="attribute.AssignedProductAttributeValue",
                to="attribute.AttributeValue",
            ),
        ),
        migrations.AddField(
            model_name="assignedvariantattribute",
            name="values",
            field=models.ManyToManyField(
                blank=True,
                related_name="variantassignments",
                through="attribute.AssignedVariantAttributeValue",
                to="attribute.AttributeValue",
            ),
        ),
        migrations.AddField(
            model_name="assignedpageattribute",
            name="values",
            field=models.ManyToManyField(
                blank=True,
                related_name="pageassignments",
                through="attribute.AssignedPageAttributeValue",
                to="attribute.AttributeValue",
            ),
        ),
    ]
