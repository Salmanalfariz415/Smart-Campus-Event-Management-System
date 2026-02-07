
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
    <div class="bg-white rounded-2xl shadow-md p-6 hover:shadow-xl transition">
      <span class="inline-block mb-3 px-3 py-1 text-sm rounded-full bg-pink-100 text-pink-600">
        ${eventData.tag || 'General'}
      </span>

      <h3 class="text-xl font-semibold mb-2">
        ${eventData.username}
      </h3>

      <p class="text-gray-600 text-sm mb-4">
        ${eventData.description}
      </p>

      <div class="text-sm text-gray-500 space-y-1 mb-4">
        <p>📅 ${eventData.start_date}</p>
        <p>⏰ ${eventData.start_time} – ${eventData.end_time}</p>
        <p>📍 ${eventData.venue}</p>
      </div>

      <a href="/event/${eventData.id}"
         class="inline-block mt-2 px-5 py-2 rounded-lg bg-blue-600 text-white text-sm hover:bg-blue-700 transition">
        View Details
      </a>
    </div>
  `;
}