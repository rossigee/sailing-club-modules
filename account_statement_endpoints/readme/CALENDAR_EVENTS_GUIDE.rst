# Calendar Events API Usage Guide

This guide covers how to use the calendar events endpoint to display club activities and schedules on your website.

## Overview

The calendar events API provides access to:
- Public club events and activities
- Training sessions and competitions
- Event details including location, duration, and attendees
- Recurring event information

## Basic Usage

### Get Upcoming Events

```javascript
// Fetch events for the next 30 days
const today = new Date().toISOString().split('T')[0];
const nextMonth = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

const response = await fetch(`https://odoo.bksc.net/calendar/events?start=${today}&end=${nextMonth}`);
const data = await response.json();

console.log(`Found ${data.count} upcoming events`);
```

### Get Events for a Specific Month

```javascript
// Get all events for July 2024
const params = new URLSearchParams({
  start: '2024-07-01',
  end: '2024-07-31',
  limit: 100
});

const response = await fetch(`https://odoo.bksc.net/calendar/events?${params}`);
const data = await response.json();

data.events.forEach(event => {
  console.log(`${event.name} on ${event.start}`);
});
```

## React Calendar Component

```jsx
import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

function ClubCalendar() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadEvents();
  }, []);
  
  const loadEvents = async () => {
    try {
      // Load 3 months of events
      const start = moment().subtract(1, 'month').format('YYYY-MM-DD');
      const end = moment().add(2, 'months').format('YYYY-MM-DD');
      
      const response = await fetch(
        `https://odoo.bksc.net/calendar/events?start=${start}&end=${end}&limit=200`
      );
      const data = await response.json();
      
      // Transform events for react-big-calendar
      const calendarEvents = data.events.map(event => ({
        id: event.id,
        title: event.name,
        start: new Date(event.start),
        end: new Date(event.stop),
        allDay: event.allday,
        resource: event
      }));
      
      setEvents(calendarEvents);
    } catch (error) {
      console.error('Failed to load events:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSelectEvent = (event) => {
    // Show event details
    const details = event.resource;
    alert(`
      Event: ${details.name}
      Location: ${details.location}
      Duration: ${details.duration} hours
      Attendees: ${details.attendees.length}
    `);
  };
  
  if (loading) return <div>Loading calendar...</div>;
  
  return (
    <div style={{ height: 600 }}>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        onSelectEvent={handleSelectEvent}
        views={['month', 'week', 'day']}
        defaultView='month'
      />
    </div>
  );
}
```

## Vue 3 Events List Component

```vue
<template>
  <div class="events-container">
    <h2>Upcoming Events</h2>
    
    <!-- Date Filter -->
    <div class="filters">
      <label>From:</label>
      <input type="date" v-model="startDate" @change="loadEvents">
      <label>To:</label>
      <input type="date" v-model="endDate" @change="loadEvents">
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading">Loading events...</div>
    
    <!-- Events List -->
    <div v-else-if="events.length > 0" class="events-list">
      <div 
        v-for="event in events" 
        :key="event.id" 
        class="event-card"
        :class="{ 'all-day': event.allday }"
      >
        <div class="event-header">
          <h3>{{ event.name }}</h3>
          <span class="event-state" :class="event.state">{{ event.state }}</span>
        </div>
        
        <div class="event-details">
          <p v-if="event.location">
            <i class="icon-location"></i> {{ event.location }}
          </p>
          <p>
            <i class="icon-clock"></i> 
            {{ formatEventTime(event) }}
          </p>
          <p v-if="event.description" class="description">
            {{ event.description }}
          </p>
        </div>
        
        <div v-if="event.attendees.length > 0" class="attendees">
          <span>{{ event.attendees.length }} attendees</span>
          <div class="attendee-avatars">
            <span 
              v-for="attendee in event.attendees.slice(0, 5)" 
              :key="attendee.id"
              class="avatar"
              :title="attendee.name"
            >
              {{ attendee.name.charAt(0) }}
            </span>
            <span v-if="event.attendees.length > 5" class="more">
              +{{ event.attendees.length - 5 }}
            </span>
          </div>
        </div>
        
        <div v-if="event.categories.length > 0" class="categories">
          <span 
            v-for="category in event.categories" 
            :key="category.id"
            class="category-tag"
          >
            {{ category.name }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="empty-state">
      No events found for the selected period.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const events = ref([])
const loading = ref(false)
const startDate = ref(new Date().toISOString().split('T')[0])
const endDate = ref(
  new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
)

onMounted(() => {
  loadEvents()
})

const loadEvents = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      start: startDate.value,
      end: endDate.value,
      limit: 50
    })
    
    const response = await fetch(`https://odoo.bksc.net/calendar/events?${params}`)
    const data = await response.json()
    
    if (data.status === 'ok') {
      events.value = data.events
    }
  } catch (error) {
    console.error('Failed to load events:', error)
  } finally {
    loading.value = false
  }
}

