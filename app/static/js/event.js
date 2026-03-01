
let eventsData = []; // Global variable to store events
let filteredEvents = []; // Global variable to store filtered events

document.addEventListener('DOMContentLoaded', async () => {
  console.log('DOM loaded, starting fetch...');

  try {
    eventsData = await add_card();
    filteredEvents = [...eventsData]; // Initialize filtered events with all events
    console.log('Events received:', eventsData); // Check what you got
    console.log('Number of events:', eventsData?.length);

    displayEvents(filteredEvents);
    setupSearchFunctionality(); // Setup search functionality

    console.log('All cards added successfully');
  } catch (e) {
    console.error('Failed to load events:', e);
    document.getElementById('eventsContainer').innerHTML =
      '<p class="col-span-full text-center text-red-500">Error loading events</p>';
  }

  // Add event listeners for overlay buttons
  document.getElementById("bookEventBtn").addEventListener("click", handleBooking);
  document.getElementById("shareEventBtn").addEventListener("click", handleSharing);
  
  // Add event listeners for booking modal
  document.getElementById("closeBookingModal").addEventListener("click", () => {
    document.getElementById("bookingModal").classList.add("hidden");
  });
  
  document.getElementById("cancelBooking").addEventListener("click", () => {
    document.getElementById("bookingModal").classList.add("hidden");
  });
  
  document.getElementById("closeSuccessModal").addEventListener("click", () => {
    document.getElementById("bookingSuccessModal").classList.add("hidden");
  });
  
  // Update total amount when attendees count changes
  document.getElementById("attendeesCount").addEventListener("change", updateTotalAmount);
  
  // Handle booking form submission
  document.getElementById("bookingForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const formData = {
      event_id: parseInt(document.getElementById("bookingEventId").value),
      contact_name: document.getElementById("contactName").value,
      contact_email: document.getElementById("contactEmail").value,
      contact_phone: document.getElementById("contactPhone").value,
      attendees_count: parseInt(document.getElementById("attendeesCount").value),
      special_requirements: document.getElementById("specialRequirements").value,
      payment_amount: window.currentEventData?.fee > 0 ? window.currentEventData.fee * parseInt(document.getElementById("attendeesCount").value) : 0
    };
    
    await submitBooking(formData);
  });
  
  // Close modals when clicking outside
  document.getElementById("bookingModal").addEventListener("click", (e) => {
    if (e.target.id === "bookingModal") {
      document.getElementById("bookingModal").classList.add("hidden");
    }
  });
  
  document.getElementById("bookingSuccessModal").addEventListener("click", (e) => {
    if (e.target.id === "bookingSuccessModal") {
      document.getElementById("bookingSuccessModal").classList.add("hidden");
    }
  });
});

// Function to display events
function displayEvents(events) {
  const container = document.getElementById('eventsContainer');
  console.log('Container found:', container); // Make sure container exists

  if (!events || events.length === 0) {
    container.innerHTML = '<div class="col-span-full text-center py-12"><div class="text-gray-500 text-lg mb-2">🔍</div><p class="text-gray-600">No events found matching your search</p><p class="text-gray-500 text-sm mt-2">Try different keywords or clear your search</p></div>';
    return;
  }

  // Clear existing content
  container.innerHTML = '';

  events.forEach((eventData, index) => {
    console.log(`Adding card ${index + 1}:`, eventData);
    container.insertAdjacentHTML('beforeend', createEventCard(eventData, getOriginalIndex(eventData)));
  });

  // Re-attach event listeners for the new cards
  attachEventListeners();
}

// Function to get original index of event in eventsData array
function getOriginalIndex(eventData) {
  return eventsData.findIndex(event => event.id === eventData.id);
}

