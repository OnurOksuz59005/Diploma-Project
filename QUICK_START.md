# Quick Start Guide - Personal Finance Tracker

## 5-Minute Setup (Windows)

### 1. Open Command Prompt
```
Press Win+R, type cmd, press Enter
```

### 2. Navigate to Project
```
cd "c:\Users\iniro\Desktop\Vizja Projects\Diploma Project"
```

### 3. Run Setup
```
setup.bat
```

This will:
- Create virtual environment
- Install dependencies
- Run database migrations
- Create admin account (follow prompts)

### 4. Start Server
```
run_server.bat
```

### 5. Open Browser
```
http://localhost:8000
```

## First Steps

### Create Your First Account
1. Click "Register" on the home page
2. Enter username, email, and password
3. Click "Register"
4. Login with your credentials

### Add Your First Transaction
1. Go to "Transactions" page
2. Fill in the form:
   - Type: Expense
   - Category: Food & Dining
   - Amount: 25.50
   - Date: Today
   - Description: Lunch
3. Click "Add Transaction"

### Create Your First Budget
1. Go to "Budgets" page
2. Fill in the form:
   - Category: Food & Dining
   - Monthly Limit: 500
   - Month: Current month
   - Year: Current year
3. Click "Create Budget"

### View Your Dashboard
1. Click "Dashboard" in navigation
2. See your income, expenses, and balance
3. View expense breakdown chart
4. Check recent transactions

## Common Tasks

### Add Income
1. Go to Transactions
2. Type: Income
3. Category: Salary (or other income type)
4. Enter amount and date
5. Click "Add Transaction"

### Track Spending
1. Add expenses as you spend
2. Watch budget progress on Budgets page
3. Get alerts when approaching limits
4. Review dashboard for overview

### Analyze Spending
1. View dashboard chart
2. See expenses by category
3. Check monthly summary
4. Adjust budgets as needed

## Troubleshooting

### "Port 8000 already in use"
```
python manage.py runserver 8001
Then open http://localhost:8001
```

### "Database error"
```
python manage.py migrate --run-syncdb
```

### "Static files not loading"
```
python manage.py collectstatic --noinput
```

### "Can't login"
- Check username/password spelling
- Create new account if forgotten
- Check admin panel: http://localhost:8000/admin

## Admin Panel

### Access Admin
1. Go to http://localhost:8000/admin
2. Login with superuser account (created during setup)
3. Manage users, transactions, budgets

### Admin Features
- View all user data
- Create/edit/delete transactions
- Create/edit/delete budgets
- View budget alerts
- Manage user accounts

## Tips & Tricks

### Monthly Review
1. Go to Dashboard
2. Check total income and expenses
3. Review spending by category
4. Plan next month's budget

### Budget Management
- Set realistic budgets
- Review monthly
- Adjust based on actual spending
- Use alerts to stay on track

### Data Entry
- Enter transactions regularly
- Be consistent with categories
- Add descriptions for clarity
- Review for accuracy

## Getting Help

### Documentation
- README.md - Full documentation
- FEATURES.md - Detailed features
- INSTALLATION.md - Installation help
- DEPLOYMENT.md - Production setup

### Common Issues
See INSTALLATION.md Troubleshooting section

### Support
- Check browser console (F12) for errors
- Review application logs
- Check database integrity

## Next Steps

1. **Customize**: Adjust categories and budgets to your needs
2. **Monitor**: Check dashboard regularly
3. **Analyze**: Review spending patterns
4. **Optimize**: Adjust budgets based on data
5. **Plan**: Set financial goals

## Keyboard Shortcuts

- `F12` - Open browser developer tools
- `Ctrl+Shift+Delete` - Clear browser cache
- `Ctrl+L` - Focus address bar

## Mobile Access

The application is responsive and works on mobile devices:
1. Find your computer's IP address
2. On mobile, go to `http://[IP]:8000`
3. Login and use normally

## Backup Your Data

### Manual Backup
```
# Backup database
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

### Automated Backup
See DEPLOYMENT.md for automated backup setup

## Performance Tips

1. **Regularly review data** - Keep database clean
2. **Use categories** - Organize spending
3. **Set budgets** - Monitor spending
4. **Review alerts** - Stay informed
5. **Export reports** - Track progress (future feature)

## Security Reminders

- **Don't share password** - Keep it private
- **Use strong password** - Mix of characters
- **Logout when done** - Especially on shared computers
- **Keep software updated** - Update Python and Django
- **Review transactions** - Check for unauthorized access

## Feedback

To improve the application:
1. Note any issues
2. Suggest features
3. Report bugs
4. Share feedback

---

**Ready to start?** Run `setup.bat` and begin tracking your finances!
