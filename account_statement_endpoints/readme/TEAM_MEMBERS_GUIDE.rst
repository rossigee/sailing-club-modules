# Team Members API Usage Guide

This guide covers how to use the team members endpoint to display contact information for club staff and instructors on your website.

## Overview

The team members API provides access to:
- Team member names and roles
- Contact information (email, phone, mobile)
- Profile images
- Job functions/positions
- Optional website and social media links

## Basic Usage

### Get All Team Members

```javascript
// Fetch all team members
const response = await fetch('https://odoo.bksc.net/team/members');
const data = await response.json();

console.log(`Found ${data.count} team members`);

data.members.forEach(member => {
  console.log(`${member.name} - ${member.function}`);
  console.log(`Email: ${member.email}`);
  console.log(`Phone: ${member.phone}`);
});
```

## React Team Component

```jsx
import React, { useState, useEffect } from 'react';

function TeamMembers() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadTeamMembers();
  }, []);
  
  const loadTeamMembers = async () => {
    try {
      const response = await fetch('https://odoo.bksc.net/team/members');
      const data = await response.json();
      
      if (data.status === 'ok') {
        setMembers(data.members);
      }
    } catch (error) {
      console.error('Failed to load team members:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) return <div>Loading team...</div>;
  
  return (
    <div className="team-section">
      <h2>Our Team</h2>
      <div className="team-grid">
        {members.map(member => (
          <TeamMemberCard key={member.id} member={member} />
        ))}
      </div>
    </div>
  );
}

function TeamMemberCard({ member }) {
  const baseUrl = 'https://odoo.bksc.net';
  const imageUrl = member.image_url 
    ? `${baseUrl}${member.image_url}` 
    : '/default-avatar.png';
  
  return (
    <div className="team-member-card">
      <img 
        src={imageUrl} 
        alt={member.name}
        className="member-photo"
        onError={(e) => {
          e.target.src = '/default-avatar.png';
        }}
      />
      
      <div className="member-info">
        <h3>{member.name}</h3>
        <p className="member-role">{member.function}</p>
        
        <div className="contact-info">
          {member.email && (
            <a href={`mailto:${member.email}`} className="contact-link">
              <i className="icon-email"></i> {member.email}
            </a>
          )}
          
          {member.phone && (
            <a href={`tel:${member.phone}`} className="contact-link">
              <i className="icon-phone"></i> {member.phone}
            </a>
          )}
          
          {member.mobile && (
            <a href={`tel:${member.mobile}`} className="contact-link">
              <i className="icon-mobile"></i> {member.mobile}
            </a>
          )}
          
          {member.website && (
            <a 
              href={member.website} 
              target="_blank" 
              rel="noopener noreferrer"
              className="contact-link"
            >
              <i className="icon-web"></i> Website
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
```

## Vue 3 Team Component

