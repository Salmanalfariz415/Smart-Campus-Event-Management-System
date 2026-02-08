// Handle event type selection
const eventRadios = document.querySelectorAll('input[name="eventType"]');

eventRadios.forEach(radio => {
    radio.addEventListener('click', (e) => {
        const selectedValue = e.target.value;

        if (selectedValue === 'concert') {
            handleConcertSelection();
        } else if (selectedValue === 'hackathon') {
            handleHackathonSelection();
        }
    });
});

function handleConcertSelection() {
    console.log("Rock on! 🎸 Concert logic triggered.");
}

function handleHackathonSelection() {
    console.log("Happy Hacking! 💻 Hackathon logic triggered.");
}

// Handle form submission
document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form values WHEN SUBMITTED (not when page loads)
    const eventName = document.getElementById("eventName").value;
    const eventDesc = document.getElementById("description").value;
    const eventOrg = document.getElementById("organizer").value;
    const startDate = document.getElementById("startDate").value;
    const startTime = document.getElementById("startTime").value;
    const endDate = document.getElementById("endDate").value;
    const endTime = document.getElementById("endTime").value;
    const venue = document.getElementById("venue").value;
    const building = document.getElementById("building").value;
    const capacity = document.getElementById("capacity").value;
    const fee = document.getElementById("fee").value;
    const registrationRequired = document.getElementById("registrationRequired").checked; // Use .checked not .value
    const contactEmail = document.getElementById("contactEmail").value;
    const website = document.getElementById("website").value;
    const tags = document.getElementById("tags").value;

    console.log('Submitting form data...');

    try {
        const res = await fetch("http://127.0.0.1:5000/event/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: eventName,
                description: eventDesc,
                organization: eventOrg,
                start_date: startDate,
                end_date: endDate,
                start_time: startTime,
                end_time: endTime,
                venue: venue,
                building: building,
                capacity: capacity || null,
                fee: fee || 0,
                reg: registrationRequired,
                image: uploadedImageUrl,
                contact: contactEmail,
                website: website,
                tag: tags
            })
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.message || "Problem in submission");
        }

        const data = await res.json();
        console.log('Success:', data);
        alert('Event published successfully!');

        // Clear the form
        document.querySelector('form').reset();

    } catch (e) {
        console.error('Error:', e);
        alert('Failed to publish event: ' + e.message);
    }
});

// Handle image upload
const imageInput = document.querySelector('input[type="file"]');
const imageDropZone = imageInput.parentElement;

imageDropZone.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    imageDropZone.querySelector('p').textContent = `Selected: ${file.name}`;

    const formData = new FormData();
    formData.append('image', file);

    try {
        const res = await fetch('http://localhost:5000/event/image_upload', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'Upload failed');
        }
        const text = await res.text();
        console.log("RAW RESPONSE:", text);

        let data;
        try {
          data = JSON.parse(text);
        } catch {
          throw new Error("Server did not return JSON");
        }
        uploadedImageUrl = data.image_url;

        console.log('Uploaded image URL:', uploadedImageUrl);
    } catch (err) {
        console.error(err.message);
        imageDropZone.querySelector('p').textContent = 'Upload failed';
    }
});
// Drag and drop for image
imageDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    imageDropZone.classList.add('border-indigo-400');
});

imageDropZone.addEventListener('dragleave', () => {
    imageDropZone.classList.remove('border-indigo-400');
});

imageDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    imageDropZone.classList.remove('border-indigo-400');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        imageInput.files = e.dataTransfer.files;
        imageDropZone.querySelector('p').textContent = `Selected: ${file.name}`;
    }
});