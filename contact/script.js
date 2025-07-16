const contactList = document.getElementById('contactList');
const refreshBtn = document.getElementById('refreshBtn');
const addContactForm = document.getElementById('addContactForm');
const nameInput = document.getElementById('nameInput');
const emailInput = document.getElementById('emailInput');
const phoneInput = document.getElementById('phoneInput');

// Your API URL (Replace this with your real API)
const API_URL = 'https://jsonplaceholder.typicode.com/users';

// Load contacts
async function loadContacts() {
  contactList.innerHTML = '<p>Loading contacts...</p>';
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    contactList.innerHTML = '';

    data.forEach(contact => {
      const card = document.createElement('div');
      card.className = 'contact-card';
      card.innerHTML = `
        <h2>${contact.name}</h2>
        <p>Email: ${contact.email}</p>
        <p>Phone: ${contact.phone}</p>
        <div class="card-actions">
          <button onclick="editContact(${contact.id})">✏️ Edit</button>
          <button onclick="deleteContact(${contact.id})">🗑️ Delete</button>
        </div>
      `;
      contactList.appendChild(card);
    });
  } catch (error) {
    contactList.innerHTML = '<p>Error loading contacts.</p>';
    console.error(error);
  }
}

// Refresh button
refreshBtn.addEventListener('click', loadContacts);

// Add contact
addContactForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const newContact = {
    name: nameInput.value,
    email: emailInput.value,
    phone: phoneInput.value
  };
  try {
    // In real API, use POST
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(newContact)
    });
    const data = await response.json();
    alert('Contact added!');
    // Optionally reload the list
    loadContacts();
    addContactForm.reset();
  } catch (error) {
    alert('Error adding contact.');
    console.error(error);
  }
});

// Edit contact (placeholder)
function editContact(id) {
  alert('Edit functionality coming soon for ID ' + id);
}

// Delete contact
async function deleteContact(id) {
  if (!confirm('Are you sure you want to delete this contact?')) return;
  try {
    // In real API, use DELETE
    await fetch(`${API_URL}/${id}`, {method: 'DELETE'});
    alert('Contact deleted!');
    loadContacts();
  } catch (error) {
    alert('Error deleting contact.');
    console.error(error);
  }
}

// Load on start
loadContacts();