```vue
<template>
  <div class="team-members">
    <h2>{{ $t('team.title') }}</h2>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>{{ $t('team.loading') }}</p>
    </div>
    
    <!-- Team Grid -->
    <div v-else-if="members.length > 0" class="team-grid">
      <div 
        v-for="member in members" 
        :key="member.id" 
        class="member-card"
      >
        <!-- Member Photo -->
        <div class="member-photo-wrapper">
          <img 
            :src="getMemberPhotoUrl(member)"
            :alt="member.name"
            @error="handleImageError"
            class="member-photo"
          />
        </div>
        
        <!-- Member Info -->
        <div class="member-details">
          <h3>{{ member.name }}</h3>
          <p class="member-function">{{ member.function }}</p>
          
          <!-- Contact Methods -->
          <div class="contact-methods">
            <a 
              v-if="member.email" 
              :href="`mailto:${member.email}`"
              class="contact-btn email"
              :title="$t('team.emailTitle')"
            >
              <EmailIcon />
              <span class="contact-text">{{ member.email }}</span>
            </a>
            
            <a 
              v-if="member.phone" 
              :href="`tel:${member.phone}`"
              class="contact-btn phone"
              :title="$t('team.phoneTitle')"
            >
              <PhoneIcon />
              <span class="contact-text">{{ member.phone }}</span>
            </a>
            
            <a 
              v-if="member.mobile" 
              :href="`tel:${member.mobile}`"
              class="contact-btn mobile"
              :title="$t('team.mobileTitle')"
            >
              <MobileIcon />
              <span class="contact-text">{{ member.mobile }}</span>
            </a>
            
            <a 
              v-if="member.website" 
              :href="member.website"
              target="_blank"
              rel="noopener noreferrer"
              class="contact-btn website"
              :title="$t('team.websiteTitle')"
            >
              <WebIcon />
              <span class="contact-text">{{ $t('team.website') }}</span>
            </a>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="empty-state">
      <p>{{ $t('team.noMembers') }}</p>
    </div>
    
    <!-- Error State -->
    <div v-if="error" class="error-state">
      <p>{{ $t('team.error') }}</p>
      <button @click="retry" class="retry-btn">
        {{ $t('common.retry') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const members = ref([])
const loading = ref(false)
const error = ref(null)
const baseUrl = 'https://odoo.bksc.net'

onMounted(() => {
  loadTeamMembers()
})

const loadTeamMembers = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${baseUrl}/team/members`)
    const data = await response.json()
    
    if (data.status === 'ok') {
      members.value = data.members
    } else {
      throw new Error(data.error || 'Unknown error')
    }
  } catch (err) {
    console.error('Failed to load team members:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const getMemberPhotoUrl = (member) => {
  if (member.image_url) {
    return `${baseUrl}${member.image_url}`
  }
  return '/images/default-avatar.png'
}

const handleImageError = (event) => {
  event.target.src = '/images/default-avatar.png'
}

const retry = () => {
  loadTeamMembers()
}
</script>

<style scoped>
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.member-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
}

.member-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.member-photo {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.member-details {
  padding: 1.5rem;
}

.member-function {
  color: #666;
  margin: 0.5rem 0 1rem;
}

.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s;
}

.contact-btn:hover {
  background-color: #f5f5f5;
}
</style>
```

## Static HTML Implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Our Team</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f5f5f5;
    }
    
    .team-container {
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .team-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    
    .team-member {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    
    .member-image {
      width: 100%;
      height: 200px;
      object-fit: cover;
      background-color: #ddd;
    }
    
    .member-info {
      padding: 20px;
    }
    
    .member-name {
      font-size: 20px;
      font-weight: bold;
      margin: 0 0 5px;
    }
    
    .member-role {
      color: #666;
      margin: 0 0 15px;
    }
    
    .contact-links {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    
    .contact-links li {
      margin: 5px 0;
    }
    
    .contact-links a {
      color: #0066cc;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .contact-links a:hover {
      text-decoration: underline;
    }
    
    .icon {
      width: 16px;
      height: 16px;
    }
    
    .loading {
      text-align: center;
      padding: 40px;
    }
    
    .error {
      background: #fee;
      color: #c00;
      padding: 20px;
      border-radius: 4px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="team-container">
    <h1>Our Team</h1>
    <div id="team-members" class="team-grid">
      <div class="loading">Loading team members...</div>
    </div>
  </div>

  <script>
    const baseUrl = 'https://odoo.bksc.net';
    
    async function loadTeamMembers() {
      const container = document.getElementById('team-members');
      
      try {
        const response = await fetch(`${baseUrl}/team/members`);
        const data = await response.json();
        
        if (data.status === 'ok' && data.members.length > 0) {
          container.innerHTML = data.members.map(member => `
            <div class="team-member">
              <img 
                src="${member.image_url ? baseUrl + member.image_url : 'default-avatar.png'}" 
                alt="${member.name}"
                class="member-image"
                onerror="this.src='default-avatar.png'"
              />
              <div class="member-info">
                <h2 class="member-name">${member.name}</h2>
                <p class="member-role">${member.function || 'Team Member'}</p>
                <ul class="contact-links">
                  ${member.email ? `
                    <li>
                      <a href="mailto:${member.email}">
                        <span class="icon">📧</span>
                        ${member.email}
                      </a>
                    </li>
                  ` : ''}
                  ${member.phone ? `
                    <li>
                      <a href="tel:${member.phone}">
                        <span class="icon">📞</span>
                        ${member.phone}
                      </a>
                    </li>
                  ` : ''}
                  ${member.mobile ? `
                    <li>
                      <a href="tel:${member.mobile}">
                        <span class="icon">📱</span>
                        ${member.mobile}
                      </a>
                    </li>
                  ` : ''}
                  ${member.website ? `
                    <li>
                      <a href="${member.website}" target="_blank" rel="noopener">
                        <span class="icon">🌐</span>
                        Website
                      </a>
                    </li>
                  ` : ''}
                </ul>
              </div>
            </div>
          `).join('');
        } else {
          container.innerHTML = '<div class="error">No team members found</div>';
        }
      } catch (error) {
        console.error('Error loading team members:', error);
        container.innerHTML = '<div class="error">Failed to load team members</div>';
      }
    }
    
    // Load on page load
    loadTeamMembers();
  </script>
</body>
</html>
```

