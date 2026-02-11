
document.addEventListener('DOMContentLoaded', async () => {
  console.log('DOM loaded, starting fetch...');

  try {
    const events = await add_card();
    console.log('Events received:', events); // Check what you got
    console.log('Number of events:', events?.length);

    const container = document.getElementById('eventsContainer');
    console.log('Container found:', container); // Make sure container exists

    if (!events || events.length === 0) {
      console.warn('No events to display');
      container.innerHTML = '<p class="col-span-full text-center">No events available</p>';
      return;
    }

    events.forEach((eventData, index) => {
      console.log(`Adding card ${index + 1}:`, eventData);
      container.insertAdjacentHTML('beforeend', createEventCard(eventData));
    });

    console.log('All cards added successfully');
  } catch (e) {
    console.error('Failed to load events:', e);
    document.getElementById('eventsContainer').innerHTML =
      '<p class="col-span-full text-center text-red-500">Error loading events</p>';
  }

  const buttons = document.querySelectorAll(".event_button");
  const overlay = document.getElementById("eventOverlay");
  const closeBtn = document.getElementById("closeOverlay");
  const overlayTitle = document.getElementById("overlayTitle");
  const overlayDesc = document.getElementById("overlayDesc");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {

      const card = btn.closest(".event-card");
      if (!card) return;

      overlayTitle.textContent =
        card.querySelector(".event-title")?.textContent || "";

      overlayDesc.textContent =
        card.querySelector(".event-desc")?.textContent || "";

      overlay.classList.remove("hidden");
    });
  });

  closeBtn.addEventListener("click", () => {
    overlay.classList.add("hidden");
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      overlay.classList.add("hidden");
    }
  });
});


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

function createEventCard(eventData) {
  return `
    <div class="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
      
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
        <h3 class="text-xl font-bold mb-2 text-gray-800 group-hover:text-blue-600 transition-colors line-clamp-2">
          ${eventData.title}
        </h3>

        <!-- Description -->
        <p class="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
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
           class="event_button block w-full text-center px-5 py-3 rounded-lg bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transform hover:scale-[1.02] transition-all shadow-sm hover:shadow-md">
          View Full Details →
        </button>

      </div>
    </div>
  `;
}
