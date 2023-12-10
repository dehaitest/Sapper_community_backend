document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    uploadFile();
});
const accessToken = sessionStorage.getItem('accessToken');
function uploadFile() {
    const input = document.getElementById('fileInput');
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/sapperchain/uploadfile', {
        method: 'POST',
        body: formData, 
        headers: {
            "Authorization": `Bearer ${accessToken}` 
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').textContent = 'File uploaded successfully. Response: ' + JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        document.getElementById('result').textContent = 'Error uploading file.';
    });
}
