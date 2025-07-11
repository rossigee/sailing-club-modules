# BKSC Digest Module

This module extends Odoo's digest functionality to include Bangkok Sailing Club specific content in the periodic digest emails.

## Features

- **Bank Statement Summaries**: Shows recent bank statements with balances and transaction counts
- **Recent Transactions**: Displays the latest 10 transactions with amounts
- **Account Balance Summary**: Shows current balances for all cash and bank accounts
- **KPI Tracking**: Tracks number of statements, transactions, and total cash balance

## Installation

1. Install the module through Odoo Apps or Settings > Apps
2. The module depends on:
   - `digest` (Odoo standard digest module)
   - `account_statement_endpoints` (BKSC bank statement module)
   - `account` (Odoo accounting)

## Configuration

### Enable Digest Emails

1. Go to **Settings > General Settings**
2. In the **Discuss** section, enable **Digest Emails**
3. Click **Save**

### Configure Digest Content

1. Go to **Settings > Technical > Email > Digest Emails** (or use the menu **BKSC Digest Configuration**)
2. Create a new digest or edit the existing one
3. Set the following:
   - **Name**: e.g., "BKSC Weekly Digest"
   - **Periodicity**: Daily, Weekly, or Monthly
   - **Next Run Date**: When to send the first digest
   - **Available for**: Which users should receive it

4. In the **BKSC Metrics** section, enable:
   - **Bank Statements Summary**: Shows recent bank statements
   - **Recent Transactions**: Shows latest transactions
   - **Account Balance Summary**: Shows account balances

### User Subscription

Users can manage their digest subscription:
1. Go to **My Profile** (user menu)
2. In **Preferences** tab, find **Digest Emails**
3. Choose frequency: Daily, Weekly, Monthly, or Disabled

## Email Content

The digest email will include:

### Standard Odoo KPIs
- Your regular Odoo metrics (if enabled)

### BKSC Specific Content
- **Recent Bank Statements**: Table showing date, journal, balance, and transaction count
- **Recent Transactions**: Table with date, description, and amount (color-coded)
- **Account Balances**: Summary of all cash and bank accounts with total

## Customization

To add more content sections:

1. Extend the `digest.digest` model to add new KPI fields
2. Add computation methods for the KPIs
3. Extend `digest.bksc` model to add content generation methods
4. Update the email template in `data/digest_data.xml`

## Testing

To test the digest immediately:
1. Go to the digest record
2. Click **Send Now** button
3. Check the recipient's email

## Troubleshooting

- **No emails received**: Check Settings > General Settings > Discuss > Digest Emails is enabled
- **Missing content**: Ensure the BKSC KPIs are enabled in the digest configuration
- **Wrong recipients**: Check the digest's "Available for" setting and user preferences