document.getElementById('uploadForm').addEventListener('submit', async function (event) {
	event.preventDefault();
	const fileInput = document.getElementById('fileInput');
	const file = fileInput.files[0];
	const formData = new FormData();
	formData.append('file', file);

	try {
		const response = await fetch('http://localhost:5000/summarize', {
			method: 'POST',
			body: formData,
		});
		const result = await response.json();
		document.getElementById('summaryText').textContent = result.summary;
	} catch (error) {
		console.error('Error:', error);
	}
});

document.getElementById('deleteButton').addEventListener('click', function() {
    document.getElementById('summaryText').innerText = '';
});