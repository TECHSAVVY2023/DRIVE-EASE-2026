from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


def migrate_car_types(apps, schema_editor):
    Cars = apps.get_model("driveease", "Cars")
    CarType = apps.get_model("driveease", "CarType")
    db = schema_editor.connection.alias

    # Preserve the existing car type values.
    existing_types = (
        Cars.objects.using(db)
        .values_list("car_type", flat=True)
        .distinct()
    )

    type_map = {
        "sedan": "Sedan",
        "suv": "SUV",
        "truck": "Truck",
        "van": "Van",
        "hatchback": "Hatchback",
        "pickup": "Pickup",
        "other": "Other",
    }

    for old_type in existing_types:
        if not old_type:
            continue

        name = type_map.get(old_type.lower(), old_type.title())

        car_type, _ = CarType.objects.using(db).get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )

        Cars.objects.using(db).filter(
            car_type=old_type
        ).update(car_type_new=car_type)


class Migration(migrations.Migration):

    dependencies = [
        (
            "driveease",
            "0018_remove_booking_location_booking_pickup_location_and_more",
        ),
    ]

    operations = [
        # 1. Create the CarType table.
        migrations.CreateModel(
            name="CarType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),

        # 2. Add a temporary nullable foreign key.
        migrations.AddField(
            model_name="cars",
            name="car_type_new",
            field=models.ForeignKey(
                to="driveease.cartype",
                on_delete=django.db.models.deletion.PROTECT,
                null=True,
                blank=True,
                related_name="+",
            ),
        ),

        # 3. Create car types and map existing cars to them.
        migrations.RunPython(
            migrate_car_types,
            reverse_code=migrations.RunPython.noop,
        ),

        # 4. Remove the old string field.
        migrations.RemoveField(
            model_name="cars",
            name="car_type",
        ),

        # 5. Rename the temporary foreign key to car_type.
        migrations.RenameField(
            model_name="cars",
            old_name="car_type_new",
            new_name="car_type",
        ),

        # 6. Make the foreign key required.
        migrations.AlterField(
            model_name="cars",
            name="car_type",
            field=models.ForeignKey(
                to="driveease.cartype",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cars",
            ),
        ),
    ]