// Function to setup search functionality
function setupSearchFunctionality() {
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const filterButton = document.querySelector('.btn');

  if (!searchInput || !searchButton) {
    console.warn('Search elements not found');
    return;
  }

  // Real-time search as user types
  searchInput.addEventListener('input', (e) => {
    performSearch(e.target.value);
  });

  // Search on button click
  searchButton.addEventListener('click', () => {
    performSearch(searchInput.value);
  });

  // Search on Enter key
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      performSearch(searchInput.value);
    }
  });

  // Clear search functionality
  searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Escape' || (e.key === 'Backspace' && searchInput.value === '')) {
      performSearch('');
    }
  });

  // Filter button functionality (placeholder for future enhancement)
  if (filterButton) {
    filterButton.addEventListener('click', () => {
      // Placeholder for filter modal/dropdown
      console.log('Filter functionality - to be implemented');
    });
  }
}

// Function to perform search
function performSearch(searchQuery) {
  const query = searchQuery.toLowerCase().trim();
  
  if (!query) {
    // If search is empty, show all events
    filteredEvents = [...eventsData];
  } else {
    // Filter events based on search query
    filteredEvents = eventsData.filter(event => {
      return (
        // Search in title
        (event.title && event.title.toLowerCase().includes(query)) ||
        // Search in description
        (event.description && event.description.toLowerCase().includes(query)) ||
        // Search in organization
        (event.organization && event.organization.toLowerCase().includes(query)) ||
        // Search in venue
        (event.venue && event.venue.toLowerCase().includes(query)) ||
        // Search in building
        (event.building && event.building.toLowerCase().includes(query)) ||
        // Search in event category
        (event.event_category && event.event_category.toLowerCase().replace(/_/g, ' ').includes(query)) ||
        // Search in tag
        (event.tag && event.tag.toLowerCase().includes(query)) ||
        // Search in event type
        (event.event_type && event.event_type.toLowerCase().includes(query))
      );
    });
  }

  // Update the display
  displayEvents(filteredEvents);
  
  // Update search input styling based on results
  const searchInput = document.getElementById('searchInput');
  if (query && filteredEvents.length === 0) {
    searchInput.classList.add('border-red-400', 'focus:border-red-500');
    searchInput.classList.remove('border-indigo-400', 'focus:border-purple-500');
  } else {
    searchInput.classList.remove('border-red-400', 'focus:border-red-500');
    searchInput.classList.add('border-indigo-400', 'focus:border-purple-500');
  }
}

// Function to attach event listeners to event cards
function attachEventListeners() {
  const buttons = document.querySelectorAll(".event_button");
  const overlay = document.getElementById("eventOverlay");
  const closeBtn = document.getElementById("closeOverlay");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const eventIndex = parseInt(btn.dataset.index);
      const eventData = eventsData[eventIndex];
      if (!eventData) return;

      populateOverlay(eventData);
      overlay.classList.remove("hidden");
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      overlay.classList.add("hidden");
    });
  }

  if (overlay) {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.add("hidden");
      }
    });
  }
}

