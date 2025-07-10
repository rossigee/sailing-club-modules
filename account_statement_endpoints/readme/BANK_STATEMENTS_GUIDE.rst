# Bank Statements API Usage Guide

This guide covers how to use the bank statement endpoints to display financial information on your website.

## Overview

The bank statements API provides access to:
- Bank account journals with current balances
- Historical bank statements
- Individual transaction details
- Statement attachments (scanned documents)

## Typical Usage Flow

1. **Display Account Overview** → `/bank/journals`
2. **Show Statement List** → `/bank/statements/BANK`
3. **View Statement Details** → `/bank/statements/BANK/31`
4. **Display Attachments** → `/bank/statements/image/123`

## Endpoint Details

### 1. Get All Bank Accounts

```javascript
// Fetch all public bank accounts
const response = await fetch('https://odoo.bksc.net/bank/journals');
const data = await response.json();

// Display total balance
console.log(`Total Balance: ${data.total_balance}`);

// Display each account
data.journals.forEach(journal => {
  console.log(`${journal.name}: ${journal.latest_statement.balance_end}`);
});
```

**Use Case:** Homepage dashboard showing all account balances

### 2. Get Statements for an Account

```javascript
// Fetch statements for the BANK account
const slug = 'BANK'; // from journal.public_slug
const response = await fetch(`https://odoo.bksc.net/bank/statements/${slug}`);
const data = await response.json();

// Display account info
console.log(`Account: ${data.account.name}`);
console.log(`Bank: ${data.account.bankname}`);
console.log(`Number: ${data.account.number}`);

// List statements
data.statements.forEach(statement => {
  console.log(`${statement.date}: ${statement.name} - Balance: ${statement.balance_end}`);
});
```

**Use Case:** Account detail page showing statement history

### 3. Get Statement Transaction Details

```javascript
// Fetch details for a specific statement
const slug = 'BANK';
const statementId = 31;
const response = await fetch(`https://odoo.bksc.net/bank/statements/${slug}/${statementId}`);
const data = await response.json();

// Display header info
console.log(`Statement: ${data.header.name}`);
console.log(`Date: ${data.header.date}`);
console.log(`Starting Balance: ${data.header.balance_start}`);
console.log(`Ending Balance: ${data.header.balance_end}`);

// Display transactions
data.lines.forEach(line => {
  console.log(`${line.date}: ${line.payment_ref} - Amount: ${line.amount}`);
});

// Show attachments
data.attachments.forEach(att => {
  console.log(`Attachment: ${att.description}`);
  console.log(`View: ${att.url}`);
});
```

**Use Case:** Detailed statement view with all transactions

### 4. Display Statement Images

```html
<!-- Display scanned statement images -->
<div class="attachments">
  <h3>Scanned Documents</h3>
  <img src="https://odoo.bksc.net/bank/statements/image/123" 
       alt="Bank statement scan" 
       class="statement-image" />
</div>
```

**Use Case:** Showing scanned bank statement documents

## React Component Example

```jsx
import React, { useState, useEffect } from 'react';

