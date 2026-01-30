from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('food', 'Food & Dining'), ('transport', 'Transport'), ('utilities', 'Utilities'), ('entertainment', 'Entertainment'), ('shopping', 'Shopping'), ('health', 'Health & Fitness'), ('education', 'Education'), ('other', 'Other')], max_length=20)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-year', '-month', 'category'],
                'unique_together': {('user', 'category', 'month', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=10)),
                ('category', models.CharField(choices=[('food', 'Food & Dining'), ('transport', 'Transport'), ('utilities', 'Utilities'), ('entertainment', 'Entertainment'), ('shopping', 'Shopping'), ('health', 'Health & Fitness'), ('education', 'Education'), ('salary', 'Salary'), ('freelance', 'Freelance'), ('investment', 'Investment'), ('other', 'Other')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('description', models.CharField(blank=True, max_length=255)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BudgetAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_type', models.CharField(choices=[('warning', 'Warning (75%)'), ('critical', 'Critical (90%)')], max_length=10)),
                ('spent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='tracker.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_alerts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', '-date'], name='tracker_tran_user_id_date_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', 'type'], name='tracker_tran_user_id_type_idx'),
        ),
    ]
