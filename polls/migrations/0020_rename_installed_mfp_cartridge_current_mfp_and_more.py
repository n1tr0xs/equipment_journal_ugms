# Generated by Django 5.1.2 on 2024-10-23 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_remove_cartridge_mfp_cartridge_installed_mfp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartridge',
            old_name='installed_mfp',
            new_name='current_mfp',
        ),
        migrations.RenameField(
            model_name='mfp',
            old_name='current_cartridge',
            new_name='installed_cartridge',
        ),
    ]