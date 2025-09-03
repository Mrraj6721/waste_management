# Generated manually to avoid rename issues

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='authority_response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='notified_authorities',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='reported_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='reported_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
        migrations.AddField(
            model_name='report',
            name='severity',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium', max_length=20),
        ),
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Review'), ('confirmed', 'Confirmed'), ('in_progress', 'Cleanup In Progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='report',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='waste_type',
            field=models.CharField(choices=[('plastic', 'Plastic Waste'), ('organic', 'Organic Waste'), ('construction', 'Construction Debris'), ('electronic', 'Electronic Waste'), ('medical', 'Medical Waste'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-reported_at']},
        ),
    ]