// Function to populate overlay with event data
function populateOverlay(eventData) {
  // Header
  document.getElementById("overlayTitle").textContent = eventData.title;
  document.getElementById("overlayCategory").textContent = 
    eventData.event_type === 'hackathon' ? '📚 Scholastic' : '🎉 Non-Scholastic';
  document.getElementById("overlayFee").textContent = 
    eventData.fee > 0 ? `₹${eventData.fee}` : 'FREE';
    
  // Update header gradient based on event type
  const header = document.getElementById("overlayHeader");
  header.className = eventData.event_type === 'hackathon' 
    ? 'h-32 bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-500 rounded-t-2xl relative overflow-hidden'
    : 'h-32 bg-gradient-to-r from-purple-500 via-pink-500 to-rose-500 rounded-t-2xl relative overflow-hidden';
  
  // Organization
  if (eventData.organization) {
    document.getElementById("overlayOrgIcon").textContent = 
      eventData.organization.charAt(0).toUpperCase();
    document.getElementById("overlayOrgName").textContent = eventData.organization;
    document.getElementById("overlayOrganization").style.display = 'flex';
  } else {
    document.getElementById("overlayOrganization").style.display = 'none';
  }
  
  // Description
  document.getElementById("overlayDesc").textContent = eventData.description;
  
  // Date & Time
  const dateText = eventData.end_date && eventData.end_date !== eventData.start_date 
    ? `${eventData.start_date} - ${eventData.end_date}`
    : eventData.start_date;
  document.getElementById("overlayDate").textContent = dateText;
  document.getElementById("overlayTime").textContent = `${eventData.start_time} – ${eventData.end_time}`;
  
  // Location
  document.getElementById("overlayVenue").textContent = eventData.venue;
  document.getElementById("overlayBuilding").textContent = eventData.building || '';
  
  // Capacity
  if (eventData.capacity) {
    document.getElementById("overlayCapacity").textContent = `${eventData.capacity} attendees`;
    document.getElementById("overlayCapacitySection").style.display = 'block';
  } else {
    document.getElementById("overlayCapacitySection").style.display = 'none';
  }
  
  // Registration
  document.getElementById("overlayRegistration").textContent = 
    eventData.reg ? 'Registration Required' : 'No Registration Required';
  
  // Tags
  const tagsContainer = document.getElementById("overlayTags");
  tagsContainer.innerHTML = '';
  
  if (eventData.tag) {
    tagsContainer.innerHTML += `<span class="px-2 py-1 bg-pink-100 text-pink-700 text-xs font-semibold rounded-md">${eventData.tag}</span>`;
  }
  
  if (eventData.event_category) {
    tagsContainer.innerHTML += `<span class="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-md">${eventData.event_category.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</span>`;
  }
  
  if (tagsContainer.innerHTML === '') {
    document.getElementById("overlayTagsSection").style.display = 'none';
  } else {
    document.getElementById("overlayTagsSection").style.display = 'block';
  }
  
  // Contact & Website
  if (eventData.contact) {
    document.getElementById("overlayContact").href = `mailto:${eventData.contact}`;
    document.getElementById("overlayContactSection").style.display = 'block';
  } else {
    document.getElementById("overlayContactSection").style.display = 'none';
  }
  
  if (eventData.website) {
    document.getElementById("overlayWebsite").href = eventData.website;
    document.getElementById("overlayWebsiteSection").style.display = 'block';
  } else {
    document.getElementById("overlayWebsiteSection").style.display = 'none';
  }
  
  // Store current event data for booking
  window.currentEventData = eventData;
}

// Booking functionality - Updated to use booking modal
function handleBooking() {
  const eventData = window.currentEventData;
  if (!eventData) return;
  
  // Show booking modal instead of simple actions
  showBookingModal(eventData);
}

// Show booking modal
function showBookingModal(eventData) {
  const modal = document.getElementById('bookingModal');
  const eventTitle = document.getElementById('bookingEventTitle');
  const eventId = document.getElementById('bookingEventId');
  const eventFee = document.getElementById('eventFee');
  const totalAmount = document.getElementById('totalAmount');
  
  // Populate modal with event data
  eventTitle.textContent = eventData.title;
  eventId.value = eventData.id;
  
  // Set fee information
  const feeText = eventData.fee > 0 ? `₹${eventData.fee}` : 'FREE';
  eventFee.textContent = feeText;
  updateTotalAmount(); // Calculate initial total
  
  modal.classList.remove('hidden');
}

// Update total amount based on attendees
function updateTotalAmount() {
  const eventData = window.currentEventData;
  const attendeesCount = parseInt(document.getElementById('attendeesCount').value) || 1;
  const totalElement = document.getElementById('totalAmount');
  
  if (eventData && eventData.fee > 0) {
    const total = eventData.fee * attendeesCount;
    totalElement.textContent = `₹${total}`;
  } else {
    totalElement.textContent = 'FREE';
  }
}