function BankStatements() {
  const [journals, setJournals] = useState(null);
  const [selectedJournal, setSelectedJournal] = useState(null);
  const [statements, setStatements] = useState(null);
  
  // Load journals on mount
  useEffect(() => {
    fetch('https://odoo.bksc.net/bank/journals')
      .then(res => res.json())
      .then(data => setJournals(data));
  }, []);
  
  // Load statements when journal selected
  const selectJournal = async (slug) => {
    const res = await fetch(`https://odoo.bksc.net/bank/statements/${slug}`);
    const data = await res.json();
    setSelectedJournal(slug);
    setStatements(data);
  };
  
  if (!journals) return <div>Loading...</div>;
  
  return (
    <div>
      <h2>Bank Accounts</h2>
      <div className="total-balance">
        Total Balance: {journals.total_balance.toLocaleString()} THB
      </div>
      
      <div className="journals">
        {journals.journals.map(journal => (
          <div 
            key={journal.id} 
            className="journal-card"
            onClick={() => selectJournal(journal.public_slug)}
          >
            <h3>{journal.name}</h3>
            <p>Balance: {journal.latest_statement.balance_end.toLocaleString()} THB</p>
            <p>Last updated: {journal.latest_statement.date}</p>
          </div>
        ))}
      </div>
      
      {statements && (
        <div className="statements">
          <h3>{statements.account.name} - Statements</h3>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Reference</th>
                <th>Balance</th>
                <th>Attachments</th>
              </tr>
            </thead>
            <tbody>
              {statements.statements.map(stmt => (
                <tr key={stmt.id}>
                  <td>{stmt.date}</td>
                  <td>{stmt.name}</td>
                  <td>{stmt.balance_end.toLocaleString()} THB</td>
                  <td>{stmt.attachments.length} files</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
```

## Vue 3 Component Example

```vue
<template>
  <div class="bank-statements">
    <h2>Bank Accounts</h2>
    
    <!-- Total Balance -->
    <div v-if="journals" class="total-balance">
      Total Balance: {{ formatCurrency(journals.total_balance) }}
    </div>
    
    <!-- Journal Cards -->
    <div v-if="journals" class="journals-grid">
      <div 
        v-for="journal in journals.journals" 
        :key="journal.id"
        class="journal-card"
        @click="loadStatements(journal.public_slug)"
      >
        <h3>{{ journal.name }}</h3>
        <p class="balance">{{ formatCurrency(journal.latest_statement.balance_end) }}</p>
        <p class="date">Updated: {{ formatDate(journal.latest_statement.date) }}</p>
      </div>
    </div>
    
    <!-- Statements List -->
    <div v-if="statements" class="statements-section">
      <h3>{{ statements.account.name }} - Statements</h3>
      <div 
        v-for="statement in statements.statements" 
        :key="statement.id"
        class="statement-row"
        @click="loadStatementDetail(statement.id)"
      >
        <span>{{ formatDate(statement.date) }}</span>
        <span>{{ statement.name }}</span>
        <span>{{ formatCurrency(statement.balance_end) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const journals = ref(null)
const statements = ref(null)
const currentSlug = ref(null)

onMounted(async () => {
  const response = await fetch('https://odoo.bksc.net/bank/journals')
  journals.value = await response.json()
})

const loadStatements = async (slug) => {
  currentSlug.value = slug
  const response = await fetch(`https://odoo.bksc.net/bank/statements/${slug}`)
  statements.value = await response.json()
}

const loadStatementDetail = async (statementId) => {
  const response = await fetch(`https://odoo.bksc.net/bank/statements/${currentSlug.value}/${statementId}`)
  const detail = await response.json()
  // Handle statement detail display
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('th-TH', {
    style: 'currency',
    currency: 'THB'
  }).format(amount)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('th-TH')
}
</script>
```

## Error Handling

Always handle potential errors:

```javascript
try {
  const response = await fetch('https://odoo.bksc.net/bank/journals');
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const data = await response.json();
  
  if (data.status === 'error') {
    console.error('API Error:', data.error);
    // Show user-friendly error message
  } else {
    // Process successful response
  }
} catch (error) {
  console.error('Network error:', error);
  // Show offline/network error message
}
```

## Security Considerations

1. **Public Data Only**: These endpoints only return data from journals marked with `public_can_view = True`
2. **No Authentication**: These are public endpoints - do not use for sensitive operations
3. **Read-Only**: All endpoints are GET requests - no data modification is possible
4. **Rate Limiting**: Consider implementing rate limiting on your frontend to prevent abuse

## Common Use Cases

1. **Public Financial Transparency**: Display account balances for club members
2. **Donation Tracking**: Show incoming donations with transaction details
3. **Financial Reports**: Generate monthly/yearly financial summaries
4. **Audit Trail**: Provide scanned statement documents for verification