const formatEventTime = (event) => {
  if (event.allday) {
    return 'All day'
  }
  
  const start = new Date(event.start)
  const end = new Date(event.stop)
  const options = { 
    hour: '2-digit', 
    minute: '2-digit',
    day: 'numeric',
    month: 'short'
  }
  
  if (start.toDateString() === end.toDateString()) {
    // Same day
    return `${start.toLocaleDateString('en-US', options)} - ${end.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`
  } else {
    // Multi-day
    return `${start.toLocaleDateString('en-US', options)} - ${end.toLocaleDateString('en-US', options)}`
  }
}
</script>
```

## Mobile-Friendly Event Widget

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .event-widget {
      max-width: 400px;
      margin: 0 auto;
      font-family: Arial, sans-serif;
    }
    .event-item {
      border-left: 4px solid #007bff;
      padding: 10px;
      margin: 10px 0;
      background: #f8f9fa;
    }
    .event-date {
      font-weight: bold;
      color: #666;
    }
    .event-name {
      font-size: 18px;
      margin: 5px 0;
    }
    .event-location {
      color: #666;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div id="events-widget" class="event-widget">
    <h3>Upcoming Events</h3>
    <div id="events-list">Loading...</div>
  </div>

  <script>
    async function loadUpcomingEvents() {
      const widget = document.getElementById('events-list');
      
      try {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(
          `https://odoo.bksc.net/calendar/events?start=${today}&limit=5`
        );
        const data = await response.json();
        
        if (data.events.length === 0) {
          widget.innerHTML = '<p>No upcoming events</p>';
          return;
        }
        
        widget.innerHTML = data.events.map(event => `
          <div class="event-item">
            <div class="event-date">
              ${new Date(event.start).toLocaleDateString()}
            </div>
            <div class="event-name">${event.name}</div>
            ${event.location ? `<div class="event-location">📍 ${event.location}</div>` : ''}
          </div>
        `).join('');
        
      } catch (error) {
        widget.innerHTML = '<p>Failed to load events</p>';
      }
    }
    
    // Load events on page load
    loadUpcomingEvents();
  </script>
</body>
</html>
```

## Handling Recurring Events

Events with `recurrency: true` include an `rrule` field:

```javascript
// Example of handling recurring events
const event = {
  name: "Weekly Training",
  start: "2024-07-01T09:00:00",
  recurrency: true,
  rrule: "FREQ=WEEKLY;BYDAY=SA;UNTIL=20241231"
};

// You can use a library like rrule.js to parse and expand recurring events
import { RRule } from 'rrule';

if (event.recurrency && event.rrule) {
  const rule = RRule.fromString(event.rrule);
  const occurrences = rule.between(
    new Date('2024-07-01'),
    new Date('2024-07-31')
  );
  
  console.log(`This event occurs ${occurrences.length} times in July`);
}
```

## Filtering Events

### By Category

```javascript
// Get only training events
const response = await fetch('https://odoo.bksc.net/calendar/events');
const data = await response.json();

const trainingEvents = data.events.filter(event => 
  event.categories.some(cat => cat.name === 'Training')
);
```

### By Availability

```javascript
// Get only events that show as busy
const busyEvents = data.events.filter(event => event.show_as === 'busy');
```

### By State

```javascript
// Get only confirmed events
const confirmedEvents = data.events.filter(event => event.state === 'open');
```

## Common Use Cases

1. **Event Calendar**: Full calendar view for the club website
2. **Upcoming Events Widget**: Small widget showing next 5 events
3. **Training Schedule**: Filtered view of training sessions only
4. **Competition Calendar**: Show only competition events
5. **Mobile App Integration**: Lightweight event feed for mobile apps
6. **Email Newsletter**: Generate event summaries for newsletters

## Best Practices

1. **Cache Results**: Events don't change frequently - cache for 5-10 minutes
2. **Pagination**: Use the `limit` parameter for better performance
3. **Date Ranges**: Always specify date ranges to avoid loading too much data
4. **Time Zones**: Convert times to user's local timezone for display
5. **Responsive Design**: Design for mobile-first as many users check on phones

## Error Handling Example

```javascript
class EventsAPI {
  constructor(baseUrl = 'https://odoo.bksc.net') {
    this.baseUrl = baseUrl;
    this.cache = new Map();
  }
  
  async getEvents(start, end, options = {}) {
    const cacheKey = `${start}-${end}`;
    
    // Check cache
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < 300000) { // 5 minutes
        return cached.data;
      }
    }
    
    try {
      const params = new URLSearchParams({
        start,
        end,
        limit: options.limit || 50
      });
      
      const response = await fetch(`${this.baseUrl}/calendar/events?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.status === 'error') {
        throw new Error(data.error);
      }
      
      // Cache successful response
      this.cache.set(cacheKey, {
        data: data.events,
        timestamp: Date.now()
      });
      
      return data.events;
      
    } catch (error) {
      console.error('Failed to fetch events:', error);
      
      // Return cached data if available
      if (this.cache.has(cacheKey)) {
        return this.cache.get(cacheKey).data;
      }
      
      throw error;
    }
  }
}

// Usage
const api = new EventsAPI();
const events = await api.getEvents('2024-07-01', '2024-07-31');
```