// Handle booking form submission
async function submitBooking(formData) {
  try {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch('http://127.0.0.1:5000/booking/create', {
      method: 'POST',
      headers,
      body: JSON.stringify(formData)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      // Hide booking modal and show success modal
      document.getElementById('bookingModal').classList.add('hidden');
      showBookingSuccess(result.booking_reference);
    } else {
      alert(`Booking failed: ${result.error}`);
    }
  } catch (error) {
    console.error('Booking error:', error);
    alert('Booking failed. Please try again.');
  }
}

// Show booking success modal
function showBookingSuccess(bookingReference) {
  const modal = document.getElementById('bookingSuccessModal');
  const refElement = document.getElementById('bookingReference');
  
  refElement.textContent = bookingReference;
  modal.classList.remove('hidden');
}

// Sharing functionality
function handleSharing() {
  const eventData = window.currentEventData;
  if (!eventData) return;
  
  const shareText = `Check out this event: ${eventData.title}\n📅 ${eventData.start_date}\n📍 ${eventData.venue}\n\n${eventData.description}`;
  
  if (navigator.share) {
    // Use native sharing if available
    navigator.share({
      title: eventData.title,
      text: shareText,
      url: window.location.href
    });
  } else {
    // Fallback to copying to clipboard
    navigator.clipboard.writeText(shareText).then(() => {
      alert('Event details copied to clipboard!');
    }).catch(() => {
      // Final fallback
      const textArea = document.createElement('textarea');
      textArea.value = shareText;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      alert('Event details copied to clipboard!');
    });
  }
};


async function add_card(){
  try{
    const res=await fetch("http://127.0.0.1:5000/event/add_card",{
      method:"GET",
    })
    if(!res.ok){
      throw new Error("Problem in retrieving info from db");
    }
    const data=await res.json();
    console.log('Success:', data);
    return data;

  }catch(e){
    console.error('Error:',e);
  }
}

function createEventCard(eventData, index) {
  return `
    <div class="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 event-card">
      
      <!-- Image Header (if available) -->
      ${eventData.image_url ? `
  <div class="relative h-48 overflow-hidden">
    <img src="${eventData.image_url}" 
         alt="${eventData.username}" 
         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
    
    <!-- Event Type Badge -->
    <span class="absolute top-3 left-3 px-3 py-1 text-xs font-semibold rounded-full ${eventData.event_type === 'hackathon' ? 'bg-blue-500 text-white' : 'bg-purple-500 text-white'} shadow-lg">
      ${eventData.event_type === 'hackathon' ? '📚 Scholastic' : '🎉 Non-Scholastic'}
    </span>
    
    <!-- Fee Badge -->
    ${eventData.fee > 0 ? `
      <span class="absolute top-3 right-3 px-3 py-1 text-xs font-bold rounded-full bg-green-500 text-white shadow-lg">
        ₹${eventData.fee}
      </span>
    ` : `
      <span class="absolute top-3 right-3 px-3 py-1 text-xs font-bold rounded-full bg-green-500 text-white shadow-lg">
        FREE
      </span>
    `}
  </div>
` : `
        <!-- Gradient Header (no image) -->
        <div class="relative h-32 ${eventData.event_type === 'hackathon' ? 'bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-500' : 'bg-gradient-to-r from-purple-500 via-pink-500 to-rose-500'}">
          <div class="absolute inset-0 opacity-20">
            <div class="absolute top-0 left-0 w-24 h-24 bg-white rounded-full -translate-x-12 -translate-y-12"></div>
            <div class="absolute bottom-0 right-0 w-32 h-32 bg-white rounded-full translate-x-16 translate-y-16"></div>
          </div>
          <div class="relative p-4 flex items-start justify-between">
            <span class="px-3 py-1 text-xs font-semibold rounded-full bg-white/95 backdrop-blur-sm ${eventData.event_type === 'hackathon' ? 'text-blue-600' : 'text-purple-600'} shadow-lg">
              ${eventData.event_type === 'hackathon' ? '📚 Scholastic' : '🎉 Non-Scholastic'}
            </span>
            ${eventData.fee > 0 ? `
              <span class="px-3 py-1 text-xs font-bold rounded-full bg-white text-green-600 shadow-lg">
                ₹${eventData.fee}
              </span>
            ` : `
              <span class="px-3 py-1 text-xs font-bold rounded-full bg-white text-green-600 shadow-lg">
                FREE
              </span>
            `}
          </div>
        </div>
      `}

      <!-- Content Section -->
      <div class="p-6">
        
        <!-- Organization -->
        ${eventData.organization ? `
          <div class="flex items-center gap-2 mb-3">
            <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
              ${eventData.organization.charAt(0).toUpperCase()}
            </div>
            <span class="text-sm text-gray-600 font-medium">${eventData.organization}</span>
          </div>
        ` : ''}

        <!-- Event Category Badge -->
        ${eventData.event_category ? `
          <span class="inline-block px-2 py-1 mb-2 text-xs font-medium rounded-md ${eventData.event_type === 'hackathon' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'}">
            ${eventData.event_category.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
          </span>
        ` : ''}

        <!-- Event Title -->
        <h3 class="event-title text-xl font-bold mb-2 text-gray-800 group-hover:text-blue-600 transition-colors line-clamp-2">
          ${eventData.title}
        </h3>

        <!-- Description -->
        <p class="event-desc text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
          ${eventData.description}
        </p>

        <!-- Event Details -->
        <div class="space-y-2 mb-4">
          
          <!-- Date Range -->
          <div class="flex items-start gap-2 text-sm">
            <span class="text-blue-500 mt-0.5">📅</span>
            <div>
              <span class="text-gray-700 font-medium">
                ${eventData.start_date}${eventData.end_date && eventData.end_date !== eventData.start_date ? ` - ${eventData.end_date}` : ''}
              </span>
            </div>
          </div>

          <!-- Time -->
          <div class="flex items-start gap-2 text-sm">
            <span class="text-purple-500 mt-0.5">⏰</span>
            <span class="text-gray-700 font-medium">${eventData.start_time} – ${eventData.end_time}</span>
          </div>

          <!-- Venue -->
          <div class="flex items-start gap-2 text-sm">
            <span class="text-pink-500 mt-0.5">📍</span>
            <span class="text-gray-700 font-medium">
              ${eventData.venue}${eventData.building ? `, ${eventData.building}` : ''}
            </span>
          </div>

          <!-- Capacity -->
          ${eventData.capacity ? `
            <div class="flex items-start gap-2 text-sm">
              <span class="text-green-500 mt-0.5">👥</span>
              <span class="text-gray-700 font-medium">Capacity: ${eventData.capacity} people</span>
            </div>
          ` : ''}

        </div>

        <!-- Info Pills -->
        <div class="flex flex-wrap gap-2 mb-4">
          ${eventData.tag ? `
            <span class="px-2 py-1 bg-pink-100 text-pink-700 text-xs font-semibold rounded-md">
              ${eventData.tag}
            </span>
          ` : ''}
          
          ${eventData.reg ? `
            <span class="px-2 py-1 bg-amber-100 text-amber-700 text-xs font-semibold rounded-md">
              Registration Required
            </span>
          ` : ''}
          
          ${eventData.website ? `
            <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-md">
              Website Available
            </span>
          ` : ''}
          
          ${eventData.contact ? `
            <span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-md">
              Contact Info
            </span>
          ` : ''}
        </div>

        <!-- Action Button -->
        <button
           class="event_button block w-full text-center px-5 py-3 rounded-lg bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transform hover:scale-[1.02] transition-all shadow-sm hover:shadow-md" data-index="${index}">
          View Full Details →
        </button>

      </div>
    </div>
  `;
}
