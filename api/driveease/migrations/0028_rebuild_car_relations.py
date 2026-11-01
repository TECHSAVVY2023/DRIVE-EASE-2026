from django.db import migrations, models
import django.db.models.deletion


def remove_existing_bookings(apps, schema_editor):
    Booking = apps.get_model("driveease", "Booking")
    Booking.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("driveease", "0027_rename_car_id_cars_car_reference"),
    ]

    operations = [
        migrations.RunPython(
            remove_existing_bookings,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="booking",
            name="car",
        ),
        migrations.RemoveField(
            model_name="cars",
            name="features",
        ),
        migrations.AddField(
            model_name="booking",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="driveease.cars",
            ),
        ),
        migrations.AddField(
            model_name="cars",
            name="features",
            field=models.ManyToManyField(
                blank=True,
                related_name="cars",
                to="driveease.feature",
            ),
        ),
    ]
