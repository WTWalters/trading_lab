# Generated manually for demonstrative purposes

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_tradelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeChecklistStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_item', models.CharField(help_text='The checklist item text', max_length=255)),
                ('is_checked', models.BooleanField(default=False, help_text='Whether the checklist item is checked or not')),
                ('trade_log', models.ForeignKey(help_text='The trade log this checklist item is associated with', on_delete=django.db.models.deletion.CASCADE, related_name='checklist_items', to='dashboard.tradelog')),
            ],
            options={
                'verbose_name': 'Trade Checklist Item',
                'verbose_name_plural': 'Trade Checklist Items',
                'ordering': ['id'],
                'unique_together': {('trade_log', 'checklist_item')},
            },
        ),
    ]