## Styling Considerations

### Responsive Design

```css
/* Mobile-first approach */
.team-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

/* Tablet */
@media (min-width: 768px) {
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .team-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

/* Large screens */
@media (min-width: 1440px) {
  .team-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Accessibility

```html
<!-- Ensure proper ARIA labels and semantic HTML -->
<article class="team-member" role="article" aria-label="Team member profile">
  <img 
    src="..." 
    alt="Portrait of John Doe" 
    loading="lazy"
  />
  <h3 id="member-1-name">John Doe</h3>
  <p aria-labelledby="member-1-name">Sailing Instructor</p>
  
  <address>
    <a href="mailto:john@example.com" aria-label="Email John Doe">
      <span aria-hidden="true">📧</span>
      john@example.com
    </a>
  </address>
</article>
```

## Common Use Cases

1. **About Us Page**: Display full team with detailed contact info
2. **Contact Page**: Show key contacts for different departments
3. **Instructor Profiles**: Detailed pages for each instructor
4. **Emergency Contacts**: Quick-access contact list for safety
5. **Staff Directory**: Internal directory for members
6. **Mobile App Contacts**: Lightweight contact list for apps

## Caching Strategy

```javascript
class TeamMembersCache {
  constructor() {
    this.cache = null;
    this.cacheTime = null;
    this.cacheValidity = 3600000; // 1 hour
  }
  
  async getMembers() {
    // Check cache validity
    if (this.cache && this.cacheTime && 
        Date.now() - this.cacheTime < this.cacheValidity) {
      return this.cache;
    }
    
    // Fetch fresh data
    try {
      const response = await fetch('https://odoo.bksc.net/team/members');
      const data = await response.json();
      
      if (data.status === 'ok') {
        this.cache = data.members;
        this.cacheTime = Date.now();
        
        // Store in localStorage for offline access
        localStorage.setItem('team_members', JSON.stringify({
          members: data.members,
          timestamp: this.cacheTime
        }));
        
        return data.members;
      }
    } catch (error) {
      // Try to load from localStorage
      const stored = localStorage.getItem('team_members');
      if (stored) {
        const { members } = JSON.parse(stored);
        return members;
      }
      throw error;
    }
  }
}
```

## Integration Tips

1. **Profile Images**: Cache images locally or use a CDN for better performance
2. **Contact Forms**: Link team member emails to contact forms
3. **Social Media**: Extend the API to include social media links
4. **Availability**: Consider adding availability/schedule information
5. **Languages**: Add spoken languages for international clubs
6. **Certifications**: Include sailing certifications and qualifications

## Security Notes

- Only displays members with `is_team_member = True`
- No sensitive personal information is exposed
- Consider rate limiting to prevent scraping
- Use HTTPS for all API calls
- Validate and sanitize all displayed data